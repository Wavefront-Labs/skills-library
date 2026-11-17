---
id: computing-software.cloud-infrastructure-engineering.observability.observability-maturity-assessment
name: observability-maturity-assessment
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability-maturity-assessment, signal-coverage-audit, observability, instrumentation, golden-signals]
level: practitioner
status: draft
description: "Audit services for signal coverage (golden signals, traces, logs, SLOs, runbooks) and produce a ranked gap list using a simple maturity rubric."
sources: ["https://sre.google/sre-book/monitoring-distributed-systems/", "https://opentelemetry.io/docs/concepts/observability-primer/", "https://sre.google/workbook/monitoring/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Observability maturity assessment

Goal: a per-service scorecard that shows where an incident would be blind, ranked by service criticality.

## Rubric (score each 0-2 per service)
| Area | 0 | 1 | 2 |
|---|---|---|---|
| Golden signals | none | some dashboards | latency/traffic/errors/saturation with alerts |
| SLO | none | SLI defined | SLO + burn-rate alerts + error budget policy |
| Tracing | none | auto-instrumented | propagated end to end, sampled deliberately |
| Logs | unstructured | structured JSON | trace ids in logs, retention by class |
| Correlation | none | manual | metric to trace (exemplars) to log links work |
| Alert hygiene | cause alerts page | mixed | symptom pages, runbook link on every page |
| Ownership | unknown | team label | team label + on-call route + service catalog entry |

## Gathering evidence automatically
```promql
# services with metrics but no latency histogram
count by (service) (up) unless count by (service) (http_server_request_duration_seconds_bucket)
# alert rules missing runbook_url
```
Use `promtool` / `pint` to list rules without `runbook_url`; query the tracing backend for services with no spans in 24h; check log streams for `trace_id` field presence.

## Process
1. Pull the service list from the catalog, tier by criticality.
2. Score with automated checks first, interviews for the rest (30 min per team).
3. Rank gaps by tier x missing score; pick the top 5 per quarter.
4. Re-score quarterly; publish the trend, not a league table of teams.

## Gotchas
- Scoring dashboards by count rewards clutter; score by "can on-call answer X in 5 minutes".
- Auto-instrumentation gives traces but often breaks at async boundaries: test an end-to-end trace.

## Verify
- [ ] Every tier-1 service scores 2 on golden signals, SLO and ownership.
- [ ] Gap list has owners and dates.
