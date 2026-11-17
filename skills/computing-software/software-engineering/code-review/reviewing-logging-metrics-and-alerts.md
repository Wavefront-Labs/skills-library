---
id: computing-software.software-engineering.code-review.reviewing-logging-metrics-and-alerts
name: reviewing-logging-metrics-and-alerts
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, observability-review, logging, metrics, alerting, tracing, cardinality]
level: practitioner
status: draft
description: "Review observability in changes: useful structured logs without secrets, metrics with bounded cardinality, trace spans, and alerts that are actionable with runbooks."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://opentelemetry.io/docs/concepts/semantic-conventions/", "https://prometheus.io/docs/practices/naming/", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing logging, metrics and alerts

## Ask first: when this breaks in production, how will we know and how will we debug it?

## Logs
- Structured (key-value/JSON) with stable field names; include correlation/trace id, entity ids,
  outcome. `log.info("payment captured", order_id=..., amount_minor=..., provider=...)`.
- Right level: ERROR = someone should look; WARN = unexpected but handled; INFO = significant
  business events; DEBUG off in production. Errors logged once (not at every layer of rethrow).
- **No secrets or sensitive data**: tokens, passwords, full card numbers, session cookies, PII beyond
  what policy allows (OWASP logging cheat sheet). Watch `log.debug(request)` dumping headers.
- Not in hot loops without sampling (cost and noise); not inside tight retry loops.
- Exceptions logged with stack trace and context, not just `str(e)`.

## Metrics
- New feature/endpoint/queue has RED (rate, errors, duration) or USE metrics.
- **Cardinality**: labels must be bounded. No user ids, order ids, raw URLs or error messages as
  label values; use route templates (`/orders/{id}`) and error classes. Each label combination is a
  time series.
- Naming conventions (Prometheus: `snake_case`, base units, `_total` for counters, `_seconds`,
  `_bytes`); histograms for latency, not averages.
- Counters vs gauges used correctly.

## Traces
Spans around external calls and significant internal work, with semantic-convention attributes
(`http.request.method`, `db.system`); context propagated across async boundaries and queues.

## Alerts
- Alert on symptoms users feel (SLO burn rate, error rate, latency) rather than causes (CPU 80%).
- Every alert: actionable, has a runbook link, owner, severity, and a threshold justified by data.
- Will it page at 3am for something that can wait? Make it a ticket instead.
- Tested: fire it in staging or with a unit test (`promtool test rules`).

## Dashboards
Updated to include new metrics; no orphan panels for removed metrics.
