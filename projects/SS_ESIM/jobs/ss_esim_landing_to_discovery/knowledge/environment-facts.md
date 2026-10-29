# Environment facts — SS_ESIM_L2D

กรอกเฉพาะ**ข้อเท็จจริงที่มีหลักฐาน** (ไฟล์ผลใน `input/run_results/`, screenshot, คำยืนยันของทีม) — สมมติฐานให้เขียนใน OPEN_DECISIONS

| หัวข้อ | Dev | SIT | Prod | แหล่งที่มา |
|---|---|---|---|---|
| Oracle version | **21c Express Edition (21.0.0.0.0) — ไม่ใช่ 19c** → re-test บน 19c ก่อน cutover (G6.M1) | | | P1 · rp00_preflight_20261028 (2026-10-29) |
| schema เจ้าของตาราง / user ที่ ODI connect (DSSDEV) | DSSDEV / DSSDEV (IS_WORK_USER = YES จาก DBeaver — Topology ของ ODI ยังไม่ได้ยืนยัน) · สิทธิ์: role DBA, CREATE TABLE/PROCEDURE, DROP ANY TABLE, quota USERS unlimited | | | P1, P2 · rp00_preflight_20261028 (2026-10-29) |
| ODI version / work repo / schema ของ `SNP_*` | 14.1.2 / work repo id 11 / work repo = **SYSTEM** (SNP_SESSION) · master repo = DSSDEV | | | P4 · rp00_preflight_20261028 (2026-10-29) |
| logical schema / context | DSS_ODI_LOG / DEV | | | |
| DB timezone (`DBTIMEZONE`, `SYSTIMESTAMP`) | DBTIMEZONE +00:00 · SESSIONTIMEZONE Asia/Bangkok · SYSDATE = 2026-10-29 09:04:21 (เวลาไทย = OS ของ DB server) | | | P1 · rp00_preflight_20261028 (2026-10-29) |
| NLS (`NLS_DATE_FORMAT`, `NLS_TIMESTAMP_FORMAT`) | DD-MON-RR · DD-MON-RR HH.MI.SSXFF AM · charset AL32UTF8 · LENGTH_SEMANTICS BYTE · NLS_SORT/COMP BINARY | | | P1 · rp00_preflight_20261028 (2026-10-29) |
| ชนิดคอลัมน์ landing `tb_landing_ss_esim` (`all_tab_columns`) | ทุกคอลัมน์ business = VARCHAR2 (first_installed VARCHAR2(100)) · PROCESS_DATE TIMESTAMP(6) · PARTITION_* NUMBER(19) · source 10/11 object มีจริง — ขาด `EXT_DSS_CHECKPOINT_TB_TRANSACTION_SS_ESIM_VALID` (ใช้เฉพาะ 999999 placeholder) · ตรงกับไฟล์คอลัมน์กลาง 184/184 | | | P3 · rp00_preflight_20261028 (2026-10-29) |
| Spark version / ansi / timeParserPolicy / escapedStringLiterals (Blendata) | 3.3.2 / false / LEGACY / **true** (แต่ regex test ทำงานแบบ backslash เดียว) · session.timeZone UTC · storeAssignmentPolicy LEGACY · sizeOfNull true · partitionOverwriteMode **DYNAMIC** | | | P5.csv + P5b.csv · rp00_preflight_20261028 (2026-10-29) |
| Airflow schedule + timezone ของ DAG | | | | |
