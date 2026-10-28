---
description: สร้าง Run Pack ให้คนรันบน Oracle / ODI / Blendata (courier loop)
argument-hint: "[rpNN]"
---
1. ถ้าไม่ระบุชื่อ → ใช้เลขถัดจาก pack ล่าสุดใน `run_packs/` (rp01, rp02, ...) — ถ้า pack เดิมยังรันไม่ครบให้ใช้ชื่อเดิม
2. `python scripts/checks/check_gate.py G3` ต้อง PASS ก่อน แล้ว `python scripts/runpack/gen_run_pack.py --pack $ARGUMENTS` (S0 gate = validator ต้องผ่าน)
3. บอก SA เป็นลำดับขั้น: ไฟล์ไหน, รันด้วย user อะไร, ใช้ Execute Script (Alt+X) ไหม, export ผลไปที่ `input/run_results/<pack>/`
4. ย้ำ: สคริปต์ที่ insert/delete ข้อมูลทดสอบต้องรันบน Dev เท่านั้น
5. `python scripts/checks/verify_all.py --level V7` ต้องไม่มี FAIL ก่อนส่ง pack ให้คน (SET/SPOOL/'/', หลาย statement ต้องบอก Alt+X)
6. pack ก่อน G0 (ตรวจ environment) ใช้ `/preflight` แทน — pack ชื่อ `rp00_preflight_*` ไม่นับในลำดับ rpNN
