---
id: computing-software.cloud-infrastructure-engineering.datadog.trace-ingestion-sampling
name: trace-ingestion-sampling
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, trace-sampling, ingestion-controls, retention-filters, sampling-rules]
level: practitioner
status: docs-checked
description: "Control Datadog APM ingestion with head-based sampling, SDK sampling rules, Agent error and rare samplers, and retention filters."
sources: ["https://docs.datadoghq.com/tracing/trace_pipeline/ingestion_mechanisms/", "https://docs.datadoghq.com/tracing/trace_pipeline/trace_retention/", "https://docs.datadoghq.com/tracing/metrics/metrics_namespace/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trace ingestion and retention
Goal: keep important traces and drop noise. Two separate stages: ingestion (what is sent to Datadog) and retention (which ingested spans are indexed).

Ingestion
- Default is head-based sampling: the keep or drop decision is made at the root span and propagated to downstream services. Rates can be set in the Agent (default) or in SDKs; any SDK mechanism overrides the Agent.
- Agent (`ingestion_reason: auto`): the Agent sends sampling rates to SDKs to target ten traces per second overall, spread across services by traffic. Change the target with `target_traces_per_second` in `datadog.yaml` or `DD_APM_TARGET_TPS` (default 10). It applies only to Datadog SDKs, not OpenTelemetry SDKs, and the real rate fluctuates. With Agent 7.42.0 or higher and Remote Configuration it can be changed from the Ingestion Control page without restart, and the remote value takes precedence over local config.
- SDK rules (`ingestion_reason: rule`): sample rate by service or resource at the trace root, with a rate limit (default 100 traces per second per service instance, ignored when using the Agent default). Example from the docs:

```
export DD_TRACE_SAMPLING_RULES='[{"service": "my-service", "resource": "GET /checkout", "sample_rate": 1},{"service": "my-service", "sample_rate": 0.2}]'
```

- `DD_TRACE_SAMPLE_RATE` is deprecated in several SDKs; the docs say to use `[{"sample_rate":0.1}]` in `DD_TRACE_SAMPLING_RULES` instead. Resource-based rules need a minimum tracer version (for example Java 1.26.0, Python 2.8.0, Go 1.60.0).
- Rules drop traces at the root, so they do not produce incomplete traces.
- Error sampler (`ingestion_reason: error`): the Agent keeps error traces head-based sampling dropped, up to 10 per second per Agent; set `errors_per_second` or `DD_APM_ERROR_TPS` (Agent 7.33+); `0` disables it. A rare sampler keeps low-traffic services and resources. Both are ignored for services with SDK sampling rules.

Retention
- After ingestion, retention filters decide which spans are indexed for 15 days. The Intelligent Retention Filter is always active; default filters include `Error Default` (query configurable, for example `status:error, env:production`). Add custom filters at APM > Retention Filters with `apm_retention_filter_write` permission.
- Filter order matters: a span matching an earlier filter is not handled by later ones. Retention filters do not change what is ingested.
- Trace metrics (requests, errors, latency) are calculated from 100% of traffic regardless of ingestion sampling in most cases, but some sampling configurations make them represent a subset.
- Usage metrics: `datadog.estimated_usage.apm.ingested_traces` (head-based) and `datadog.estimated_usage.apm.indexed_spans`.

Gotcha: the draft's `apm_config.max_traces_per_second` is not the documented Agent setting; use `target_traces_per_second`.

## Verify
- The Ingestion Control page shows the configuration per service (Automatic or rule) and error traces stay searchable.

## Checked
2026-11-03. Confirmed against the Ingestion Mechanisms, Trace Retention and Trace Metrics pages. Fixed: removed the wrong Agent key `apm_config.max_traces_per_second` (docs use `target_traces_per_second`), replaced the `healthcheck` rate-0 rules example with the docs example, and removed the deprecated `DD_TRACE_SAMPLE_RATE=0.2` example and weekly review advice.
Method: documentation only; no commands were run.
