---
id: computing-software.cloud-infrastructure-engineering.observability.otel-log-severity-mapping
name: otel-log-severity-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [severity-number-mapping, severity-text, otel-logs, log-levels, log-parsing]
level: practitioner
status: docs-checked
description: "Map source log levels to OTel SeverityNumber and SeverityText: ranges, mapping tables for syslog, Log4j, Python and .NET, filelog severity parser and OTTL fixes."
sources: ["https://opentelemetry.io/docs/specs/otel/logs/data-model/#field-severitynumber", "https://opentelemetry.io/docs/specs/otel/logs/data-model-appendix/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/types/severity.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Severity number and text mapping

## Ranges (logs data model)
| Range | Short name |
|---|---|
| 1-4 | TRACE (TRACE..TRACE4) |
| 5-8 | DEBUG |
| 9-12 | INFO |
| 13-16 | WARN |
| 17-20 | ERROR |
| 21-24 | FATAL |
0 may be used for an unspecified value. `SeverityText` keeps the original source string (`warning`, `E`, `err`). Filter and alert on
the **number** (`>= 17` means an erroneous situation per the data model), which is comparable across sources. If a source has
several severities in one range, assign values in that range by severity; a lone source severity gets the smallest value of the
range. Records without severity may be treated by backends as INFO (9).

## Common mappings (spec data model appendix B, plus SDK bridges)
| Source | Mapping |
|---|---|
| syslog | Emergency FATAL(21), Alert ERROR3(19), Critical ERROR2(18), Error ERROR(17), Warning WARN(13), Notice INFO2(10), Informational INFO(9), Debug DEBUG(5) |
| Log4j | FATAL 21, ERROR 17, WARN 13, INFO 9, DEBUG 5, TRACE 1 |
| .NET LogLevel | Critical 21, Error 17, Warning 13, Information 9, Debug 5, Trace 1 |
| Python logging (SDK `_STD_TO_OTEL` table) | CRITICAL(50) 21, ERROR(40) 17, WARNING(30) 13, INFO(20) 9, DEBUG(10) 5 |
| Go slog (otelslog bridge) | Debug 5, Info 9, Warn 13, Error 17 (slog levels are offset into the OTel range) |
Appenders and bridges do this for you; parsing raw text needs explicit mapping.

## filelog severity parser
```yaml
operators:
  - type: json_parser
    severity:
      parse_from: attributes.level
      preset: default            # understands common words and numbers
      mapping:
        warn: [warning, w, WARN]
        error: [err, e, 'error ']
        fatal: [panic, crit]
        info:
          - min: 200               # numeric range (list form, as in the stanza docs)
            max: 299
```
Aliases are `trace`..`trace4`, `debug`..`debug4`, `info`..`info4`, `warn`..`warn4`, `error`..`error4`, `fatal`..`fatal4` and
`default`; `preset` defaults to `default` and `preset: none` starts from an empty mapping. By default the original text is kept as
`SeverityText`; `overwrite_text: true` replaces it with the standard short name.

## OTTL fix-up (transform processor)
```yaml
transform/severity:
  log_statements:
    - context: log
      statements:
        - set(log.severity_number, SEVERITY_NUMBER_WARN) where IsMatch(log.severity_text, "(?i)^warn")
        - set(log.severity_number, SEVERITY_NUMBER_ERROR) where IsMatch(log.severity_text, "(?i)^(err|error)$")
        - set(log.severity_text, "ERROR") where log.severity_number >= SEVERITY_NUMBER_ERROR and log.severity_number < SEVERITY_NUMBER_FATAL
```

## Backends
Check that unspecified (0) records are rare in your backend: a query or dashboard on records with severity number 0 shows which
sources need a mapping.

## Checked

2026-10-24. OpenTelemetry specification logs data model and data-model-appendix (Appendix B), stanza severity type and severity_parser docs, OTTL log context README, opentelemetry-python SDK `_STD_TO_OTEL` table and opentelemetry-go-contrib otelslog bridge (main branch). Confirmed: severity ranges and names, 0 as unspecified, error semantics at 17, syslog, Log4j and .NET mappings, Python and slog bridge mappings, stanza mapping aliases, `preset` default, `overwrite_text`, range list form, and OTTL `log.severity_number`, `log.severity_text` and `SEVERITY_NUMBER_*` enums. Removed the Logback line (not in the appendix) and the Loki-specific claims.

Method: documentation only; no commands were run.
