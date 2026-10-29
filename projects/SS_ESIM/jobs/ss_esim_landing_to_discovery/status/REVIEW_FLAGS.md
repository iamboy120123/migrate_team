# status/REVIEW_FLAGS.md

Generated: 2026-10-28T15:16:37
AI Mode: `manual`

SQL ที่ถูกแปลงอัตโนมัติแล้วแต่ยังต้องผ่านการตรวจทาน (โดย AI ถ้า auto, โดย SA ถ้า manual)
ก่อนเข้า Phase 5 (gen_dml.py) ทุกแถวต้องมี status = RESOLVED

| Task ID | Reason | Snippet | Status |
|---|---|---|---|
| task_1b899dbbbe54449d8218e58bed2a044f_030000_running_ss_esim_landing_to_discovery_workflow_status | [FLAG] BOOLEAN literal true/false - Oracle 19c ไม่มี BOOLEAN ใน SQL ต้อง map เป็น NUMBER(1) | `true` | RESOLVED (boolean → 'TRUE'/'FALSE' VARCHAR2 · Q12 ✅ SA 2026-10-28 @mana-ma) |
| task_6451c19231b14139ab3d99b35ac9c734_020000_overwrite_ss_esim_checkpoint_temp | [FLAG] BOOLEAN literal true/false - Oracle 19c ไม่มี BOOLEAN ใน SQL ต้อง map เป็น NUMBER(1) | `TRUE` | RESOLVED (boolean → 'TRUE'/'FALSE' VARCHAR2 · Q12 ✅ SA 2026-10-28 @mana-ma) |
| task_6451c19231b14139ab3d99b35ac9c734_020000_overwrite_ss_esim_checkpoint_temp | [FLAG] BOOLEAN literal true/false - Oracle 19c ไม่มี BOOLEAN ใน SQL ต้อง map เป็น NUMBER(1) | `TRUE` | RESOLVED (boolean → 'TRUE'/'FALSE' VARCHAR2 · Q12 ✅ SA 2026-10-28 @mana-ma) |
| task_6660be16ef9e43bfbcc8974256bb27f6_090000_success_ss_esim_landing_to_discovery_workflow_status | [FLAG] BOOLEAN literal true/false - Oracle 19c ไม่มี BOOLEAN ใน SQL ต้อง map เป็น NUMBER(1) | `true` | RESOLVED (boolean → 'TRUE'/'FALSE' VARCHAR2 · Q12 ✅ SA 2026-10-28 @mana-ma) |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] TO_DATE(...) ต้องตรวจ format mask | `to_date(raw_.first_installed)` | RESOLVED (to_date(timestamp) → TRUNC(raw_.first_installed) · PHASE4_REVIEW_LOG) |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] TO_DATE(...) ต้องตรวจ format mask | `to_date(raw_.first_installed)` | RESOLVED (to_date(timestamp) → TRUNC(raw_.first_installed) · PHASE4_REVIEW_LOG) |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] split/reverse/array index ไม่มีใน Oracle ต้องใช้ REGEXP_SUBSTR | `reverse(` | RESOLVED (reverse(split(p,'/'))[0] → REGEXP_SUBSTR(p,'[^/]+$') · PHASE4_REVIEW_LOG) |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] split/reverse/array index ไม่มีใน Oracle ต้องใช้ REGEXP_SUBSTR | `split(` | RESOLVED (reverse(split(p,'/'))[0] → REGEXP_SUBSTR(p,'[^/]+$') · PHASE4_REVIEW_LOG) |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] split/reverse/array index ไม่มีใน Oracle ต้องใช้ REGEXP_SUBSTR | `)[0]` | RESOLVED (reverse(split(p,'/'))[0] → REGEXP_SUBSTR(p,'[^/]+$') · PHASE4_REVIEW_LOG) |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] regexp_extract -> REGEXP_SUBSTR(...,1,1,NULL,n); regexp_replace semantics ต่างกัน | `regexp_replace(type_error,': Invalid [A-Z]+ type \\(Raw=[\\S]*\\)` | RESOLVED (regexp_extract → REGEXP_SUBSTR(...,1,1,'c',3) · regexp_replace → REGEXP_REPLACE(...,1,0,'c') · PHASE4_REVIEW_LOG) |
| task_b045fc16dd1e4272a3a28795693c2291_040000_overwrite_ss_esim_raw_temp | [CRITICAL] regexp_extract -> REGEXP_SUBSTR(...,1,1,NULL,n); regexp_replace semantics ต่างกัน | `regexp_extract(reverse(split(input_source_name,'/')` | RESOLVED (reverse(split(p,'/'))[0] → REGEXP_SUBSTR(p,'[^/]+$') · PHASE4_REVIEW_LOG) |
