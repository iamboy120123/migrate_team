# Open Decisions — ss_esim_landing_to_discovery (SS_ESIM_L2D)

รวมประเด็นที่ต้องให้ SA / ทีมตัดสินใจ — ตอบโดยใส่ X ในช่อง `[ ]` แล้วบอก Claude Code ให้อัปเดต kit ต่อ
ตัวเลือก **[แนะนำ]** คือคำแนะนำจากการวิเคราะห์ ไม่ใช่ค่าที่ตั้งไว้แล้ว

---

## Phase 0 — Environment & Config

### Q1. Landing retention
landing `tb_staging_ss_esim_landing_to_discovery_workflow_status` เก็บย้อนหลังกี่วัน (กำหนด point of no return ของ rollback)

- [ ] A) ระบุ: ____ วัน
- [ ] B) ยังไม่ทราบ — ต้องถามทีม ingestion

### Q2. Fail-fast เมื่อ landing ค้าง
ต้องการให้ package หยุดเมื่อ lag > 120 นาทีหรือไม่ (ต้องมี Evaluate Variable sample จาก Studio)

- [ ] A) ต้องการ (เดิม [แนะนำ] จากแม่แบบ kit — ถอดออก 2026-10-29: Blendata ไม่มี fail-fast = ไม่ใช่ As-Is)
- [X] B) ไม่ต้อง — รันต่อแม้ landing ค้าง (As-Is) **[แนะนำ]** ✅ SA 2026-10-29 @mana-ma — ถอด `odi.variables` (v_max_partition, v_lag_minutes: SQL อ่าน partition_minute จากตาราง status ซึ่งไม่มีคอลัมน์นี้) ไปเก็บใน `odi.variables_removed_20261029` · fail-fast = งานเสริมรอบถัดไป (ผูก Q6)

### Q3. Spark config ของ Blendata (มีผลต่อความหมายของ SQL)
ข้อเท็จจริง (จากโปรเจกต์ก่อน): ค่าเหล่านี้ทำให้ผลของ SQL เดียวกันต่างกัน — `ansi.enabled` (CAST ที่แปลงไม่ได้ = error แทน NULL), `legacy.timeParserPolicy` (EXCEPTION ทำให้ workflow ล้มทั้งรอบเมื่อเจอวันที่ผิดรูป), `parser.escapedStringLiterals` (false = backslash ใน regex literal ถูกตัด → regex อาจไม่ match)
ขอทีม Blendata รันใน workspace ของ workflow นี้ แล้วกรอก:
- `SELECT version()`: 3.3.2 · `SET spark.sql.ansi.enabled`: false · `SET spark.sql.legacy.timeParserPolicy`: LEGACY · `SET spark.sql.parser.escapedStringLiterals`: true · `SET spark.sql.sources.partitionOverwriteMode`: DYNAMIC · `SET spark.sql.session.timeZone`: UTC · regex_test (ถ้า SQL มี regexp_replace/regexp_extract ที่มี backslash): รัน pattern จริงกับข้อความตัวอย่างบน Blendata แล้วจดผล — ใช้ตัดสินแทนการเดาจาก escapedStringLiterals (E26)
- ได้บางส่วน 2026-10-29 (P5.csv): ansi.enabled=false · timeParserPolicy=LEGACY · escapedStringLiterals=**true** · session.timeZone=**UTC** · storeAssignmentPolicy=LEGACY · sizeOfNull=true · ครบ 2026-10-29 (P5b.csv): partitionOverwriteMode=**DYNAMIC** · version 3.3.2 · regex test A/B match ปกติ
- [X] A) ได้ค่าครบแล้ว (P5.csv + P5b.csv จากทีม Blendata ผ่าน SA) **[แนะนำ — ต้องมีก่อนปิด Phase 4]** ✅ SA 2026-10-29 @mana-ma
- [ ] B) ยังขอไม่ได้ — D1 (PySpark) รันทุกค่าที่เป็นไปได้ และถือว่ากฎถูกเฉพาะเมื่อผลตรงกันทุกแบบ

### Q4. Data contract ของ landing `tb_landing_ss_esim` (แก้ชื่อ 2026-10-29 — เดิมเขียนเป็นตาราง status)
ข้อเท็จจริง: landing ใน Oracle ที่ Spark JDBC สร้างมักมีชนิดต่างจาก Blendata (เช่น timestamp = TIMESTAMP(6), string = VARCHAR2(255), partition = NUMBER(19)) — กฎแปลงขึ้นกับชนิดจริง
- [X] A) ใช้ชนิดตาม `all_tab_columns` ของ Oracle Dev (P3 rp00 2026-10-29: business = VARCHAR2, PROCESS_DATE TIMESTAMP(6), PARTITION_* NUMBER(19)) **[แนะนำ]** ✅ SA 2026-10-29 @mana-ma — เทียบ Prod ก่อน cutover
- [ ] B) กำหนด DDL landing ใหม่เอง (ต้องแจ้งทีมที่เติม landing)
- ผู้เติม landing ใน Prod: ____ (ค้าง — ก่อน cutover)

### Q5. Schedule และ timezone
ข้อเท็จจริง: Airflow ใช้ **UTC** เป็น default ถ้า DAG ไม่กำหนด timezone · SQL มักใช้ `SYSDATE` (เวลาของ DB server)
- cron เดิมของ DAG: ____ · timezone ของ DAG: ____ · `SELECT DBTIMEZONE, SESSIONTIMEZONE, SYSTIMESTAMP FROM dual` (Dev/Prod): ____
- ตัวเลือก schedule ใน ODI:
  - [ ] A) Scenario + ODI Agent schedule + กันรอบซ้อน (Limit Concurrent Executions / guard flag) **[แนะนำ]**
  - [ ] B) Load Plan
  - [ ] C) scheduler ภายนอก (`startscen`) — ระบุ: ____

### Q6. แจ้งเตือนและ recovery
ข้อเท็จจริง: task recover ของ Blendata (ถ้ามี) มักถูก exclude · ODI KO path แจ้งเตือนได้เฉพาะเมื่อ session เริ่มแล้ว (Agent ล่ม = เงียบ)
- ช่องทาง / SMTP: ____ · ผู้รับ WARNING: ____ · ผู้รับ CRITICAL: ____
- [ ] A) OdiSendMail ใน KO path + runbook "Restart session เดิม" + missing-run check จากภายนอก **[แนะนำ]**
- [ ] B) monitoring ภายนอกอ่าน `SNP_SESSION` อย่างเดียว

### Q7. Work repository
ตาราง `SNP_*` อยู่ใน schema ของ work repository (Dev อาจเป็น `SYSTEM`) — ต้องรู้เพื่อ query log ใน Run Pack
- schema ของ work repo (Dev): **SYSTEM** (P4 + P4b_snp_session_owner.csv รันด้วย DSSDEV) · DSSDEV = master repository (SNP_CONNECT/SNP_LSCHEMA/…) · (Prod): ____ (ถาม DBA ก่อน cutover, G6.M4) · user ที่มีสิทธิ์ SELECT (Dev): DSSDEV (role DBA)
- [X] A) กรอกแล้วสำหรับ Dev — `odi.work_repo_schema = SYSTEM` ใน config · Prod ค้าง ✅ SA 2026-10-29 @mana-ma

---

## Workflow (setup_migrate) (2026-10-28)

### Q8. Schema qualification ของตารางใน step SQL (D-R2 ↔ kit odi-step-sql ข้อ 6)
ข้อเท็จจริง: คู่มือบังคับ qualify schema ทุกตาราง (`check_sql.py` D-R2 = ERROR, เคยเกิด ORA-00942 — lessons-learned L25 / เคส 19) · kit ห้าม hardcode schema (V3 ต้อง = 0 ก่อน G6) เพราะ schema ของ Prod อาจต่าง · ผล `check_sql.py` ล่าสุด: `output/verify/sql_check_converted.txt`
ยังไม่รู้: login / owner ของตารางใน SIT และ Prod เป็น user เดียวกันหรือไม่ · ตาราง external / master อยู่ schema เดียวกันหรือไม่
- [X] A) `schema_mode = odiref` ใน config — kit เติม `<%=odiRef.getSchemaName("<logical schema>","D")%>.` หน้าทุกตาราง (SELECT + ตารางปลายทางใน DML, K3) · portable ข้าม environment · ผ่าน D-R2 ไม่ต้อง waiver · ไม่ต้องแก้ generator · Run Pack ต้องแทน tag เป็น schema จริงก่อนรันใน DBeaver **[แนะนำ — ใช้จริงแล้ว SS_PAYMENT_3BB_VDO: Smart Import + Dev run ผ่าน]** ✅ SA 2026-10-28 @mana-ma
- [ ] B) `schema_mode = literal` (ค่าตั้งต้น) — hardcode `target_table_prefix` (เช่น `dssdev.`) · check_sql ผ่าน แต่ V3 FAIL และต้อง build ใหม่เมื่อ Prod ใช้ schema อื่น
- [ ] C) ไม่ qualify (ชื่อตารางเปล่า) — **kit 2.8.x ไม่รองรับ**: `convert_sql.py` / `check_inputs.py` หยุดเมื่อ prefix ว่าง → ต้องแก้ kit (K#) + บังคับ data server login = owner ทุก environment (G4.M2, G6.M4) + waiver D-R2 ใน `status/GATES.md`

---

## I14 — overwrite ต่อ task (DECISION ใน `config/partitions_check.csv`)

ข้อเท็จจริง: Spark sink = `Overwrite` + `partitions: [partition_date]` · ผลจริงขึ้นกับ `spark.sql.sources.partitionOverwriteMode` (Q3 ยังไม่ได้ค่า) · dynamic = ลบเฉพาะ partition ที่เขียน · static (default) = ลบทั้งตาราง

### Q9. `020000_overwrite_ss_esim_checkpoint_temp` → `tb_staging_ss_esim_checkpoint_temp`
- [X] A) delete_by_partition **[แนะนำ — ไม่ลบเกินที่ Spark ลบไม่ว่าโหมดไหน]** ✅ SA 2026-10-29 @mana-ma — ทบทวนหลัง P5b: partitionOverwriteMode = DYNAMIC (GAP-05 = K)
- [ ] B) TRUNCATE PARTITION (ต้องตรวจ DDL ว่าเป็น partitioned table)
- [ ] C) truncate_all (ตรงกับ Spark static) — เดิมเลือก 2026-10-28 · ยกเลิก 2026-10-29 เพราะ Blendata = DYNAMIC

### Q10. `040000_overwrite_ss_esim_raw_temp` → `tb_staging_ss_esim_raw_temp`
ข้อเท็จจริง: 050100/050200/050300 อ่าน raw_temp ทั้งตาราง (ไม่กรอง partition) · chk_dup_append ตรวจเฉพาะ workflow_process_date รอบปัจจุบัน · 080000 retention = placeholder (I12)
- [ ] A) delete_by_partition — แถววันก่อนค้าง → append ซ้ำเข้า valid/reject/temp
- [ ] B) TRUNCATE PARTITION — ผลเหมือน A
- [X] C) truncate_all **[แนะนำ — ตารางมีเฉพาะข้อมูลรอบนี้ เท่ากับผลรวม overwrite + retention ของ Blendata]** ✅ SA 2026-10-28 @mana-ma
- ทบทวน 2026-10-29 หลัง P5b (partitionOverwriteMode = DYNAMIC): คง C + waiver W2 (D-R7) · `PARTITIONS_EMPTY = Y` ใน partitions_check.csv พร้อมเหตุผล · 080000 ยังเป็น placeholder ✅ SA 2026-10-29 @mana-ma

### Q11. `070000_overwrite_ss_esim_checkpoint` → `tb_staging_ss_esim_checkpoint`
ข้อเท็จจริง: ตาราง state ถาวร · 020000/040000 อ่าน MAX(checkpoint_partition) · checkpoint_temp = truncate_all (Q9) → รอบไม่มี landing ใหม่ temp ว่าง
- [X] A) delete_by_partition **[แนะนำ — รอบที่ไม่มีข้อมูลใหม่ไม่ลบอะไร checkpoint ไม่หาย]** ✅ SA 2026-10-28 @mana-ma
- [ ] B) TRUNCATE PARTITION
- [ ] C) truncate_all — รอบไม่มีข้อมูลใหม่ checkpoint = 0 → ประมวลผลซ้ำทั้งหมด

### Q12. Boolean mapping (Spark true/false → Oracle)
ข้อเท็จจริง: RUNNING/SUCCESS ของ workflow_status = VARCHAR2(5) · SUCCESS ของ _temp = VARCHAR2(20) · ใช้ที่ 030000/090000 (เขียน) และ 020000 (เทียบ `'TRUE' = COALESCE(success,'TRUE')`)
- [X] A) `'TRUE'` / `'FALSE'` (ตัวใหญ่) **[แนะนำ — type map kit + ชนิดคอลัมน์จริง · package เขียนและอ่านเอง]** ✅ SA 2026-10-28 @mana-ma
- [ ] B) `'true'` / `'false'`
- [ ] C) `1` / `0` (ต้องแก้ DDL เป็น NUMBER(1))

### Q13. `create_by` (Spark `get_user()`)
ข้อเท็จจริง: Oracle ไม่มี get_user() · converter ใส่ `USER` (= DB user ที่ ODI login, DEV = DSSDEV) · ไหลไป valid / reject / temp และ export MSSQL
- [X] A) `USER` **[แนะนำ — ความหมายใกล้ get_user() ที่สุด ไม่ hardcode]** ✅ SA 2026-10-28 @mana-ma
- [ ] B) ค่าคงที่ที่ทีมกำหนด: ____
- [ ] C) ค่าเดียวกับที่ Blendata เขียนอยู่ (ดูจากข้อมูลจริง): ____

### Q14. เวลาปัจจุบัน: UTC (Blendata `now()`, session.timeZone=UTC) vs `SYSDATE` (Dev = เวลาไทย) — GAP-01
ข้อเท็จจริง: P1 SYSDATE = เวลาไทย (+7) · P5 session.timeZone = UTC · กระทบ workflow_process_date, cdr_id, process_date, partition_date, เงื่อนไข `partition_minute < now()-5 min` (020000), ช่วง 7 วันของ 999999, `v_lag_minutes`
- [ ] A) UTC: `CAST(SYS_EXTRACT_UTC(SYSTIMESTAMP) AS DATE)` แทน SYSDATE ที่มาจาก now() **[แนะนำ — As-Is]**
- [X] B) เวลาไทย (`SYSDATE` ตามที่แปลงไว้) ✅ SA 2026-10-29 @mana-ma — เงื่อนไข: (1) ยืนยันว่าผู้เติม landing ใน Oracle เขียน `partition_minute` เป็นเวลาไทย (2) downstream / SQL Server ยอมรับค่าเวลาที่เลื่อน +7 ชม. (3) ถ้าย้ายข้อมูลย้อนหลัง (UTC) ต้องวางแผนรอยต่อ checkpoint / workflow_process_date ตอน cutover — ทั้ง 3 ข้อเป็น open item ก่อน G5/G6
- [ ] C) ยังไม่ตัดสิน

### Q15. parse วันที่ `first_installed` — Spark LEGACY (ผ่อนปรน) vs Oracle (เข้มงวด) — GAP-02
ข้อเท็จจริง: timeParserPolicy = LEGACY (P5) · Oracle: REGEXP_LIKE 14 หลัก + TO_TIMESTAMP DEFAULT NULL → ค่าผิดรูป (เดือน 13, 13 หลัก) = TYP · ค่าถูกต้องผลเท่ากัน
- [X] A) Accept — ค่าผิดรูปเป็น TYP ใน Oracle · วัดจำนวนแถวที่ต่างใน D2/D3 **[แนะนำ]** ✅ SA 2026-10-29 @mana-ma
- [ ] B) วัดจาก landing จริงก่อนตัดสิน
- [ ] C) เลียนแบบ LEGACY ด้วย function ใหม่ (ต้องอนุมัติสร้าง object)
