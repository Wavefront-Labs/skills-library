---
id: computing-software.cloud-infrastructure-engineering.aws.redshift-query-monitoring-rules-and-advisor
name: redshift-query-monitoring-rules-and-advisor
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, redshift, query-monitoring-rules, redshift-advisor, wlm, performance-tuning]
level: advanced
status: docs-checked
description: "Guard Redshift with WLM query monitoring rules (log, hop, abort runaway queries) and act on Redshift Advisor recommendations for keys, compression and maintenance."
sources: ["https://docs.aws.amazon.com/redshift/latest/dg/cm-c-wlm-query-monitoring-rules.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/workload-mgmt-config.html", "https://docs.aws.amazon.com/redshift/latest/dg/advisor.html", "https://docs.aws.amazon.com/redshift/latest/dg/advisor-recommendations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query monitoring rules and Redshift Advisor

## 1. Query monitoring rules (QMR)
Defined per WLM queue inside `wlm_json_configuration` (the console can generate the JSON for you):
```json
[{"query_group":[],"user_group":["analysts"],"auto_wlm":true,"queue_type":"auto","priority":"normal",
  "rules":[
   {"rule_name":"abort_long_scans","predicate":[
      {"metric_name":"query_execution_time","operator":">","value":1800},
      {"metric_name":"scan_row_count","operator":">","value":1000000000}],"action":"abort"},
   {"rule_name":"log_nested_loops","predicate":[
      {"metric_name":"nested_loop_join_row_count","operator":">","value":100000000}],"action":"log"},
   {"rule_name":"spill","predicate":[
      {"metric_name":"query_temp_blocks_to_disk","operator":">","value":100000}],"action":"change_query_priority","value":"low"}]},
 {"short_query_queue":true}]
```
```bash
aws redshift modify-cluster-parameter-group --parameter-group-name dw-params \
  --parameters ParameterName=wlm_json_configuration,ParameterValue="$(jq -c . wlm.json)"
```
- Limits: up to 25 rules per queue and 25 across all queues; up to three predicates per rule; operators `=`, `<`, `>`;
  rule names up to 32 alphanumeric characters or underscores, unique within the configuration; the whole
  `wlm_json_configuration` value is at most 8,000 characters. WLM evaluates metrics every 10 seconds.
- Actions, in ascending severity: `log`, `hop` (manual WLM only), `abort`, `change_query_priority` (automatic WLM
  only). If several rules fire, the most severe action wins. `hop` is ignored with a `query_queue_time` predicate.
  QMR does not stop `COPY` or maintenance statements such as `ALTER`, `ANALYZE` and `VACUUM`.
- Metric names include `query_execution_time` (seconds, 0-86,399), `query_cpu_time`, `query_blocks_read`,
  `scan_row_count`, `return_row_count`, `join_row_count`, `nested_loop_join_row_count`,
  `query_temp_blocks_to_disk` (1 MB blocks), `cpu_skew`, `io_skew`, `segment_execution_time`, `query_priority`.
  Add `segment_execution_time > 10` to rules on skew or CPU-percent metrics to avoid sampling errors. Use
  `SVL_QUERY_METRICS_SUMMARY` to choose thresholds.
- Hits are written to `STL_WLM_RULE_ACTION`:
```sql
SELECT userid, query, rule, action, recordtime FROM stl_wlm_rule_action ORDER BY recordtime DESC LIMIT 50;
```
- Start rules with `log`, review a week, then `abort`. AWS recommends a rule over the WLM `max_execution_time`
  timeout for limiting runtime.
- Serverless: queues and rules are also set through `wlm_json_configuration`, with its own metric set
  (for example `max_query_execution_time`, `max_scan_row_count`); see the Serverless metrics table.

## 2. Redshift Advisor
```bash
aws redshift list-recommendations --cluster-identifier dw
```
The call also accepts `--namespace-arn` for Serverless; each recommendation carries `ImpactRanking` of `HIGH`, `MEDIUM`
or `LOW`. Documented recommendation topics: compress S3 files loaded by `COPY`, isolate multiple active databases,
reallocate WLM memory (reduce unused slots), skip compression analysis during `COPY` (`ENCODE` on tables or
`COMPUPDATE OFF`), split S3 objects loaded by `COPY` (a multiple of the slice count), update table statistics
(`ANALYZE`), enable short query acceleration, alter distribution keys, alter sort keys (add `COMPOUND` or convert
`INTERLEAVED`), alter compression encodings, and data type changes. Advisor's `ALTER TABLE` statements consume
resources and take table locks, so run each recommendation group when load is light. Advisor gives no
recommendation when there is not enough data or the benefit is small. Advisor is available only in listed Regions;
check the Advisor page for the current list.
Measure with `SVL_QUERY_SUMMARY` or `SYS_QUERY_HISTORY` before and after.

## Verify
- [ ] Runaway query test is aborted by the rule and logged; Advisor list reviewed monthly with owners.

## Checked
Date: 2026-10-27. Documentation release: Amazon Redshift Database Developer Guide and Management Guide (latest),
botocore redshift 2012-12-01 model. Confirmed: rule and predicate limits, rule-name rules, operators, action list and
engine restrictions, metric names and ranges, `STL_WLM_RULE_ACTION`, the 8,000-character parameter limit, JSON
property names including `change_query_priority` with `value`, `list-recommendations` parameters and
`ImpactRanking` values, and the Advisor recommendation topics. Removed `ALTER DISTSTYLE AUTO` and `SORTKEY AUTO`
as Advisor outputs (the documented statements are explicit `DISTKEY` and `COMPOUND` sort key changes), and the
unconfirmed "skipped `VACUUM`" recommendation and "workgroup query limits" wording.
Method: documentation only; no commands were run.
