# Migration Status — ss_esim_landing_to_discovery (Blendata → ODI)

Updated: 2026-10-29 (rev.17) | SA: 41642975+iamboy120123@users.noreply.github.com

> สร้างโดย `setup_migrate.ps1` — Claude Code อัปเดตไฟล์นี้ด้วย `/update-status` ทุกครั้งที่จบ step

## 1. Scope

| รายการ | ค่า |
|---|---|
| Workflow | `ss_esim_landing_to_discovery` |
| Blendata export | `input/blendata/export_workflow.json` |
| ODI project / package | `SS_ESIM_L2D` / `PKG_SS_ESIM_L2D` |
| Logical schema / context | `DSS_ODI_LOG` / `DEV` |
| Excluded tasks | - (ไม่ตัด) · placeholder 3 task: 000000 recover · 080000 retention · 999999 export MSSQL (I12) |

## 2. สถานะรายเฟส

| Phase | งาน | สถานะ |
|---|---|---|
| 0 | Setup / config (`setup_migrate.ps1`) + pre-flight | ✅ setup 2026-10-28 · PREFLIGHT 5/5 · **G0 PASS** 2026-10-29 (✅ SA 2026-10-29 @mana-ma) |
| 1-3 | Extract + Convert | ✅ 2026-10-28 รันออฟไลน์ก่อน G0 (PREFLIGHT 2/5) ตาม SA เลือก ✅ SA 2026-10-28 @mana-ma · 12 task: SQL 10 / non-SQL 2 · REVIEW_FLAGS 11 PENDING |
| 4 | SQL Review | ✅ 2026-10-29 REVIEW_FLAGS 11/11 · SQL_REVIEW ✅5 🟡5 (ความเร็ว · NO_CHANGE ครบ) ⛔0 · Q3 ปิด · GAP-01..06 มี disposition · **G2 PASS** (G2.M1 ✅ SA 2026-10-29 @mana-ma) |
| 5 | DML + ODI Smart Import XML | ✅ 2026-10-29 build `output/odi_export/PKG_SS_ESIM_L2D.zip` · **เกรด B (ส่งได้ มีเงื่อนไข)** · 12 procedure / 0 variable · chain 000000→…→999999 · validate_odi_xml error 0 / warn 0 · pre_delivery_gate FAIL 0 · check_inputs [พร้อม] · G3 PASS · GlobalId ใหม่ทั้งหมด (import ครั้งแรก) · ยังไม่ Smart Import |
| 6 | DDL / DBA prereq | ⏳ |
| 7 | Validation (Dev run + L1/L2/L3) | ⏳ |
| 8 | Backfill / Cutover | ⏳ |

## 3. Package (ลำดับรันใน ODI)

_(เติมหลัง Phase 5)_

## 4. การตัดสินใจที่ปิดแล้ว

_(ดู `status/OPEN_DECISIONS.md`)_

## 5. ยังค้าง

- [x] rev.2 2026-10-28 — /intake: I4 (Q8 odiref), I12 (3 placeholder), I14 (Q9–Q11), I15 (As-Is), I16 (repo เดียวกัน), concat_policy=spark_null · ค้าง I10 (หลัง /convert), I13 (หลัง /gen-export)
- [ ] repo `Migrate_team` ยังไม่มี remote `origin` — push branch R01 ยังไม่ยืนยัน
- [x] ถอด `000000` จาก `v_max_partition.replaces_tasks` แล้ว (I12) — variable ยังอยู่ รอ Q2
- [ ] rp00_preflight: P1–P4 (Oracle Dev) + P5 (Blendata) → ปิด G0, Q3, Q4, Q7 · 2026-10-29 ครบ P1–P5 + P5b · Q3 ปิด (✅ SA 2026-10-29)
- [ ] GAP-01 timezone (Q5) · GAP-02 LEGACY parse · GAP-05/06 DYNAMIC overwrite → ทบทวน Q9/Q10 · regex ปิดแล้ว (GAP-03 K) · เดิม: escapedStringLiterals=true → regex `\\d` ใน 040000 อาจไม่ match ใน Blendata (file_date NULL ทุกแถว / type_error ไม่ถูกตัด) · timeParserPolicy=LEGACY → to_timestamp ผ่อนปรน (Oracle เข้มกว่า → TYP มากขึ้น) · session.timeZone=UTC → now() = UTC แต่ SYSDATE = เวลา DB (Q5)
- [x] DDL `ext_dss_checkpoint_tb_transaction_ss_esim_valid` ไม่มีใน DSSDEV (P3) → waiver W1 (✅ SA 2026-10-29) + K3
- [ ] ✅ ของ SA ที่ agent บันทึกจากแชต ต้อง commit จากบัญชีผู้อนุมัติ `mana-ma`

- [ ] `/inputs` ขึ้น `[พร้อม]` (ของครบ) → build → **Smart Import ครั้งเดียว** → ทดสอบ (`/run-pack`)
- [x] `odi.work_repo_schema = SYSTEM` (P4/P4b 2026-10-29 · Q7 ✅ SA 2026-10-29 @mana-ma)
- [x] Q4 data contract = all_tab_columns Dev (✅ SA 2026-10-29) · ค้าง: ผู้เติม landing ใน Prod
- [ ] Q14 เวลาไทย (SYSDATE): ยืนยัน timezone ของ `partition_minute` ที่ผู้เติม landing ใน Oracle เขียน · downstream ยอมรับ +7 ชม. · แผนรอยต่อ cutover (ข้อมูลเก่า UTC)
- [x] G2.M1 ✅ SA 2026-10-29
- [ ] builder warning: SqlIndGrp ของ DELETE/SELECT มาจากตัวอย่างเดียวใน reference · SnpLineTrt.FirstUser = SUPERVISOR (ค่า default) → ตรวจหลัง import
- [x] intake I1–I17 ครบ (I13 ✅ SA 2026-10-29)
- [ ] เมื่อ implement 999999 จริง: ย้าย step 999999 ให้อยู่ก่อน 090000 ตาม DAG (I13)
- [x] 05.1 DDL: ไม่ต้องรัน — ตารางมีแล้ว (DEPLOY_LOG, P3)
- [ ] Dev DB = **21c XE** ไม่ใช่ 19c → re-test บน 19c ก่อน cutover (G6.M1)

## 6. Kit — สิ่งที่แก้/เพิ่ม

| # | ไฟล์ | รายละเอียด |
|---|---|---|
| K4 | `config/config.json` `odi.variables` (สร้างโดย setup_migrate) | refresh_query ของ v_max_partition / v_lag_minutes อ่าน `partition_minute` จากตาราง status (`tb_staging_..._workflow_status`) ซึ่งไม่มีคอลัมน์นี้ — ควรเป็น landing `tb_landing_ss_esim` · ถอดออกตาม Q2 B · placeholder no-op เปลี่ยนจาก `BEGIN NULL; END;` เป็น `SELECT ... FROM DUAL` (reference ไม่มี SqlIndGrp ของ BEGIN) · เสนอ /kit-backport |
| K6 | `scripts/checks/review_report.py` (backup `.bak-20261029`) | (1) `tid = stem.split('_')[0]` = "task" → flag ของทุก task ปนกัน (⛔ 10 เท็จ) → ใช้ `task_<id>` · (2) รับสถานะ `RESOLVED (เหตุผล)` · (3) ⑤ หา procedure ใน XML ด้วยชื่อที่ตัด `task_<id>_` ออก · ผล ✅5 🟡5 ⛔0 · เสนอ /kit-backport |
| K5 | `scripts/checks/verify_all.py` `result_csvs()` (backup `.bak-20261029`) | crash `'list' object has no attribute 'strip'` เมื่อไฟล์ใน run_results มีแถวคอลัมน์เกิน header (P5b.csv) → ข้าม restkey · เสนอ /kit-backport |
| K3 | `scripts/checks/check_inputs.py` `check_ddl()` (backup `.bak-20261029`) | ข้าม raw SQL ของ task ที่ manifest เป็น `placeholder: true` — SQL นั้นไม่ถูกรัน จึงไม่ต้องมี DDL · คู่กับ waiver W1 ใน GATES.md · เสนอ /kit-backport |
| K2 | `scripts/runpack/gen_preflight_pack.py` บรรทัด 129 (ยังไม่แก้ script) | README ของ rp00 พิมพ์ `{res_dir.as_posix()}` ออกมาตรง ๆ (ขาด f-string) · แก้มือใน README ของ pack · P5 ขาด `partitionOverwriteMode` / `version()` → agent เติมใน pack |
| K1 | `scripts/pipeline/convert_sql.py` (ยังไม่แก้ script) | concat_policy=spark_null ห่อ `concat(CASE ... ELSE '' END, ...)` ด้วย `IS NULL` check → ใน Oracle `''`=NULL ทำให้ผลเป็น NULL ทุกครั้งที่มี arg = '' (ผิด) · แก้มือใน converted 040000 · ควรแก้ converter: ข้าม wrapper เมื่อ arg ทุกตัวมี ELSE ''/COALESCE → เสนอ /kit-backport |

## 7. ไฟล์อ้างอิง

- `CLAUDE.md` — กฎของโปรเจกต์สำหรับ Claude Code
- `config/config.json` — config pipeline
- `status/PREFLIGHT_CHECKLIST.md` — gate ก่อน Phase 1 (อัปเดตด้วย `setup_migrate.ps1 -Mode InPlace`)
