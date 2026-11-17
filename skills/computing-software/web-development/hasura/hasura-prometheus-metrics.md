---
id: computing-software.web-development.hasura.hasura-prometheus-metrics
name: hasura-prometheus-metrics
category: computing-software
field: web-development
product: hasura
tags: [hasura, observability, prometheus, metrics, grafana, enterprise]
level: advanced
status: docs-checked
description: "Expose Hasura Enterprise Prometheus metrics at /v1/metrics with a metrics secret and scrape them, including key metric names and cardinality."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/observability/enterprise-edition/prometheus/index.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/observability/enterprise-edition/prometheus/metrics.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/observability/enterprise-edition/prometheus/integrate-prometheus-grafana.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: monitor Hasura Enterprise Edition with Prometheus.

The metrics endpoint is disabled by default. Enable it and secure it:

```bash
HASURA_GRAPHQL_ENABLED_APIS=metadata,graphql,config,metrics
HASURA_GRAPHQL_METRICS_SECRET=<secret>
```
Check it with `curl 'http://127.0.0.1:8080/v1/metrics' -H 'Authorization: Bearer <secret>'`. The docs say the endpoint needs a secret to prevent misuse and should not be exposed over the internet.

The page's Prometheus scrape job is:

```yaml
scrape_configs:
  - job_name: 'hasura'
    metrics_path: '/v1/metrics'
    static_configs:
      - targets: ['ip_address_of_hasura_installation:8080']
```
It shows no authorization block for the secret, so how Prometheus sends the Bearer secret is not covered by these pages.

Metric types: histogram, counter and gauge. Examples from the page:
- `hasura_graphql_execution_time_seconds` (histogram; successful requests, excluding subscriptions; label `operation_type`).
- `hasura_graphql_requests_total` (counter; labels `operation_type`, `response_status`, `operation_name`, `parameterized_query_hash`).
- `hasura_active_subscriptions` (gauge; labels `subscription_kind`, `operation_name`, `parameterized_query_hash`).
- `hasura_cache_request_count` (counter; `status` hit or miss).
- Event trigger metrics such as `hasura_event_processing_time_seconds`, `hasura_event_queue_time_seconds`, `hasura_event_invocations_total`, `hasura_event_trigger_http_workers`.
- Others include `hasura_postgres_connections`, `hasura_source_health` (0 OK, 1 TIMEOUT, 2 FAILED, 3 ERROR) and cron and one-off event counters.

From v2.26.0 metrics expose high-cardinality labels by default. Cardinality can be disabled if you see high memory use, typically with more than 10000 labels.

Grafana: add Prometheus as a data source (Configuration -> Data Sources), then search for `hasura` in the Metric field when adding a panel.

## Checked
2026-11-07. Read in full all three cited pages (index.mdx, metrics.mdx, integrate-prometheus-grafana.mdx; GitHub file view, no snippet files), including the full metrics list.
Confirmed: env vars, curl, scrape config, metric names, types, labels, cardinality note.
Removed: the invented `authorization: type: Bearer` scrape config, the "keep metrics secret different from admin secret" advice, the "ready-made dashboard to import" claim (the pre-built dashboards page was not cited or read), the claim that operation name is the high-cardinality label, the "only a part was read" gotcha, and the invented Verify step.
Method: documentation only; no commands were run.
