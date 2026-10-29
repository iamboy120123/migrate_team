-- ============================================================
-- ODI Procedure Body: task_0a7791409dbc4c789e892d888f5e1a51_080000_cleanup_ss_esim_raw_temp
-- Target Table      : DSSDEV.TB_STAGING_SS_ESIM_RAW_TEMP
-- Generated         : 2026-10-28T15:26:18 (manual placeholder, I12)
-- Strategy          : placeholder no-op SELECT FROM DUAL (I12 option 1; BEGIN NULL END has no SqlIndGrp in reference)
-- ============================================================

-- @@ODI_STEP: STEP_1_PLACEHOLDER_NOOP
-- PLACEHOLDER - no data change. Original Blendata task kept for reference:
-- Blendata task : 080000_cleanup_ss_esim_raw_temp (serviceTemplate = service-job-table-retention)
-- Original role  : retention / cleanup of tb_staging_ss_esim_raw_temp after 070000 (no SQL in export)
-- Original config (verbatim body): {"tableName": "tb_staging_ss_esim_raw_temp", "olderThan": -1, "realmId": 3, "zeusId": 3}
-- Why not converted: service-job-table-retention has no SQL; meaning of olderThan=-1 unknown
-- Note          : 040000 uses truncate_all (Q10) so raw_temp holds only the current run
-- SA decision   : I12 option 1 - placeholder, OPEN ITEM waiting for more info (2026-10-28 @mana-ma)
SELECT 'PLACEHOLDER_NOOP' AS placeholder FROM DUAL;
