# PHASE4 REVIEW LOG — ss_esim_landing_to_discovery (Blendata → ODI)

Updated: 2026-10-28 · บันทึกผล Phase 4 (`/review-sql` → `sql-reviewer` → `semantic-verifier`) ต่อ task
ใช้โดย: gate **G2** (`verify_all.py` V4 — ทุก task ใน `status/REVIEW_FLAGS.md` ต้องมีแถวที่นี่ และไม่มีสถานะ `OPEN`) · G2.M1 (SA ตรวจไฟล์นี้)

## วิธีบันทึก

- 1 แถว = 1 ประเด็น ของ 1 task · คอลัมน์แรก = task id ตรงกับ `status/REVIEW_FLAGS.md` · **คอลัมน์สุดท้าย = สถานะ**
- สถานะ: `OPEN` (ยังไม่จบ) · `FIXED` (แก้ใน converted แล้ว, semantics เท่าเดิม) · `ACCEPTED` (ต่างจาก Spark แต่มี Q/ADR ที่ SA ปิดแล้ว) · `NO_CHANGE` (ตรวจแล้วไม่ต้องแก้)
- เปลี่ยน semantics = `ใช่` → ต้องมี Q ใน `status/OPEN_DECISIONS.md` (ปิดโดย SA) หรือ ADR ก่อนเป็น `ACCEPTED` — agent ห้ามตัดสินเอง
- semantic-verifier: `PASS` (หา counter-example ไม่ได้) · `FAIL <case>` · `-` (ยังไม่รัน)

## Spark config ที่ใช้ตีความ (Q3)

| config | ค่า (Blendata) | แหล่งที่มา |
|---|---|---|
| `spark.sql.ansi.enabled` | `false` | input/run_results/rp00_preflight_20261028/P5.csv (ทีม Blendata, 2026-10-29) |
| `spark.sql.legacy.timeParserPolicy` | `LEGACY` | input/run_results/rp00_preflight_20261028/P5.csv (ทีม Blendata, 2026-10-29) |
| `spark.sql.parser.escapedStringLiterals` | `true` | input/run_results/rp00_preflight_20261028/P5.csv (ทีม Blendata, 2026-10-29) |
| `spark.sql.session.timeZone` | `UTC` | input/run_results/rp00_preflight_20261028/P5.csv (ทีม Blendata, 2026-10-29) |
| `spark.sql.storeAssignmentPolicy` | `LEGACY` | input/run_results/rp00_preflight_20261028/P5.csv (ทีม Blendata, 2026-10-29) |
| `spark.sql.legacy.sizeOfNull` | `true` | input/run_results/rp00_preflight_20261028/P5.csv (ทีม Blendata, 2026-10-29) |
| `spark.sql.sources.partitionOverwriteMode` | `DYNAMIC` | P5b.csv (2026-10-29) |
| `version()` | `3.3.2` | P5b.csv (2026-10-29) |
| regex test file_date / type_error | **match ปกติ** — file_date = 14 หลักทั้ง 5 แถว · type_error_test = `first_installed\|` → regex ของ Blendata ทำงานแบบ backslash เดียว (แม้ escapedStringLiterals=true) = ตรงกับ converted 040000 | P5b.csv (2026-10-29) |

## บันทึกต่อ task

| Task | ประเด็น / flag | ผลตรวจ (sql-reviewer) | การแก้ใน converted | เปลี่ยน semantics? | semantic-verifier | Q / ADR | สถานะ |
|---|---|---|---|---|---|---|---|
| task_1b899dbbbe54449d8218e58bed2a044f_030000_running_ss_esim_landing_to_discovery_workflow_status | BOOLEAN literal | Oracle 19c ไม่มี BOOLEAN ใน SQL · คอลัมน์จริง VARCHAR2 | `true as running` → `'TRUE' as running` | ไม่ | - | Q12 | FIXED |
| task_6660be16ef9e43bfbcc8974256bb27f6_090000_success_ss_esim_landing_to_discovery_workflow_status | BOOLEAN literal | Oracle 19c ไม่มี BOOLEAN ใน SQL · คอลัมน์จริง VARCHAR2 | `true as success` → `'TRUE' as success` | ไม่ | - | Q12 | FIXED |
| task_6451c19231b14139ab3d99b35ac9c734_020000_overwrite_ss_esim_checkpoint_temp | BOOLEAN literal | Oracle 19c ไม่มี BOOLEAN ใน SQL · คอลัมน์จริง VARCHAR2 | `TRUE = COALESCE(success, TRUE)` → `'TRUE' = COALESCE(success, 'TRUE')` · ข้อสังเกต As-Is: success NULL (รอบก่อนล้ม) → ยังรันต่อ = guard ไม่กันรอบที่ล้ม → รายงาน SA | ไม่ | - | Q12 | FIXED |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | concat spark_null ผิดกับ `''` (K1) | converter ห่อ `concat(CASE..ELSE '' END,...)` ด้วย spark_null → ใน Oracle `''` = NULL → ถ้าคอลัมน์ใดไม่ NULL ทั้งก้อนเป็น NULL → filter_error / mapping_error = NULL ผิด (MAN/UNMAP หาย) | ถอด wrapper ของ `filter_error`, `mapping_error` เหลือ `a || b || ...` (Spark arg ไม่มีวัน NULL เพราะ ELSE '') · type_error: ถอด `CASE WHEN coalesce(fi,'') IS NULL` → `'...(Raw=' || first_installed || ')|'` (Spark ได้ `(Raw=)|` เมื่อ NULL) | ไม่ (คืน semantics ของ Spark) | - | K1 · concat_policy | FIXED |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] TO_DATE format mask | `to_date(raw.first_installed)` — first_installed เป็น TIMESTAMP แล้ว (to_timestamp ชั้นใน) · Spark to_date(ts) = ตัดเวลา | `TRUNC(raw_.first_installed)` ทั้ง 2 จุด (effective_date/expired_date เป็น TIMESTAMP → TRUNC แล้วจาก converter) | ไม่ | - | - | FIXED |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] split/reverse/[0] + regexp_extract | `replace(regexp_extract(reverse(split(input_source_name,'/'))[0], '(.+)([_])(\d{8}[_]\d{6})([_])(.+[.].+)',3),'_','')` | `REPLACE(REGEXP_SUBSTR(REGEXP_SUBSTR(input_source_name,'[^/]+$'),'(.+)(_)([0-9]{8}_[0-9]{6})(_)(.+[.].+)',1,1,'c',3),'_','')` · ไม่ match: Spark '' / Oracle NULL → to_timestamp ได้ NULL เท่ากัน · ต้องยืนยัน escapedStringLiterals (Q3) | ไม่ (รอ Q3) | - | Q3 | FIXED |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] regexp_replace | `regexp_replace(type_error,': Invalid [A-Z]+ type \(Raw=[\S]*\)','')` — `[\S]` ใน Oracle = อักขระ `\` กับ `S` | `REGEXP_REPLACE(type_error, ': Invalid [A-Z]+ type \(Raw=\S*\)', '', 1, 0, 'c')` · 'c' = case-sensitive | ไม่ (รอ Q3) | - | Q3 | FIXED |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | ORDER BY NULL ordering (dedup) | `ROW_NUMBER() OVER (PARTITION BY chk_duplicate,status ORDER BY file_date)` — Spark ASC = NULL/'' ก่อน · Oracle ASC = NULL ท้าย | `ORDER BY file_date NULLS FIRST` · ข้อสังเกต As-Is: dedup ไม่ deterministic เมื่อ file_date เท่ากัน | ไม่ | - | - | FIXED |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | ข้อสังเกต As-Is (ไม่แก้) | b_no: Spark ใช้ partner/sim_type ก่อน nullif → `''` ได้ `_ESIM_x` · Oracle `''`=NULL → b_no NULL — กระทบเฉพาะแถว MAN (filter_error มาก่อน) · process_date: SYSDATE (DATE, เวลา DB) vs now() (timestamp, session TZ) → Q5 · create_by: USER vs get_user() → Q13 (A ✅) | - | - | - | Q13 | NO_CHANGE |
| task_6451c19231b14139ab3d99b35ac9c734_020000_overwrite_ss_esim_checkpoint_temp | WARN check_sql: TO_NUMBER ไม่มี format mask | ข้อความ = ตัวเลข 12 หลักล้วน (YYYYMMDDHH24MI) ไม่มีทศนิยม/ตัวคั่น → NLS ไม่มีผล | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_6451c19231b14139ab3d99b35ac9c734_020000_overwrite_ss_esim_checkpoint_temp | ความเร็ว: DISTINCT | DISTINCT มีใน Spark เดิม — ตัด = เปลี่ยนผล | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | WARN check_sql: UNION datatype check ข้าม | ทั้งสองฝั่ง = chk_duplicate ของ valid/temp เป็น VARCHAR2 (P3) | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | WARN check_sql: TO_CHAR(1) ไม่มี mask (จุดที่ 1) | จำนวนเต็มบวก NLS ไม่เปลี่ยนรูป + LPAD เติมหลัก | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | WARN check_sql: TO_CHAR(ROW_NUMBER()) ไม่มี mask (จุดที่ 1) | จำนวนเต็มบวก NLS ไม่เปลี่ยนรูป + LPAD เติมหลัก | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | WARN check_sql: TO_CHAR(1) ไม่มี mask (จุดที่ 2) | เหมือนข้างบน (ใน guard ของ concat spark_null) | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | WARN check_sql: TO_CHAR(ROW_NUMBER()) ไม่มี mask (จุดที่ 2) | เหมือนข้างบน (ใน guard ของ concat spark_null) | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | ความเร็ว: UNION / CROSS JOIN / DISTINCT | logic เดิมของ Spark: UNION ตัดซ้ำ chk_duplicate · CROSS JOIN ตาราง status 1 แถว · DISTINCT ใน mapping — วัดจริงขั้น 05.3 | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_d60b3f0310094ab3bdbbad1eca43e81e_050100_append_ss_esim_valid | ความเร็ว: CROSS JOIN | join กับ COUNT(*) 1 แถว = guard chk_dup_append ตาม Spark เดิม | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_081c89ad18764c6ebe7fb2f7ed84d433_050200_append_ss_esim_reject | ความเร็ว: CROSS JOIN | join กับ COUNT(*) 1 แถว = guard chk_dup_append ตาม Spark เดิม | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |
| task_17e9202f814842e3b6d91fabe785f479_050300_append_ss_esim_temp | ความเร็ว: CROSS JOIN | join กับ COUNT(*) 1 แถว = guard chk_dup_append ตาม Spark เดิม | ไม่แก้ | ไม่ | - | SQL_REVIEW 🟡 ✅ SA 2026-10-29 @mana-ma | NO_CHANGE |

## ประวัติ

- 2026-10-28: สร้างจาก kit 2.8.1 (2026-10-14)

