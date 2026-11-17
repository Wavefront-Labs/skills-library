---
id: computing-software.cloud-infrastructure-engineering.observability.transforming-telemetry-with-ottl
name: transforming-telemetry-with-ottl
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, otel-collector, ottl, transform-processor, filter-processor, attributes-processor, resource-processor, redaction-processor, metricstransform-processor, pii-redaction, drop-telemetry, rename-attributes, set-attribute, delete-key, replace-pattern, truncate-all, limit-attributes, contexts, span-context, datapoint-context, log-context, ottl-functions, ottl-conditions, error-mode, ottl-playground]
level: advanced
status: gated
description: "Reshape telemetry in the Collector with OTTL: transform processor statements per context (resource, span, metric, datapoint, log), filter processor conditions to drop noise."
sources: ["https://opentelemetry.io/docs/collector/transforming-telemetry/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/README.md", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transforming telemetry with OTTL

**Goal:** fix, enrich, redact and drop telemetry centrally, in a language you can read and
test, instead of asking 40 services to change their instrumentation.

## 1. Pick the processor
| Need | Processor | Notes |
|---|---|---|
| set/rename/delete/hash attributes, simple | `attributes` (span/log/datapoint attrs), `resource` (resource attrs) | actions: `insert`, `update`, `upsert`, `delete`, `hash`, `extract` (regex), `convert` |
| anything conditional or computed | `transform` (OTTL statements) | the general tool |
| drop whole spans/metrics/logs by condition | `filter` (OTTL conditions) | cheaper than transform for dropping |
| allow-list attributes and mask values by regex | `redaction` | PII compliance |
| metric renames/aggregations/label ops | `metricstransform`, `transform` metric context | |
| sampling | `probabilistic_sampler`, `tail_sampling` | not OTTL |
Order in the pipeline: `memory_limiter` → enrich (`k8sattributes`, `resourcedetection`) →
`transform`/`attributes` → `filter`/`redaction` → `batch`.

## 2. OTTL essentials
- **Contexts**: `resource`, `scope`, `span`, `spanevent`, `metric`, `datapoint`, `log`.
  Lower contexts can reach higher ones: in `span` context, `resource.attributes["k"]`.
- **Paths**: `attributes["http.route"]`, `name`, `kind`, `status.code`, `trace_id`,
  `body`, `severity_text`, `severity_number`, `metric.name`, `metric.unit`,
  `resource.attributes["service.name"]`, `cache["tmp"]` (per-item scratch map).
- **Statements** (`set`, `delete_key`, `delete_matching_keys`, `keep_keys`, `keep_matching_keys`,
  `replace_pattern`, `replace_all_patterns`, `replace_match`, `truncate_all`, `limit`,
  `merge_maps`, `append`, `flatten`) with optional `where <condition>`.
- **Converters** (functions returning values): `Concat`, `Int`, `Double`, `String`,
  `IsMatch`, `Substring`, `Split`, `Len`, `SHA256`, `FNV`, `UUID`, `Now`, `UnixNano`,
  `ParseJSON`, `ParseKeyValue`, `ExtractPatterns`, `ToLowerCase`, `TraceID`, `SpanID`,
  `IsMap`, `IsString`, `Hour`, `Format`.
- Enums: `SPAN_KIND_SERVER`, `STATUS_CODE_ERROR`, `SEVERITY_NUMBER_WARN`, `METRIC_DATA_TYPE_SUM`.
- `error_mode: ignore | silent | propagate` on the processor: `ignore` logs and continues (use it).

## 3. Recipes
```yaml
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - context: resource
        statements:
          - set(attributes["deployment.environment"], "prod") where attributes["deployment.environment"] == nil
          - set(attributes["service.name"], attributes["k8s.deployment.name"]) where attributes["service.name"] == "unknown_service"
      - context: span
        statements:
          # semconv migration: old → new, keep both briefly
          - set(attributes["http.response.status_code"], attributes["http.status_code"]) where attributes["http.status_code"] != nil and attributes["http.response.status_code"] == nil
          # bound cardinality: normalize ids in span names
          - replace_pattern(name, "/[0-9]+(/|$)", "/{id}$1") where kind == SPAN_KIND_SERVER
          # PII
          - replace_all_patterns(attributes, "value", "(\\d{4})\\d{8}(\\d{4})", "$$1********$$2")   # card numbers; $$ escapes $
          - delete_matching_keys(attributes, "(?i).*(password|token|secret|authorization).*")
          - set(attributes["enduser.id"], SHA256(attributes["enduser.id"])) where attributes["enduser.id"] != nil
          # mark slow
          - set(attributes["slow"], true) where end_time_unix_nano - start_time_unix_nano > 2000000000
          - truncate_all(attributes, 1024)
          - limit(attributes, 64, ["http.route", "http.response.status_code"])
    metric_statements:
      - context: metric
        statements:
          - set(name, "http.server.request.duration") where name == "http.server.duration"
          - set(unit, "s") where name == "http.server.request.duration"
          - convert_sum_to_gauge() where name == "system.cpu.load"
      - context: datapoint
        statements:
          - delete_key(attributes, "url.full")
          - set(attributes["http.route"], "unmatched") where attributes["http.route"] == nil and metric.name == "http.server.request.duration"
    log_statements:
      - context: log
        statements:
          - set(severity_number, SEVERITY_NUMBER_ERROR) where IsMatch(severity_text, "(?i)^err")
          - merge_maps(attributes, ParseJSON(body), "upsert") where IsMatch(body, "^\\{")
          - set(body, attributes["message"]) where attributes["message"] != nil
          - set(trace_id.string, attributes["trace_id"]) where attributes["trace_id"] != nil
          - replace_pattern(body, "([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\\.[a-z]{2,})", "***@$$2")
  filter:
    error_mode: ignore
    traces:
      span:
        - attributes["http.route"] == "/healthz" or attributes["http.route"] == "/metrics"
        - resource.attributes["service.name"] == "load-generator"
      spanevent:
        - name == "debug"
    metrics:
      metric:
        - IsMatch(name, "^go_gc_.*|^process_.*")
      datapoint:
        - attributes["k8s.container.name"] == "istio-proxy"
    logs:
      log_record:
        - severity_number < SEVERITY_NUMBER_INFO and resource.attributes["deployment.environment"] == "prod"
        - IsMatch(body, "(?i)healthcheck")
  redaction:
    allow_all_keys: false
    allowed_keys: [http.route, http.method, http.response.status_code, db.system, messaging.system, enduser.id]
    blocked_values: ["4[0-9]{12}(?:[0-9]{3})?", "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[a-z]{2,}"]
    summary: debug
```
`filter` **drops** items where any condition is true; a filtered-out parent span leaves
orphans — filter by `resource`/route at the root or sample instead.

## 4. Test statements before deploying
- **OTTL Playground** (`https://ottl.run`? the contrib repo ships `cmd/ottlplayground`; web
  version linked from the processor README) — paste a sample payload and statements.
- Local run: `otelcol-contrib --config test.yaml` with `otlp` receiver → `transform` →
  `debug{verbosity: detailed}` exporter and `telemetrygen traces --traces 1 --otlp-attributes 'http.status_code="500"'`.
- Unit-ish test in CI: a `golden` file approach with `otelcol validate` for syntax plus a
  small Go test using `ottl` packages if you own a custom distro.
- Watch `otelcol_processor_transform_errors`? (newer versions expose error counters) and
  Collector logs for `failed to execute statement`.

## Gotchas
- Regex strings need double escaping in YAML (`"\\d"`), and `$` in replacements must be
  `$$` (`$$1`) because the Collector config does env expansion on `$`.
- `set(attributes["x"], ...)` on a context where the attribute is a different type fails silently in `ignore` mode; use `String()`/`Int()` converters.
- `convert_sum_to_gauge` and friends change metric semantics; downstream `rate()` breaks.
- `keep_keys` on resource attributes drops `service.name` if you forget it; backends then show `unknown_service`.
- Transforms run per item: a regex-heavy statement over 100k logs/s is CPU; put `where` guards first and prefer `filter` for drops.
- Redaction `allow_all_keys: false` with a short allow-list quietly removes attributes other teams rely on (exemplar trace ids, `k8s.*`).

## Verify
- [ ] Sample payload through a local pipeline shows the renamed/scrubbed attributes exactly as intended (debug exporter output).
- [ ] After deploy, searching the backend for a known PII pattern (an email, a card test number) returns nothing new.
- [ ] Span/metric volume drops by the expected fraction after `filter` rules (`otelcol_processor_filter_spans_filtered`).
- [ ] No `failed to execute statement` lines in Collector logs over 24 h.

## Checked

- Date: 2026-11-02.
- Confirmed against: transform processor statement groups (trace_statements), replace_pattern, replace_all_patterns, delete_matching_keys, filter processor error_mode (transformprocessor and filterprocessor READMEs).
- Not confirmed: the sample regexes, redaction patterns and probabilistic_sampler wiring, which are illustrative and not stated in the fetched pages (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
