# GAP ANALYSIS — As-Is (Blendata / Spark SQL) ↔ To-Be (ODI / Oracle) — SS_ESIM_L2D

Updated: 2026-10-29 · โครงสร้างโดย `setup_migrate.ps1` · เติมด้วย `/gap-analysis` จาก `status/PHASE4_REVIEW_LOG.md`, `status/OPEN_DECISIONS.md`, `status/BUSINESS_RULES.md`, `knowledge/reference/spark-to-oracle-sql.md`, `knowledge/reference/validation-and-cutover.md`, `knowledge/lessons-learned.md`, `output/verify/sql_check_*.txt`

- Disposition: **K** Keep · **M** Modify (เปลี่ยนวิธี ผลเท่าเดิม) · **A** Accept (ผลต่าง ยอมรับโดย Q) · **R** Remove/Defer
- ผลกระทบ: **H** เปลี่ยนตัวเลข/แถวที่ downstream เห็น · **M** บางคอลัมน์ / ข้อมูลขอบ · **L** ไม่กระทบผลลัพธ์
- ทุกแถวที่ไม่ใช่ K ต้องมี Q/ADR ที่ SA ปิดแล้ว · "ยืนยันด้วย" = หลักฐานที่ต้องมีก่อน G5/G6

## 1. Semantics ของข้อมูล

| GAP | เรื่อง | As-Is (Spark) | To-Be (Oracle) | BR | กระทบ | Disp. | Q / ADR | ยืนยันด้วย | สถานะ |
|---|---|---|---|---|---|---|---|---|---|
| GAP-01 | เวลา `now()` vs `SYSDATE` | session.timeZone = UTC → workflow_process_date, cdr_id, process_date, partition_date, เงื่อนไข `now()-5 min` เป็นเวลา UTC | `SYSDATE` = เวลา OS ของ DB (Dev = เวลาไทย, +7) | - | H | A | Q14 B (✅ SA 2026-10-29) — เวลาไทย | ยืนยัน timezone ของ partition_minute ใน landing Oracle + downstream ยอมรับ + แผนรอยต่อ cutover | ปิด (Accept) — มีเงื่อนไขค้าง |
| GAP-02 | parse วันที่ `to_timestamp(left(first_installed,14),'yyyyMMddHHmmss')` | timeParserPolicy = LEGACY (SimpleDateFormat ผ่อนปรน: เดือน 13 / วันที่ 32 ปัดต่อ ไม่เป็น NULL) | `REGEXP_LIKE` 14 หลัก + `TO_TIMESTAMP ... DEFAULT NULL ON CONVERSION ERROR` เข้มงวด → ค่าผิดรูปเป็น TYP | - | M | A | Q15 A (✅ SA 2026-10-29) | D2/D3 นับแถวที่ Spark ผ่านแต่ Oracle = TYP · D1 PySpark 3.3.2 LEGACY ค่าขอบ | ปิด (Accept) รอยืนยันใน D2 |
| GAP-03 | regex file_date / type_error (escapedStringLiterals=true) | P5b: match ปกติ | REGEXP_SUBSTR / REGEXP_REPLACE match ปกติ | - | L | K | Q3 | P5b.csv regex test A/B | ปิด — ผลเท่ากัน |
| GAP-04 | guard รอบก่อนล้ม `COALESCE(success, TRUE)` | success NULL (รอบล้มกลางทาง) → ยังรันต่อ | เหมือนเดิม (`'TRUE'`) | - | L | K | Q12 | - | ข้อสังเกต As-Is |

## 2. พฤติกรรมของ workflow / การรัน

| GAP | เรื่อง | As-Is | To-Be | BR | กระทบ | Disp. | Q / ADR | ยืนยันด้วย | สถานะ |
|---|---|---|---|---|---|---|---|---|---|
| GAP-05 | overwrite `020000` checkpoint_temp | partitionOverwriteMode = DYNAMIC → แทนเฉพาะ partition วันนี้ · partition วันก่อนสะสม | Q9 = delete_by_partition (DYNAMIC เหมือนเดิม) | - | L | K | Q9 (✅ SA 2026-10-29) | D2 | ปิด — ผลเท่ากัน |
| GAP-06 | overwrite `040000` raw_temp | DYNAMIC → แทนเฉพาะวันนี้ + 080000 retention (`olderThan=-1`) ล้างหลังใช้ | Q10 = truncate_all + 080000 placeholder → มีแค่รอบนี้ | - | M | M | Q10 + W2 (✅ SA 2026-10-29) | D2 จำนวนแถว valid/reject ข้ามวัน | ปิด รอยืนยันใน D2 |

## 3. Scope ของ task

| GAP | Task | As-Is | To-Be | Disp. | Q | สถานะ |
|---|---|---|---|---|---|---|

## 4. Platform / ODI

| GAP | เรื่อง | ข้อเท็จจริง | Disp. | Q | สถานะ |
|---|---|---|---|---|---|

## 5. สรุป

| สถานะ | GAP |
|---|---|
| เปิด — ต้องให้ SA ตัดสิน | |
| เปิด — ต้องมีหลักฐาน/test | |
| ปิดแล้ว รอยืนยันใน D1/D2 | |
| ข้อสังเกต (ผลเท่ากันทั้งสองฝั่ง) | |

## Checklist gap ที่พบบ่อย (ไล่ให้ครบ แล้วลบ/ติ๊กเมื่อบันทึกเป็น GAP หรือยืนยันว่าไม่เกี่ยว)

- [ ] `''` vs NULL (`= ''`, `<> ''`, `nullif(x,'')`, `coalesce(x,'')`, `concat` เมื่อมี NULL)
- [ ] `spark.sql.legacy.timeParserPolicy` (EXCEPTION = ทั้งรอบ error, Oracle = NULL)
- [ ] ค่าวันที่สั้นกว่า pattern (D-R8 / L37) — ต้องมี shape guard หรือ mask `FX` + test แถวสั้นกว่า pattern
- [ ] `spark.sql.parser.escapedStringLiterals` กับ regex / LIKE escape
- [ ] `now()` precision / timezone (`spark.sql.session.timeZone` vs DB)
- [ ] `get_user()` → `USER`
- [ ] boolean → VARCHAR2 / NUMBER
- [ ] overwrite ตาราง partition: ห้าม TRUNCATE ทั้งตารางเอง · ถามเลือกต่อ task (I14: DELETE เฉพาะ partition ใน SELECT / TRUNCATE PARTITION / TRUNCATE ทั้งตารางเมื่อยืนยันว่าว่าง) + ยืนยัน `spark.sql.sources.partitionOverwriteMode` (D-R7 / L29, `config/partitions_check.csv`)
- [ ] status table ที่ schema เปลี่ยนตาม overwrite (guard รอบค้าง)
- [ ] ลำดับไม่แน่นอน (`ROW_NUMBER() over(order by 1)`, tie, `NULLS FIRST`)
- [ ] INNER JOIN กับ master/lookup ที่ทำให้แถวหายเงียบ
- [ ] task non-SQL (recover / retention / export ต่าง technology)
- [ ] ความยาว string (Spark ไม่จำกัด, Oracle VARCHAR2)
- [ ] schema qualification (D-R2 ↔ kit V3)
- [ ] Oracle version ของ Dev ≠ Prod (19c)
- [ ] schedule / timezone ของ DAG และ alert / recovery