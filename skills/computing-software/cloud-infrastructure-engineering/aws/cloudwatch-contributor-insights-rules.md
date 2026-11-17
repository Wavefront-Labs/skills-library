---
id: computing-software.cloud-infrastructure-engineering.aws.cloudwatch-contributor-insights-rules
name: cloudwatch-contributor-insights-rules
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, contributor-insights-rules, contributor-insights, top-n, insight-rule-metric, log-analysis]
level: practitioner
status: docs-checked
description: "Find top talkers with CloudWatch Contributor Insights: rule syntax over JSON and CLF logs, keys and filters, built-in rules, INSIGHT_RULE_METRIC alarms and cost control."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-RuleSyntax.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights-GraphReportData.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudWatch Contributor Insights rules

**Goal:** answer "which IPs / users / keys / endpoints are causing this?" continuously, from
logs, with top-N time series and alarms.

## Rule
```json
{"Schema":{"Name":"CloudWatchLogRule","Version":1},
 "LogGroupNames":["/aws/apigateway/orders-access"],
 "LogFormat":"JSON",
 "Contribution":{"Keys":["$.ip","$.resourcePath"],
   "Filters":[{"Match":"$.status","GreaterThan":499}]},
 "AggregateOn":"Count"}
```
```bash
aws cloudwatch put-insight-rule --rule-name orders-5xx-by-ip --rule-state ENABLED \
  --rule-definition file://rule.json
aws cloudwatch get-insight-rule-report --rule-name orders-5xx-by-ip \
  --start-time 2026-10-18T08:00:00Z --end-time 2026-10-18T09:00:00Z --period 300 --max-contributor-count 10
```
- Up to 4 `Keys`; `AggregateOn: Sum` with `ValueOf: "$.bytes"` for top by volume (`ValueOf` only with `Sum`).
- Up to 4 `Filters`, combined with AND. Operators: `In`, `NotIn`, `StartsWith` (arrays of up to 10 strings), `GreaterThan`, `LessThan`, `EqualTo`, `NotEqualTo` (one number), `IsPresent` (true or false).
- `LogFormat: CLF` addresses fields by position starting at 1 and `Fields` gives them aliases.
- A trailing `*` in a `LogGroupNames` entry matches a name prefix; `LogGroupARNs` (monitoring accounts only) replaces `LogGroupNames`, not both. Wildcards raise cost.
- Field names and values are case-sensitive; numeric values outside -1e9 to 1e9 are skipped.

## Built-in and service rules
- Built-in rules exist for DynamoDB (most accessed and throttled keys) and AWS PrivateLink.
- The console also offers sample rules for log data.

## Alarm on it
Metric math in an alarm:
```
INSIGHT_RULE_METRIC("orders-5xx-by-ip", "UniqueContributors")
INSIGHT_RULE_METRIC("orders-5xx-by-ip", "MaxContributorValue")
```
`metricName` can also be `SampleCount`, `Sum`, `Minimum`, `Maximum` or `Average`. The caller needs `cloudwatch:GetMetricData` and `cloudwatch:GetInsightRuleReport`. Alarm when one IP exceeds N errors in 5 min (likely bot) or unique contributors spike.

## Cost
Charged per rule per month plus per million log events matched. Narrow `LogGroupNames` and use
filters; disable rules used only for investigations (`--rule-state DISABLED`).

## Gotchas
- Rules analyze incoming data in real time; nothing in the docs describes backfill, so test with new events.

## Verify
- [ ] Report shows expected top contributors for a known test (send errors from a test IP).
- [ ] Alarm on MaxContributorValue fires in a test.

## Checked
Checked 2026-10-27 against the live CloudWatch docs (current release) and the botocore cloudwatch 2010-08-01 model.
- Rule syntax page: schema, LogFormat JSON/CLF, 4 keys, ValueOf only with Sum, 4 filters, operator list, array limit of 10, JSON property notation, CLF Fields, case sensitivity, LogGroupNames prefix wildcard, LogGroupARNs.
- Contributor Insights overview: -1e9 to 1e9 numeric range, charge per matched log event; built-in rules page: DynamoDB and PrivateLink.
- Graphing page: INSIGHT_RULE_METRIC metric names and required permissions.
- botocore model: PutInsightRule (RuleName, RuleState, RuleDefinition) and GetInsightRuleReport (Period, MaxContributorCount) match the CLI examples.
- Removed claims no page confirmed: Standard-class-only support, missing-key behaviour, named sample rules.

Method: documentation only; no commands were run.
