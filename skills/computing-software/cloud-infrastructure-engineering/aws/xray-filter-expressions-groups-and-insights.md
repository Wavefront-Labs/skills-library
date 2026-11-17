---
id: computing-software.cloud-infrastructure-engineering.aws.xray-filter-expressions-groups-and-insights
name: xray-filter-expressions-groups-and-insights
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, x-ray, filter-expressions, xray-groups, xray-insights, trace-analysis, annotations]
level: practitioner
status: docs-checked
description: "Find the traces that matter in X-Ray: filter expressions (latency, errors, annotations, service and edge scopes), groups with metrics, and Insights notifications."
sources: ["https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-console-groups.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-console-insights.html", "https://docs.aws.amazon.com/xray/latest/devguide/xray-console-sampling.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Transaction-Search.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X-Ray filter expressions, groups and Insights

## 1. Filter expressions
Used in the console trace search, `get-trace-summaries --filter-expression`, and groups.
```
responsetime > 2
error = true                      # 4xx
fault = true                      # 5xx
throttle = true                   # 429
http.url CONTAINS "/checkout"
http.status = 503
service("orders-api") { fault = true }
edge("orders-api", "payments") { responsetime > 1 }
annotation[tenant] = "acme" AND responsetime > 1
!ok                                # response status not 2XX
rootcause.fault.service { name = "payments" }
user = "alice"
```
- Annotations (indexed key-value pairs you add in code; X-Ray indexes up to 50 per trace) are
  filterable with `annotation[key]`; **metadata is not indexed**. Put tenant, order type,
  feature flag into annotations. Keys containing dots must use the bracket form.
- Plain keywords such as `error` match at trace level; an error handled downstream is found
  only with `service()` or `edge()`.
- `service()` and `edge()` scope conditions to a node or call between nodes in the
  service map.
- `rootcause.*` filters on the root cause analysis X-Ray computed.

CLI:
```bash
aws xray get-trace-summaries --start-time $(date -d '-30 min' +%s) --end-time $(date +%s) \
  --filter-expression 'service("orders-api") { fault = true } AND annotation[tenant] = "acme"' \
  --query 'TraceSummaries[].{id:Id,rt:ResponseTime,url:Http.HttpURL}'
aws xray batch-get-traces --trace-ids <id>
```

## 2. Groups
A group is a saved filter expression with its own service map; X-Ray publishes CloudWatch
metrics for the traces matching each group every minute. Group names are case sensitive, up
to 32 characters (letters, digits, dashes), and cannot be renamed.
```bash
aws xray create-group --group-name checkout-slow \
  --filter-expression 'http.url CONTAINS "/checkout" AND responsetime > 1' \
  --insights-configuration InsightsEnabled=true,NotificationsEnabled=true
```
Alarm on group metrics for SLO-like alerting per journey or tenant. Editing a group's filter
expression applies only to subsequent traces (no backfill), which can give a merged graph;
delete and recreate the group to avoid that. Groups are billed by the number of retrieved
traces that match the filter. The `Default` group cannot be deleted.

## 3. X-Ray Insights
Insights must be enabled per group. When fault rates exceed the range X-Ray predicts
statistically, it creates an insight that records the affected nodes, root cause and impact
until the issue is resolved. Notifications (best effort, not guaranteed) go to EventBridge
(`source: aws.xray`, detail-type `AWS X-Ray Insight Update`, with `State` and `Category`
fields you can match) for routing to chat or incident tooling.

## 4. Sampling interplay
Filters only search **sampled** traces. If the default sampling (1 request/s + 5%) misses
rare tenants or paths, add sampling rules with higher rates for them (match on service
name, URL path, HTTP method, host or attributes). Rules take effect at the root service,
because downstream services honour the upstream sampling decision.

## 5. CloudWatch Transaction Search
With Transaction Search enabled, 100% of spans are ingested as structured logs in the
`aws/spans` log group and searchable in CloudWatch; a percentage you choose is indexed as trace
summaries in X-Ray. Consider it for high-cardinality searches.

## Verify
- [ ] Key annotations (tenant, operation) are set in code and searchable.
- [ ] Groups exist for critical journeys with CloudWatch alarms on their fault and latency metrics.
- [ ] Insights notifications reach the on-call channel via EventBridge.

## Checked

2026-10-27, AWS documentation (current release as read on that date). X-Ray Developer Guide filter, group, insights, sampling and concepts pages, CloudWatch Transaction Search page, botocore xray model. Fixed: annotation filters use annotation[key] syntax; Transaction Search ingests 100 percent of spans as logs but indexes only a chosen percentage as trace summaries; Insights are enabled per group and the Default-group remark was removed. Confirmed: boolean/number/string keywords, service() and edge() scopes, 50 indexed annotations, group name limit of 32 characters, groups apply to new traces only, EventBridge source and detail-type. Removed group metric names and namespace, which the pages do not list.
Method: documentation only; no commands were run.
