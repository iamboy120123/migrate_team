-- P5b (2026-10-29) - run on Blendata SQL editor, SAME workspace as workflow ss_esim_landing_to_discovery (NOT Oracle)
-- Items missing from P5.csv. Read-only. Export or screenshot EVERY result (4 results).
-- 1) decides whether truncate_all (020000 / 040000) matches Blendata
SET spark.sql.sources.partitionOverwriteMode;
-- 2) Spark version
SELECT version();
-- 3) regex test A: file_date extraction exactly as in task 040000 - record the actual value (may be empty)
SELECT input_source_name,
       replace(regexp_extract(reverse(split(input_source_name,'/'))[0],'(.+)([_])(\\d{8}[_]\\d{6})([_])(.+[.].+)',3),'_','') AS file_date
FROM tb_landing_ss_esim LIMIT 5;
-- 4) regex test B: type_error cleanup exactly as in task 040000 - record the actual value
SELECT regexp_replace('first_installed: Invalid TIMESTAMP type (Raw=abc)|',': Invalid [A-Z]+ type \\(Raw=[\\S]*\\)','') AS type_error_test;
