---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-logs-insights-query-language
name: cloudwatch-logs-insights-query-language
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch-logs, logs-insights, insights-query, saved-queries, parse-fields, troubleshooting]
level: practitioner
status: docs-checked
description: "Write CloudWatch Logs Insights queries: fields, filter, parse (glob and regex), stats by bin, dedup, Lambda REPORT parsing, cost control by scope, and saved queries via CLI."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax-examples.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_Insights-Saving-Queries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch Logs Insights query language

## 1. Core commands (pipe-separated)
`fields`, `filter`, `parse`, `stats`, `sort`, `limit`, `dedup`, `display`, `unmask`,
`pattern`, `diff`. JSON logs are auto-discovered as fields (`level`, `requestId`, nested
`detail.status`).

```
fields @timestamp, @message, level, requestId
| filter level = "ERROR" and @message like /timeout/
| sort @timestamp desc
| limit 50
```

## 2. Parse unstructured text
Glob:
```
parse @message "user=* action=* latency=*ms" as user, action, latency
| stats avg(latency) as avg_ms, pct(latency, 99) as p99 by action
```
Regex with named groups:
```
parse @message /status=(?<status>\d{3}) path=(?<path>\S+)/
| filter status >= 500
| stats count(*) as errors by path | sort errors desc | limit 20
```

## 3. Time series
```
filter @message like /ERROR/
| stats count(*) as errors by bin(5m)
```
Charts in the console; add to dashboards.

## 4. Lambda REPORT lines
```
filter @type = "REPORT"
| stats max(@maxMemoryUsed / 1000 / 1000) as maxMemMB,
        avg(@duration) as avgMs, pct(@duration, 95) as p95Ms,
        sum(strcontains(@message, "Init Duration")) as coldStarts
  by bin(1h)
```

## 5. Run from the CLI and save
```bash
QID=$(aws logs start-query --log-group-names /aws/lambda/orders --start-time $(date -d '-1 hour' +%s) --end-time $(date +%s) \
  --query-string 'filter level="ERROR" | stats count(*) by bin(5m)' --query queryId --output text)
aws logs get-query-results --query-id $QID
aws logs put-query-definition --name "orders-errors-5m" --log-group-names /aws/lambda/orders \
  --query-string 'filter level="ERROR" | stats count(*) by bin(5m)'
```
Saved queries (query definitions) appear in the console; up to 1,000 can be saved per Region, and in the console slashes in a folder name create nested folders.

## Gotchas
- Billed per GB **scanned**: narrow the time range and log groups first; field indexes and
  `filterIndex` reduce scanned data for indexed fields.
- `GetQueryResults` returns at most 10,000 events per call; the `limit` of `start-query` can go up to 100,000 events, read by paginating (Logs Insights QL only). Queries time out after 60 minutes. `logGroupNames` and `logGroupIdentifiers` accept up to 50 log groups; the `SOURCE` command (CLI and API only) selects many by name prefix, account, class, data source or tag.
- Log groups in the Infrequent Access class do not support `pattern`, `diff`, `unmask` or `filterIndex`.
- `like` accepts a string or a regex such as `like /(?i)error/`; use regex for anchors and case-insensitive matches.

## Verify
- [ ] Saved queries exist for the top runbook questions (errors per 5 min, slowest requests, cold starts).
- [ ] A query run during an incident returns in seconds with a scoped time range.

## Checked
Checked 2026-10-27 against the live CloudWatch Logs docs (current release) and the botocore logs 2014-03-28 model.
- Query syntax page: pipe and comment syntax, command list including pattern, diff, unmask, filterIndex and SOURCE, and the log-class support note.
- StartQuery API reference: 60-minute timeout, 50 log groups, limit up to 100,000 with 10,000 per GetQueryResults call. botocore: start-query and put-query-definition parameters match the CLI examples.
- Functions page: bin(5m), pct, strcontains, like with regex; discovered fields page: Lambda @duration, @type, @maxMemoryUsed, @memorySize.
- Saving queries page: 1,000 saved queries per Region and slash folder structure.
- Removed the claim that slashes in a query name create folders, which the pages only state for folder names.

Method: documentation only; no commands were run.
