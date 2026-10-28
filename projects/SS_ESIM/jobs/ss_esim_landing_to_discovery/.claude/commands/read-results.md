---
description: อ่านผล Run Pack ใน input/run_results/<pack>/ แล้ววิเคราะห์ + บอก step ถัดไป
argument-hint: "[run_packs/<pack>]"
---
1. pack = $ARGUMENTS (ถ้าว่าง = โฟลเดอร์ล่าสุดใน `run_packs/`)
2. `python scripts/runpack/read_run_results.py --pack <pack>` แล้วอ่าน `run_packs/<pack>/REPORT.md` และ CSV ที่เกี่ยวข้อง
3. screenshot (`*.png`) ให้เปิดดูด้วย Read
4. ใช้ subagent `run-result-analyst` วิเคราะห์สาเหตุ (ถ้า ❌) แยก "ข้อเท็จจริงจากผล" กับ "สมมติฐาน" — ถ้าแยกสมมติฐานไม่ได้ ให้เพิ่มสคริปต์ diagnose ใน pack
5. ORA error ที่ reader ไม่รู้จัก = ห้ามเดาแก้
6. สรุปผลเป็นตาราง step/ผล แล้ว `/update-status`
