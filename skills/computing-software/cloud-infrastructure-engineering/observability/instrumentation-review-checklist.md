---
id: computing-software.cloud-infrastructure-engineering.observability.instrumentation-review-checklist
name: instrumentation-review-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [instrumentation-review-checklist, instrumentation, code-review, metric-naming, cardinality, opentelemetry]
level: practitioner
status: docs-checked
description: "Code-review checklist for new metrics and attributes: Prometheus naming, units, label cardinality, initialising series, failure ratios and OpenTelemetry naming rules."
sources: ["https://prometheus.io/docs/practices/naming/", "https://prometheus.io/docs/practices/instrumentation/", "https://opentelemetry.io/docs/specs/semconv/general/naming/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumentation review checklist

Use on any PR that adds or changes telemetry. Each "no" needs a reason in the PR.

## Prometheus metrics (naming page: a style guide, not required by Prometheus)
- [ ] Name starts with a single-word application prefix and refers to one unit and one quantity.
- [ ] Base units (seconds, bytes, meters), plural unit suffix, `_total` on accumulating counts; bits converted to bytes; percent as a 0 to 1 ratio.
- [ ] `sum()` or `avg()` across all label dimensions is meaningful; otherwise split the metric.
- [ ] Label names are not repeated in the metric name.
- [ ] Every label has a bounded set of values. No user IDs, emails or other unbounded values. The instrumentation page suggests keeping cardinality below about 10 for most metrics, and treats anything above 100 as needing another approach.
- [ ] Prefer no labels to start; add them when a concrete use case appears.
- [ ] Counter only if the value never goes down, otherwise a gauge; `rate()` is not applied to gauges.
- [ ] Failures counted with a total-attempts metric so the failure ratio is easy to compute.
- [ ] Known series exported with value 0 so absent series do not complicate queries.
- [ ] Time since an event is exported as a Unix timestamp, not elapsed time.
- [ ] Metrics defined in the file where they are used; no procedurally generated metric names.
- [ ] Hot code (over about 100k calls per second per process) avoids labels in inner loops or caches label lookups.

## OpenTelemetry names (general naming page)
- [ ] Lowercase, dot-delimited namespaces, snake_case within a component.
- [ ] Company or app-specific names are prefixed with a reverse domain or unique app name, never an existing OpenTelemetry namespace; `otel.*` is reserved.
- [ ] Metric counters and UpDownCounters do not append `_total`; units are not needed in names unless ambiguous (this differs from Prometheus naming, so follow the target convention).
- [ ] Singular attribute names for one entity, plural with arrays for several.

## Downstream
- [ ] Dashboards and alerts that use the metric are updated, or the PR says they are not needed.
- [ ] Renamed or removed metrics are checked against rule and dashboard repos.

## Gotcha
Renaming a metric silently breaks alerts and dashboards that reference it. Keep the old name for a release or update the rules in the same change (practice advice; the pages do not cover it).

## Checked

2026-11-08. Confirmed on the three pages: Prometheus naming rules and base-unit table, instrumentation guidance on labels (about 10, 100), counters versus gauges, failure ratios, zero-initialisation, timestamps, performance note, and the OpenTelemetry general naming rules including the no-_total statement for counters. Removed because none of the three pages cover them: span checklist items (names, kinds, RecordException, context propagation), log checklist items, `promtool check metrics`, help-text and series-estimate items, and the `<namespace>_<subsystem>_<name>_<unit>` template (the page says single-word prefix only). The rename gotcha is flagged as practice advice.
Method: documentation only; no commands were run.
