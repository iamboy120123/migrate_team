---
paths:
  - "run_packs/**"
  - "scripts/runpack/gen_run_pack.py"
  - "scripts/runpack/gen_preflight_pack.py"
  - "scripts/runpack/read_run_results.py"
---
# กฎ Run Pack (courier loop — คนรันใน DBeaver แล้วส่งผลกลับ)

1. สคริปต์ Oracle เป็น SELECT / DML ธรรมดา — **ห้าม `SET` / `SPOOL` / `PROMPT` / `WHENEVER`** (ORA-00922) และห้ามบรรทัด `/` (V7 FAIL)
2. ไฟล์ที่มีหลาย statement → README และ comment หัวไฟล์ต้องบอก **Execute Script (Alt+X)** · SELECT เดียว → Ctrl+Enter
3. ผลลัพธ์ต้องอ่านได้ด้วย `read_run_results.py` (จำไฟล์จาก header ไม่ใช่ชื่อไฟล์) — assertions = SELECT เดียวคืน `TEST_CASE, ..., RESULT`
4. DBeaver export NULL เป็น `" "` — reader strip ให้แล้ว ห้ามตีความเป็นค่า
5. DML ทดสอบ (seed / cleanup) รันบน **Dev เท่านั้น**, มี marker ลบได้, บอกเส้นตาย precheck lag ใน comment
6. seed หลาย statement รัน Alt+X **ครั้งเดียว** แล้วตรวจ count ทันที (L4)
7. สคริปต์ของ Blendata (Spark SQL) ใส่ `blendata` / `spark` ในชื่อไฟล์หรือหัวไฟล์ — V7 ยกเว้นกฎ SET ให้
8. ORA error ที่ไม่อยู่ใน `KNOWN_ERRORS` ของ reader = **ห้ามเดาแก้** → `/diagnose` ขอ log เพิ่ม
9. ห้ามแก้ไฟล์ใน `input/run_results/` (เป็นหลักฐานจากคนรัน) — สรุปผลใน `run_packs/<pack>/REPORT.md` ผ่าน reader เท่านั้น
