# INTAKE — คำถาม I1–I17 (ตาม knowledge/reference/intake-questions.md) — SS_ESIM_L2D

Updated: 2026-10-28 · สร้างโดย `setup_migrate.ps1` จาก `config/config.json` · ใช้กับ `/intake` · ข้อเหล่านี้ใช้ตัว `I` เพื่อไม่ชนกับ Q ของ `status/OPEN_DECISIONS.md` · รายละเอียดต่อข้อ: `knowledge/reference/intake-questions.md`

- ver 6: I1, I2, I5, I9, I11, I17 ตอบจากไฟล์ / ค่าเริ่มต้นแล้ว (ไม่ถาม) · I4, I7, I8, I13, I14, I16 ถามเป็นคำยืนยันครั้งเดียว · ตารางที่ตัด/ลด: knowledge/reference/intake-questions.md หัวข้อ "ver 6"
- ✅ = มีคำตอบพร้อมแหล่งที่มา · ⬜ = ต้องถาม SA (ทีละข้อ ตามกฎการถามใน intake-questions.md) · ⚠️ = ตอบแล้วแต่มีเงื่อนไขค้าง
- คำตอบที่มาจาก config = ค่าที่ตั้งตอน setup — SA ยืนยันอีกครั้งตอน `/intake`

| # | หัวข้อ | คำตอบ | แหล่งที่มา | สถานะ |
|---|---|---|---|---|
| I1 | โฟลเดอร์งาน Blendata ต้นทาง | `input/blendata/export_workflow.json` | config `paths.input_export_workflow` | ✅ |
| I2 | ไฟล์ reference SmartExport จาก repository ปลายทาง | `input/odi_reference/_shared_smart_export_DEV_20261028.xml` | config `odi.*`, `input/odi_reference/` | ✅ |
| I3 | โครงสร้างคอลัมน์ตารางปลายทาง (DDL) | `input/oracle_ddl/_shared_all_tab_columns.csv` | `input/oracle_ddl/`, rp00 P3 | ✅ |
| I4 | Oracle schema และวิธี qualify | schema / user / prefix อ่านจาก Smart Export แล้ว: `DSSDEV` / `dssdev.` · วิธี qualify = `schema_mode = odiref` (Q8 A) | config `odi.*` (จาก Smart Export) + Q8 | ✅ SA 2026-10-28 @mana-ma |
| I5 | ODI ProjectName | SS_ESIM_L2D | config `odi.project_name` | ✅ |
| I6 | ProjectCode / prefix เดิมที่ต้อง rename | SS_ESIM_L2D | config `odi.project_code` | ✅ |
| I7 | FolderName | SS_ESIM_L2D | config `odi.folder_name` | ✅ |
| I8 | PackageName | PKG_SS_ESIM_L2D | config `odi.package_name` | ✅ |
| I9 | path ไฟล์ปลายทาง | output/odi_export/PROJ_EXPORT.xml | builder md15 (build_odi_export.py) | ✅ |
| I10 | ความพร้อมของ SQL | (1) ต้นทาง = Spark SQL ฝังใน DAG JSON → แปลงแล้ว 10 ไฟล์ `output/sql/converted/` (2) **ยังไม่เคยรันกับ Oracle** — ยืนยันตอนทดสอบ 05.3 (3) ที่อยู่ = export JSON (4) อักขระนอก latin-1: ไม่มีใน step (validator V6 ผ่าน) (5) DDL ปลายทาง: ตารางจริงครบใน DSSDEV (P3) ยกเว้น ext checkpoint ของ 999999 (W1) (6) Oracle 21c XE / SYSDATE เวลาไทย → Q14 | `/convert`, REVIEW_FLAGS 11/11, SQL_REVIEW ⛔0, P1, P3 | ✅ (ข้อเท็จจริงจากไฟล์) |
| I11 | สถาปัตยกรรม Procedure / Mapping / ผสม | Procedure 1 task = 1 procedure (ADR-001) — task ต่าง technology พิจารณา Mapping แยก | ADR-001 | ✅ |
| I12 | ทาสก์ที่ implement ตรง ๆ ไม่ได้ | 3 task (000000 recover · 080000 retention · 999999 export MSSQL) — คำตอบต่อ task ดูหัวข้อ "I12 — คำตอบต่อ task" | config `scope.excluded_tasks` (+ Q ใน OPEN_DECISIONS) | ✅ SA 2026-10-28 @mana-ma |
| I13 | ลำดับ step chain | 000000→010000→020000→030000→040000→050100→050200→050300→070000→080000→090000→999999 (V5) · ต่างจาก DAG: 050x00 ขนาน→ต่อกัน (ผลเท่ากัน) · DAG 090000 รอ 080000+999999 แต่ ODI 999999 อยู่หลัง 090000 — ไม่มีผลเพราะ 999999 = placeholder · open item: ย้าย 999999 ก่อน 090000 เมื่อ implement export จริง | V5 validate_odi_xml + DAG parentTask | ✅ SA 2026-10-29 @mana-ma |
| I14 | overwrite / append / upsert + column list | load strategy `smart` · partition: `config/partitions_check.csv` | config, D-R7 | ✅ SA 2026-10-28 @mana-ma — 020000 truncate_all (Q9) · 040000 truncate_all (Q10) · 070000 delete_by_partition (Q11) · 010000/030000/090000 partition ว่าง = TRUNCATE+INSERT · 050x00 Append |
| I15 | step สถานะ (success / running / checkpoint) | As-Is: 010000 / 030000 / 090000 ตาม SQL เดิม · ตาราง control `tb_staging_ss_esim_landing_to_discovery_workflow_status` (RUNNING/SUCCESS VARCHAR2(5), WORKFLOW_PROCESS_DATE VARCHAR2(14)) มีแล้วใน DSSDEV · ไม่เพิ่ม logic | raw SQL + all_tab_columns | ✅ SA 2026-10-28 @mana-ma |
| I16 | สภาพ repository ปลายทาง | ODI 14.1.2 · work repo schema `?` · context `DEV` · logical schema `DSS_ODI_LOG` · variables: v_max_partition, v_lag_minutes | config `odi.*`, rp00 P4 | ✅ SA 2026-10-28 @mana-ma — repo เดียวกับที่ export reference (ODI_DEV ของทีม) |
| I17 | รูปแบบ output | Smart Import XML จาก kit + เอกสารส่งมอบ (`HANDOVER.md`, table inventory) | setup_migrate.ps1 (generator = kit) | ✅ |

## I12 — คำตอบต่อ task

DAG 12 task = แปลงตรงได้ 9 + แปลงตรงไม่ได้ 3 (reconcile แล้ว) · ทุก task ต้องอยู่ใน step chain

| task | เหตุผลที่แปลงตรงไม่ได้ | ทางเลือก | สถานะ |
|---|---|---|---|
| `000000_recover_landing_ss_esim` | `service-job-recover` ไม่มี SQL (config: tableName=tb_landing_ss_esim) | 1) placeholder no-op + embed config เดิมใน comment · open item รอข้อมูลเพิ่ม | [X] ✅ SA 2026-10-28 @mana-ma |
| `080000_cleanup_ss_esim_raw_temp` | `service-job-table-retention` ไม่มี SQL (config: tableName=tb_staging_ss_esim_raw_temp, olderThan=-1) | 1) placeholder no-op + embed config เดิมใน comment · open item รอข้อมูลเพิ่ม (ความหมาย olderThan=-1 ยังไม่ทราบ) | [X] ✅ SA 2026-10-28 @mana-ma |
| `999999_export_data_to_mssql` | ปลายทาง SQL Server (JDBC) ไม่มี connection ใน Topology ของ Smart Export DEV · อ่าน `ext_dss_checkpoint_tb_transaction_ss_esim_valid` | 1) placeholder no-op + embed SQL/config เดิม (redact credential) ใน comment · open item รอ connection SQL Server · ผลกระทบ: ข้อมูล valid ไม่ถูกส่งไป SQL Server อัตโนมัติ | [X] ✅ SA 2026-10-28 @mana-ma |
