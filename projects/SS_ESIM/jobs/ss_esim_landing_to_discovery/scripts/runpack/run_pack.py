"""
run_pack.py — รัน Run Pack ทั้งชุดด้วยคำสั่งเดียว (อ่านอย่างเดียว) แทนการเปิด DBeaver + export ทีละไฟล์

Usage:
    python scripts/runpack/run_pack.py rp00            # รันทุก .sql ใน run_packs/rp00*/ → input/run_results/<pack>/<ไฟล์>.csv
    python scripts/runpack/run_pack.py rp00 --check    # ตรวจอย่างเดียวว่าทุกไฟล์เป็น SELECT ไม่ต่อฐาน
    python scripts/runpack/run_pack.py rp_compile --compile   # คอมไพล์ SQL แบบ WHERE 1=0 · error = ผลตรวจ ไม่หยุด → output/verify/sql_compile.txt

รั้ว (ทุกรูปแบบ):
  - รับเฉพาะคำสั่งเดียวที่ขึ้นต้นด้วย SELECT / WITH · DDL / DML / PL/SQL / FOR UPDATE / ;หลายคำสั่ง = ปฏิเสธทั้ง pack (exit 2)
  - session เป็น READ ONLY และ rollback ตอนจบเสมอ
  - การเชื่อมต่อ: shared/db.local.json ของ workspace (host · port · service · user — ไม่มีรหัสผ่าน)
    รหัสผ่านจากตัวแปร ORA_RO_PASSWORD บนเครื่องเท่านั้น · ไม่พิมพ์ ไม่เขียนลงไฟล์ · ไม่รับทาง argument
  - ทุก query ถูกบันทึกที่ input/run_results/<pack>/_run_log.txt (ผลรันไม่ขึ้น Git)
ต้องมี python-oracledb (pip install oracledb) — thin mode ไม่ต้องลง Oracle Client
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[2]
BAD_START = re.compile(r"^\s*(insert|update|delete|merge|create|alter|drop|truncate|grant|revoke|rename|comment|begin|declare|call|exec|execute|lock|commit|rollback|savepoint|set|analyze|purge|flashback|audit)\b", re.I)
BAD_ANY = re.compile(r"\bfor\s+update\b|\binto\s+[:\w]+\s+from\b|\bdbms_\w+\s*\.\s*(?!output)|\butl_\w+\s*\.", re.I)


def ws_root():
    for p in [ROOT, *ROOT.parents]:
        if (p / "workspace.json").exists():
            return p
    return None


def strip_sql(s: str) -> str:
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    out, q = [], False
    for line in s.splitlines():
        buf, i = "", 0
        while i < len(line):
            c = line[i]
            if c == "'":
                q = not q
            if not q and line[i:i + 2] == "--":
                break
            buf += c
            i += 1
        out.append(buf)
    return "\n".join(out).strip()


def statements(s: str) -> list[str]:
    parts, cur, q = [], "", False
    for c in s:
        if c == "'":
            q = not q
        if c == ";" and not q:
            parts.append(cur)
            cur = ""
        else:
            cur += c
    parts.append(cur)
    parts = [p.strip() for p in parts if p.strip() and p.strip() != "/"]
    return parts


def vet(path: Path) -> tuple[str | None, str]:
    """(ข้อความ error, sql ที่จะรัน)"""
    body = strip_sql(path.read_text(encoding="utf-8-sig", errors="replace"))
    st = statements(body)
    if len(st) != 1:
        return f"ต้องมีคำสั่งเดียว (พบ {len(st)})", ""
    sql = st[0]
    if BAD_START.search(sql) or not re.match(r"^\s*(select|with)\b", sql, re.I):
        return "รับเฉพาะ SELECT / WITH", ""
    if BAD_ANY.search(sql):
        return "มีส่วนที่เขียนข้อมูล / เรียก package (FOR UPDATE · INTO · DBMS_ / UTL_)", ""
    return None, sql


def connect():
    w = ws_root()
    cfgp = (w / "shared/db.local.json") if w else None
    if not cfgp or not cfgp.exists():
        raise SystemExit("[ERROR] ไม่พบ shared/db.local.json ของ workspace — ทีมยังไม่ได้ตั้งการเชื่อมต่อ (init ข้อ 9) · ให้คนรัน SQL ใน DBeaver แทน")
    c = json.loads(cfgp.read_text(encoding="utf-8"))
    pw = os.environ.get("ORA_RO_PASSWORD")
    if not pw:
        raise SystemExit("[ERROR] ไม่มีตัวแปร ORA_RO_PASSWORD บนเครื่องนี้ — ตั้งเอง (Windows: setx ORA_RO_PASSWORD \"…\" แล้วเปิด Terminal ใหม่) · ห้ามพิมพ์รหัสในแชท")
    try:
        import oracledb
    except ImportError:
        raise SystemExit("[ERROR] ต้องติดตั้ง python-oracledb: pip install oracledb")
    conn = oracledb.connect(user=c["user"], password=pw, dsn=f"{c['host']}:{c.get('port', 1521)}/{c['service']}")
    conn.autocommit = False
    cur = conn.cursor()
    cur.execute("SET TRANSACTION READ ONLY")
    return conn, c["user"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--compile", action="store_true")
    a = ap.parse_args()
    packs = sorted(p for p in (ROOT / "run_packs").glob(f"{a.pack}*") if p.is_dir())
    if not packs:
        raise SystemExit(f"[ERROR] ไม่พบ run_packs/{a.pack}*")
    pack = packs[-1]
    files = sorted(pack.glob("*.sql"))
    if not files:
        raise SystemExit(f"[ERROR] {pack.name} ไม่มีไฟล์ .sql")
    vetted, bad = [], []
    for f in files:
        err, sql = vet(f)
        (bad.append((f.name, err)) if err else vetted.append((f, sql)))
    if bad:
        for n, e in bad:
            print(f"  ⛔ {n}: {e}")
        print(f"[BLOCKED] {pack.name}: มีไฟล์ที่ไม่ใช่ SELECT อย่างเดียว {len(bad)} ไฟล์ — ไม่รันทั้ง pack (ให้คนตรวจ / รันเองถ้าจำเป็น)")
        sys.exit(2)
    print(f"✅ {pack.name}: {len(vetted)} ไฟล์ เป็น SELECT อย่างเดียว")
    if a.check:
        return
    out = ROOT / "input" / "run_results" / pack.name
    out.mkdir(parents=True, exist_ok=True)
    conn, user = connect()
    log = open(out / "_run_log.txt", "a", encoding="utf-8")
    log.write(f"\n# {dt.datetime.now().isoformat(timespec='seconds')} pack={pack.name} user={user} (READ ONLY)\n")
    comp = []
    try:
        cur = conn.cursor()
        for f, sql in vetted:
            t0 = time.time()
            try:
                cur.execute(sql)
                cols = [d[0] for d in cur.description or []]
                rows = cur.fetchall() if cols else []
                with open(out / (f.stem + ".csv"), "w", encoding="utf-8-sig", newline="") as fh:
                    w = csv.writer(fh)
                    w.writerow(cols)
                    for r in rows:
                        w.writerow(["" if v is None else (v.isoformat(sep=" ") if hasattr(v, "isoformat") else v) for v in r])
                msg = f"{len(rows)} แถว" + (" (0 แถว — ไม่นับว่าผ่าน ตรวจเงื่อนไข)" if not rows and not a.compile else "")
                print(f"  ✅ {f.name}: {msg} · {time.time() - t0:.1f}s")
                log.write(f"{f.name}\tOK\t{len(rows)}\t{time.time() - t0:.2f}s\n")
                comp.append((f.name, "OK", ""))
            except Exception as e:
                m = str(e).splitlines()[0][:200]
                print(f"  ❌ {f.name}: {m}")
                log.write(f"{f.name}\tERROR\t{m}\n")
                comp.append((f.name, "ERROR", m))
                if not a.compile:
                    print("  (error ที่ไม่รู้จัก: ส่งข้อความนี้ให้ AI /diagnose — ไม่เดา)")
    finally:
        conn.rollback()
        conn.close()
        log.close()
    if a.compile:
        vp = ROOT / "output" / "verify" / "sql_compile.txt"
        vp.parent.mkdir(parents=True, exist_ok=True)
        vp.write_text("# คอมไพล์ SQL กับฐานจริง (WHERE 1=0) — " + dt.datetime.now().isoformat(timespec="seconds") + "\n" +
                      "\n".join(f"{n}\t{s}\t{m}" for n, s, m in comp) + "\n", encoding="utf-8")
        print(f"→ {vp.relative_to(ROOT).as_posix()}")
    print(f"ผลอยู่ที่ input/run_results/{pack.name}/ · ต่อไป: /read-results {pack.name}")


if __name__ == "__main__":
    main()
