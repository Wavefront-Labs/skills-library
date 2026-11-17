---
id: computing-software.cloud-infrastructure-engineering.observability.log-aggregation-and-structured-logging
name: log-aggregation-and-structured-logging
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, logging, structured-logging, json-logs, log-schema, log-levels, log-aggregation, log-pipeline, fluent-bit, fluentd, vector, otel-collector, filelog-receiver, loki, logql, elasticsearch, opensearch, elk, cloudwatch-logs, azure-monitor-logs, log-analytics, google-cloud-logging, splunk, retention, log-sampling, pii-redaction, multiline-logs, kubernetes-logging, cost-control, ecs-schema]
level: practitioner
status: draft
description: "Build a log pipeline: one JSON log schema, stdout collection with Fluent Bit/Vector/OTel, parsing and PII redaction at the edge, index vs label choices, tiered retention and cost controls."
sources: ["OpenTelemetry Logs data model and semantic conventions", "Elastic Common Schema (ECS) reference", "Grafana Loki documentation - Labels and best practices", "Fluent Bit documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log aggregation and structured logging — one schema, one pipeline, bounded cost

**Goal:** every service emits machine-parsable logs with a shared schema, a pipeline ships
them reliably to a queryable store with personal data removed, and retention matches the
value of each log class.

## 1. A shared schema
Pick a base (OpenTelemetry log data model or Elastic Common Schema) and require these fields:
```json
{"timestamp":"2026-10-15T09:12:03.123Z","severity":"ERROR","service.name":"orders",
 "service.version":"1.42.0","deployment.environment":"prod","trace_id":"4bf9...","span_id":"00f0...",
 "event.name":"payment.declined","message":"payment declined by provider",
 "order.id":"o_81f2","http.response.status_code":502,"error.type":"ProviderTimeout"}
```
- UTC ISO-8601 timestamps with milliseconds; never local time.
- A stable `event.name` per log statement → you can count and alert on events without regexes.
- Context as fields, not interpolated into `message` (`"user 42 failed"` is unqueryable; `user.id: 42` is).
- Severity policy: ERROR = needs a human eventually; WARN = degraded but handled; INFO = business events and state changes; DEBUG off in prod (toggle per service at runtime).

## 2. Emit to stdout, collect at the node
Apps write JSON lines to stdout/stderr; a node agent tails and ships. Don't ship from inside
the app to the backend — it couples app latency to the log backend.
- Agents: Fluent Bit (light, C), Vector (Rust, strong transforms), OTel Collector `filelog` receiver (one agent for all signals).
- Kubernetes: DaemonSet tails `/var/log/containers`, enriches with pod/namespace labels.
- Managed: CloudWatch agent / FireLens, Azure Monitor agent, Ops Agent on GCP.
- Buffer to disk in the agent; backpressure during backend outages otherwise drops logs.

## 3. Process at the edge
- **Parse** non-JSON legacy logs once (regex/grok) in the agent, not at query time.
- **Multiline**: stack traces split into many records unless the agent's multiline parser joins them — or log exceptions as one JSON field.
- **Redact** PII and secrets before logs leave the node: emails, card numbers, tokens in URLs, `Authorization` headers. Allow-list fields for sensitive services rather than deny-listing patterns.
- **Drop or sample** noise: health checks, successful high-volume DEBUG, repeated identical errors (rate-limit per `event.name`).

## 4. Store and index wisely
- **Loki-style (label-indexed):** labels must be low-cardinality (`service`, `env`, `namespace`, `level`); everything else stays in the line and is filtered at query time. Putting `user_id` in labels creates a stream per user and kills ingestion.
- **Elasticsearch/OpenSearch (field-indexed):** define explicit mappings; dynamic mapping on arbitrary JSON causes mapping explosions — set `index.mapping.total_fields.limit` and map unknown objects as `flattened`.
- **Cloud-native** (CloudWatch Logs, Log Analytics, Cloud Logging): easiest; ingest pricing dominates cost.

## 5. Retention tiers
| Class | Hot (searchable) | Archive |
|---|---|---|
| Debug/app noise | 3-7 days | none |
| Application INFO/ERROR | 14-30 days | object storage 90 days-1 yr |
| Audit / security | 90 days | per regulation (often 1-7 yrs), immutable |
Archive to object storage (S3/GCS/Blob) with lifecycle rules; rehydrate on demand.

## Gotchas
- Logging inside hot loops at INFO can be the largest line on the cloud bill.
- Ingestion is usually billed per GB *before* compression; measure bytes per request.
- Inconsistent field types (`status` as string in one service, int in another) break indexing — enforce the schema with a shared logging library.
- Lost logs during node eviction: agents need disk buffers and `terminationGracePeriodSeconds` long enough to flush.
- Logs are not metrics: counting errors from logs at query time is slow and costly; emit a counter too.

## Verify
- [ ] All services emit JSON with the required fields including `trace_id`.
- [ ] A test PII string injected into a log does not appear in the backend.
- [ ] Label/field cardinality is bounded and monitored.
- [ ] Agents buffer to disk; a backend outage drill showed no loss within the buffer window.
- [ ] Retention tiers are configured and cost per GB/day is reported per service.
