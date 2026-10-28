---
description: Phase 6 — generate DDL + DBA prerequisite แล้วให้ ddl-dba-reviewer ตรวจก่อนส่ง DBA
---
1. ต้องมี `output/dml/_manifest.json` (ผ่าน `/gen-export` แล้ว) — ไม่มีให้หยุดและบอกขั้นตอน
2. ถ้ามี `input/run_results/profile_result.csv` (ผลรัน `output/ddl/03_profile_source_lengths.sql` ฝั่ง Blendata) จะใช้ความยาวจริง — ไม่มีให้บอก SA ว่าความยาวยังเป็น DRAFT
3. `python scripts/pipeline/gen_ddl.py && python scripts/pipeline/gen_dba_prereq.py`
4. `python scripts/checks/verify_all.py --level V3,V6` แล้วสรุป: fallback กี่คอลัมน์, target/คอลัมน์ที่ DDL ขาด, data contract
5. ใช้ subagent `ddl-dba-reviewer` — ข้อ FIX: แก้ที่ต้นทาง (`config/config.json` → `profile.*` ต้องบอก SA ว่าแก้ field ไหน / converted SQL) แล้ววนข้อ 3; ข้อ DECIDE → `/decide`
6. ถ้า DDL ยังไม่มีใน Dev: เสนอ Run Pack (`/run-pack`) ที่มี `S2a_create_tables_DRAFT.sql` (Execute Script Alt+X) + `output/dba/*.sql` ให้ DBA
7. บอก SA เป็นขั้นตอนมีเลขกำกับ: ไฟล์ที่ส่ง DBA, ลำดับรัน, สิ่งที่ต้องยืนยัน (G6.M2–M4) แล้ว `/update-status`
