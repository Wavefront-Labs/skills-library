---
id: computing-software.cloud-infrastructure-engineering.observability.parsing-log-bodies-with-ottl
name: parsing-log-bodies-with-ottl
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [parse-json-ottl, parse-logs-ottl, log-body-parsing, transforming-telemetry, ottl]
level: advanced
status: docs-checked
description: "Parse log bodies in the collector with OTTL: ParseJSON, ExtractPatterns, ParseKeyValue, grok, timestamps and severity, using the cache map and guarding with conditions."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/ottlfuncs/README.md", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor", "https://opentelemetry.io/blog/2024/otel-collector-container-log-parser/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing log bodies with OTTL

Use when logs arrive as raw strings over OTLP (or after filelog without operators) and you want structured
attributes, real timestamps and severity.

```yaml
processors:
  transform/parse:
    error_mode: ignore              # never drop the record because one statement failed
    log_statements:
      - context: log
        statements:
          # JSON bodies
          - merge_maps(cache, ParseJSON(body), "upsert") where IsMatch(body, "^\\s*\\{")
          - set(attributes["http.route"], cache["route"]) where cache["route"] != nil
          - set(severity_text, cache["level"]) where cache["level"] != nil
          - set(time, Time(cache["ts"], "%Y-%m-%dT%H:%M:%S.%fZ")) where cache["ts"] != nil
          - set(body, cache["msg"]) where cache["msg"] != nil
          - set(trace_id.string, cache["trace_id"]) where cache["trace_id"] != nil
          # plain text: "2026-10-16 09:12:03 WARN [worker-3] cache miss key=abc"
          - merge_maps(cache, ExtractPatterns(body, "^(?P<ts>\\S+ \\S+) (?P<lvl>[A-Z]+) \\[(?P<thread>[^\\]]+)\\] (?P<msg>.*)$"), "upsert") where not IsMatch(body, "^\\s*\\{")
          - merge_maps(attributes, ParseKeyValue(cache["msg"], "=", " "), "insert") where cache["msg"] != nil
          - set(attributes["thread.name"], cache["thread"]) where cache["thread"] != nil
```

## Functions
`ParseJSON`, `ParseKeyValue(target, delimiter, pair_delimiter)`, `ParseCSV`, `ParseSimplifiedXML`, `ParseXML`,
`ExtractPatterns` (named groups), `ExtractGrokPatterns(body, "%{COMMONAPACHELOG}", true)`, `Time(str, format)`,
`flatten(attributes, "prefix", depth)`, `keep_keys`, `delete_matching_keys`, `truncate_all`, `limit`.
`cache` is a per-record scratch map that is not exported - parse into it, then pick fields.

## Severity after parsing
`set(severity_number, SEVERITY_NUMBER_WARN) where severity_text == "WARN"` (map each level), use the `ParseSeverity(target, mapping)` converter, or parse in filelog
with the `severity` block.

## Gotchas
- Without guards, `ParseJSON` on a body that is not JSON returns an error; with `error_mode: propagate` the payload is dropped from the collector.
- `$` in regexes must be `$$` in the config file (env substitution).
- Loki only stores string log bodies and stringifies non-string bodies, so setting `body` to a map changes what you see there.

## Verify
`debug` exporter output: `Body`, `Attributes`, `Timestamp`, `SeverityNumber` populated as intended.

## Checked
Checked 2026-10-28 against the OTTL function reference (pkg/ottl/ottlfuncs README), the ottllog context README, the transformprocessor README, the Collector configuration page and the Loki OTLP page.
- Confirmed: `ParseJSON` (errors on non-JSON), `ParseKeyValue(target, delimiter, pair_delimiter)` with `=` default, `ParseCSV`, `ParseXML`, `ParseSimplifiedXML`, `ExtractPatterns` (named groups required), `ExtractGrokPatterns(target, pattern, namedCapturesOnly, ...)`, `Time`, `flatten`, `keep_keys`, `delete_matching_keys`, `truncate_all`, `limit`, `merge_maps`, `trace_id.string` path, `error_mode` ignore/propagate (propagate drops the payload), `$$` for a literal `$`, Loki stringifies non-string bodies.
- Removed: the CPU/telemetrygen benchmark claim and the "detailed" debug verbosity wording; the claim that Loki displays a map body as JSON is reworded to what the page states.
- The `cache` scratch map is the transform processor's documented per-context `cache` path (ottllog README); read, not run.

Method: documentation only; no commands were run.
