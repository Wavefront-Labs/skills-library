---
id: computing-software.cloud-infrastructure-engineering.aws.appsync-logging-xray-and-enhanced-metrics
name: appsync-logging-xray-and-enhanced-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, appsync, appsync-logging, graphql, x-ray, enhanced-metrics, field-level-logs, resolver-metrics]
level: practitioner
status: docs-checked
description: "Observe AppSync GraphQL APIs: field-level and request logs without runaway cost, X-Ray tracing, enhanced resolver and data source metrics, and alarms on errors and latency."
sources: ["https://docs.aws.amazon.com/appsync/latest/devguide/monitoring.html", "https://docs.aws.amazon.com/appsync/latest/devguide/x-ray-tracing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppSync logging, X-Ray and enhanced metrics

## Logging
```bash
aws appsync update-graphql-api --api-id "$API" --name orders \
  --log-config fieldLogLevel=ERROR,cloudWatchLogsRoleArn=$ROLE,excludeVerboseContent=true \
  --xray-enabled
```
| `fieldLogLevel` | Logs |
|---|---|
| `NONE` | no field-level logs |
| `ERROR` | field-level logs for errors only (the level AWS suggests to cut log size) |
| `INFO`, `DEBUG` | progressively more detail |
| `ALL` | most verbose field-level logging |
- Field-level logs include the generated request mapping and the transformed response mapping for each
  field. AppSync sends up to 1 MB of logs per request and truncates the rest. Use `ERROR` in production
  and raise temporarily to debug; Enhanced Metrics are an alternative to `ALL`.
- `excludeVerboseContent=true` leaves out verbose request-level content (HTTP headers, the GraphQL
  query); with it off and field logging at INFO or higher, transformed mappings are also logged
  (safer for PII when excluded).
- Log group `/aws/appsync/apis/<api-id>`; query `fieldName`, `resolverArn`, `duration` with Logs Insights.
- The CloudWatch role needs `logs:CreateLogGroup`, `logs:CreateLogStream` and `logs:PutLogEvents`
  and must trust `appsync.amazonaws.com`.

## X-Ray
- With `--xray-enabled` (`xrayEnabled`), AppSync sends traces to X-Ray and creates a service-linked
  role automatically; the service map shows the request, its resolvers and integrated AWS services.
- X-Ray sampling rules apply; the service type for rules is `AWS::AppSync::GraphQLAPI`.

## Enhanced metrics
```bash
aws appsync update-graphql-api ... --enhanced-metrics-config \
  resolverLevelMetricsBehavior=PER_RESOLVER_METRICS,dataSourceLevelMetricsBehavior=PER_DATA_SOURCE_METRICS,operationLevelMetricsConfig=ENABLED
```
- Adds metrics `Request`, `Latency` and `GraphQLError` (plus `CacheHit` and `CacheMiss` per resolver) with
  dimensions `API_Id` plus `Resolver`, `Datasource` or `Operation`. `FULL_REQUEST_*` emits for all;
  `PER_*` only where enabled on the resolver (`metricsConfig: ENABLED`) to limit cost. Enhanced
  metrics incur additional CloudWatch charges.
- Standard API metrics: `4XXError`, `5XXError`, `Latency`, `Requests`, `TokensConsumed`;
  real-time: `ConnectSuccess`, `SubscribeSuccess`, `PublishDataMessageSuccess`, `ActiveConnections`.

## Alarms
- `5XXError` Sum > 0 for 5 min; `Latency` p99 > SLO; per-resolver `GraphQLError` for critical mutations.
- `4XXError` covers requests that are not valid (bad payload or query, throttling, authorization
  misconfiguration); `5XXError` covers errors while running a query and internal AppSync problems.
  Per-resolver `GraphQLError` (enhanced metrics) and the logs show resolver-level errors.

## Verify
- [ ] Log config is ERROR in prod with verbose content excluded.
- [ ] Trace map shows AppSync -> resolvers -> data sources for a sample query.
- [ ] Alarms exist on 5XX and latency; per-resolver metrics enabled for top mutations.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS AppSync Developer Guide CloudWatch monitoring and logging page and X-Ray tracing page; botocore appsync 2017-07-25 model (LogConfig, FieldLogLevel, EnhancedMetricsConfig enums). Fixed: enhanced metric names are Request (not Requests), Latency, GraphQLError, CacheHit and CacheMiss with API_Id plus Resolver, Datasource or Operation dimensions; the unsourced claim that partial-response errors return HTTP 200 and the claim that ALL logging can cost more than the API were removed; added the 1 MB per request log limit and logging role permissions. Confirmed: fieldLogLevel enum NONE/ERROR/ALL/INFO/DEBUG, excludeVerboseContent, resolver and data source behaviour enums, /aws/appsync/apis/<id> log group, xrayEnabled with automatic service-linked role, standard and real-time metric names. Removed the unsourced service() grouping and Lambda trace-join claims.
Method: documentation only; no commands were run.
