---
description: Phase 7 — generate query เทียบผล L1 / L2 / L3 (Spark vs Oracle) แล้วสร้างรอบให้คนรันทั้งสองฝั่ง
---
1. ต้องผ่าน G5 auto ส่วน assertions (หรือ SA สั่งให้ทำคู่ขนาน) — `python scripts/checks/check_gate.py G5 --no-verify` แล้วบอกข้อที่ยังขาด
2. `python scripts/runpack/gen_validation.py` → `output/validation/` (L1 row count, L2 column profile / row hash, L3 business rules)
3. ตรวจ query คู่ก่อนส่ง: หน้าต่างข้อมูลเดียวกันทั้งสองฝั่ง (partition / process date), normalize NULL → `''`, format ของ DATE/TIMESTAMP/NUMBER ตรงกันทุกคอลัมน์ (อ่าน docstring ของ `gen_validation.py`)
4. สร้าง Run Pack (`/run-pack`) ที่มีไฟล์ `*_spark.sql` (Blendata) และ `*_oracle.sql` (Oracle Dev) — บอกคนรันเป็นขั้นตอนมีเลขกำกับ: ที่รัน, ไฟล์, ชื่อผลที่ export
5. หลังได้ผล: `/read-results` แล้วเทียบ L1 → L2 → L3 ตามลำดับ — **L1/L2 ไม่ตรง = หยุดหาสาเหตุ** (`/diagnose`) ห้ามปรับ threshold
6. ส่วนต่างที่อธิบายได้ต้องมี Q ที่ SA ปิดแล้ว · ผลตรงครบ → เสนอ SA ติ๊ก G5.M3
