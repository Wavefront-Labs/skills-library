---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.normalising-label-values-route-templating
name: normalising-label-values-route-templating
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [label-value-normalization, route-templating, cardinality, label-design, instrumentation, http-route]
level: practitioner
status: docs-checked
description: "Keep label values bounded: use route templates not raw URL paths, map unknown HTTP methods to _OTHER, use low-cardinality error types, and fix leaks with metric relabelling."
sources: ["https://prometheus.io/docs/practices/naming/#labels", "https://prometheus.io/docs/practices/instrumentation/#do-not-overuse-labels", "https://opentelemetry.io/docs/specs/semconv/http/http-spans/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Normalising label values

Cardinality comes from label values, so normalise them where they are produced.

## What the sources require
- Prometheus naming guidance: every unique combination of label key-value pairs is a new time series; do not use labels
  for high-cardinality dimensions such as user IDs, email addresses or other unbounded sets of values.
- Prometheus instrumentation guidance: keep metric cardinality below 10 as a general guideline, aim for a handful of
  higher-cardinality metrics across the whole system, and investigate alternatives (fewer dimensions, or moving the
  analysis out of monitoring) for a metric over 100 or with the potential to grow that large. Most metrics should have
  no labels.
- OpenTelemetry HTTP semantic conventions:
  - `http.route` is the matched route template for the request. It MUST be low-cardinality: static path segments stay,
    dynamic ones become placeholders (examples on the page: `/users/:userID?`, `my-controller/my-action/{id?}`). It MUST
    NOT be populated when the framework does not support it, because the URI path cannot substitute for it.
  - `url.template` (opt-in) is the low-cardinality template of an absolute path reference, for example `/users/{id}`.
  - `http.request.method` uses the well-known values (`CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, ...); a
    method the instrumentation has no prior knowledge of MUST be recorded as `_OTHER`, and instrumentation that could
    convert valid methods to `_OTHER` must offer an override, via an environment variable named
    `OTEL_INSTRUMENTATION_HTTP_KNOWN_METHODS` (comma-separated, case-sensitive) if done by environment.
  - `error.type` SHOULD be predictable and low-cardinality (an exception type or a component-specific low-cardinality
    identifier).

## Practice that follows
- Label metrics with the framework's route template (for example `/users/{id}`), never the raw path. Choose a single
  fixed value for requests that match no route rather than the raw path. Use your framework's documentation for how to
  read the matched template.
- Bound the method label with a known set and a catch-all; bound error labels to a fixed enumeration, not error message
  strings.
- Status code: either the full code from a known set or a class such as `5xx`, with a catch-all for unknown values.

## Fixing after the fact (relabel)
```yaml
metric_relabel_configs:
  - source_labels: [path]
    regex: "/users/[0-9]+"
    target_label: path
    replacement: "/users/{id}"
```
This corrects what is stored, but the client process still creates the series, so fix the source as well.

## Verify
- [ ] The number of distinct values of the route label stays flat while a scanner hits random URLs.
- [ ] A query for route values containing numeric path segments returns nothing.

## Checked

Checked 2026-11-08 against the Prometheus naming and instrumentation practices pages and the OpenTelemetry HTTP span
semantic conventions. Removed because the cited pages do not state them: the per-framework route accessors
(chi, gin, Express, Spring, FastAPI, Go `r.Pattern`), the `route="unmatched"` and `other` value conventions as
requirements, the claim that unbounded client labels can OOM the application and the exemplar advice for tenant labels.
Method: docs-only read of cited pages, 2026-11-08
