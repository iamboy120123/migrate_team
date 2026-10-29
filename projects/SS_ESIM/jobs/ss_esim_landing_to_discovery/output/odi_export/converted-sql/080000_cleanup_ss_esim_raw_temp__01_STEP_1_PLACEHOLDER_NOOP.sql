-- PLACEHOLDER - no data change. Original Blendata task kept for reference:
-- Blendata task : 080000_cleanup_ss_esim_raw_temp (serviceTemplate = service-job-table-retention)
-- Original role  : retention / cleanup of tb_staging_ss_esim_raw_temp after 070000 (no SQL in export)
-- Original config (verbatim body): {"tableName": "tb_staging_ss_esim_raw_temp", "olderThan": -1, "realmId": 3, "zeusId": 3}
-- Why not converted: service-job-table-retention has no SQL; meaning of olderThan=-1 unknown
-- Note          : 040000 uses truncate_all (Q10) so raw_temp holds only the current run
-- SA decision   : I12 option 1 - placeholder, OPEN ITEM waiting for more info (2026-10-28 @mana-ma)
SELECT 'PLACEHOLDER_NOOP' AS placeholder FROM DUAL
