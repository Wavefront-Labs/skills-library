---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.logql-pattern-and-regexp-parsers
name: logql-pattern-and-regexp-parsers
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [pattern-parser, loki, logql-pattern, regexp-parser, parse-unstructured-logs, label-extraction]
level: practitioner
status: docs-checked
description: "Parse unstructured log lines in LogQL with the pattern and regexp parsers and know the pattern anchoring rules."
sources: ["https://grafana.com/docs/loki/latest/query/log_queries/#parser-expression"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: extract fields from nginx-style or free-text logs at query time.

Pattern parser, using `<name>` captures and `<_>` for skipped text (from the docs, for an NGINX line):
```logql
{app="nginx"} | pattern `<ip> - - <_> "<method> <uri> <_>" <status> <size> <_> "<agent>" <_>` | status >= 500
```
Regexp parser, Go RE2 with at least one named sub-match:
```logql
{app="legacy"} | regexp `(?P<level>[A-Z]+)\s+(?P<user>\w+)\s+(?P<msg>.*)` | level="ERROR"
```
Prefer `json` or `logfmt` for structured lines. The docs say the pattern parser is easier and faster to write and outperforms regexp.

Pattern rules
- A capture is `<name>`; an unnamed capture `<_>` skips matched content. Literals can be any UTF-8 text including whitespace.
- By default a pattern is anchored at the start of the line: if it starts with literals, the line must start with them. Begin with `<_>` to avoid the anchor, for example `<_> msg="<method> <path> (<status>) <latency>"`.
- If a capture does not match, the pattern parser stops.
- A pattern is invalid if it has no named capture or has two consecutive captures not separated by whitespace.

After parsing, extracted labels can be filtered (`status >= 500`), unwrapped, or grouped in metric queries:
```logql
sum by (status) (count_over_time({app="nginx"} | pattern `<_> "<_> <uri> <_>" <status> <_>` [5m]))
```
Gotchas
- Use backticks around patterns and regexes so backslashes need no double escaping.
- Extracted label names are sanitized to Prometheus naming rules (ASCII letters, digits, underscores, colons; not starting with a digit).

## Verify
```
logcli query '{app="nginx"} | pattern `<ip> - - <_> "<method> <uri> <_>" <status> <size> <_> "<agent>" <_>` | line_format "{{.method}} {{.status}}"' --limit 5
```
Output lines show the extracted fields.

## Checked
2026-11-03. Confirmed against the Loki log queries page (parser expression section: pattern, regexp, backticks, sanitization). Corrected: the pattern parser anchors at the line start only; it does not need to match the whole line. Removed: the `__error__="PatternParserErr"` claim, "several times faster", and the CPU and indexing gotchas.
Method: documentation only; no commands were run.
