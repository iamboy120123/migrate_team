-- P5 Spark config (2026-10-28T15:26:53) - run on Blendata SQL editor / spark-sql (NOT Oracle)
-- SET <key> only displays the current value in Spark; screenshot or export each result into input/run_results/<this pack name>/
SET spark.sql.ansi.enabled;
SET spark.sql.legacy.timeParserPolicy;
SET spark.sql.parser.escapedStringLiterals;
SET spark.sql.session.timeZone;
SET spark.sql.storeAssignmentPolicy;
SET spark.sql.legacy.sizeOfNull;
-- added by agent 2026-10-28 (Q3 needs these too; I14 truncate_all for 020000/040000 depends on partitionOverwriteMode)
SET spark.sql.sources.partitionOverwriteMode;
SELECT version();
-- regex test (escapedStringLiterals): file_date extraction used by task 040000 - expect 14-digit value per row
SELECT input_source_name,
       replace(regexp_extract(reverse(split(input_source_name,'/'))[0],'(.+)([_])(\\d{8}[_]\\d{6})([_])(.+[.].+)',3),'_','') AS file_date
FROM tb_landing_ss_esim LIMIT 5;
-- regex test 2: type_error cleanup used by task 040000 - expect 'first_installed|'
SELECT regexp_replace('first_installed: Invalid TIMESTAMP type (Raw=abc)|',': Invalid [A-Z]+ type \\(Raw=[\\S]*\\)','') AS type_error_test;
