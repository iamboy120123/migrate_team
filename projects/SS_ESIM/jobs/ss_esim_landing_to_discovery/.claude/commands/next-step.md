---
description: อ่านสถานะล่าสุดแล้วทำ step ถัดไปของ migration
---
1. อ่าน `status/PREFLIGHT_CHECKLIST.md` (gate Phase 0), `status/MIGRATION_STATUS.md` (หัวข้อ "ยังค้าง" และ "ผล Run Pack") และ `status/OPEN_DECISIONS.md`
2. ถ้ามี `input/run_results/<pack>/` ที่ใหม่กว่า `run_packs/<pack>/REPORT.md` → รัน `python scripts/runpack/read_run_results.py --pack <pack ล่าสุด>` ก่อน แล้วอ่าน `REPORT.md`
3. เลือก step ถัดไปที่ **ไม่ติด human-decide** แล้วลงมือทำ (regenerate / validate / สร้าง Run Pack / แก้ SQL ตาม flag)
   - ก่อนข้ามช่วงงาน (เช่น สร้าง Run Pack = G3, ไป Pre-Prod = G5) ต้องรัน `/gate G<n>` — BLOCKED = ห้ามข้าม เว้นแต่มี waiver ที่ SA อนุมัติ
4. ถ้าติดการตัดสินใจ → เขียนคำถามแบบมีตัวเลือกลง `status/OPEN_DECISIONS.md` แล้ว **ถาม SA ในแชตเลย** (ยกคำถาม+ตัวเลือกมาแสดง ทีละข้อ ไม่ให้ไปเปิดไฟล์อ่านเอง) เมื่อตอบแล้ว agent บันทึกลงไฟล์เอง แทนการเดา
5. ถ้าต้องให้คนรันบน Oracle/ODI/Blendata → สร้าง Run Pack และบอกลำดับขั้นให้คนทำ (มีเลขกำกับ)
6. จบด้วย `/update-status` แล้วสรุปสั้น ๆ: ทำอะไรไป, ผล, คนต้องทำอะไรต่อ
7. ลำดับขั้นของงานยึด `knowledge/WORKFLOW.md` (คู่มือใน knowledge/ เป็นแกน + BR / Gap / Decision / Status) — เลือกขั้นถัดไปจากขั้นแรกในตารางที่ยังไม่ผ่าน gate

$ARGUMENTS
