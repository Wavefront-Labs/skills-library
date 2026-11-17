---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.logql-line-format-and-label-format-templates
name: logql-line-format-and-label-format-templates
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [line-format, loki, label-format, logql-templates, go-template, template-functions, regexreplaceall]
level: practitioner
status: docs-checked
description: "Reshape LogQL output with line_format and label_format Go templates, including template functions and conditionals."
sources: ["https://grafana.com/docs/loki/latest/query/template_functions/", "https://grafana.com/docs/loki/latest/query/log_queries/#parser-expression"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: readable log lines and derived labels without changing stored data.

```logql
{app="api"} | json | line_format "{{.level | upper}} {{.msg}} (user={{.user}})"

{app="api"} | logfmt
  | label_format duration_ms=`{{ mulf (.duration | float64) 1000.0 }}`
  | line_format `{{ if eq .level "error" }}ERR{{ else }}ok{{ end }} {{ .route }} {{ .duration_ms }}ms`

{job="nginx"} | json | label_format host=`{{ regexReplaceAll "\\..*" .host "" }}`
```
Templates use Go `text/template`. Labels are variables written `{{ .label_name }}`; `__line__` returns the original line and `__timestamp__` the line's timestamp (for example `{{ __timestamp__ | date "2006-01-02T15:04:05.00Z-07:00" }}`). Pipelines chain with `|` and pass the result as the last argument of the next function: `{{ .path | replace " " "_" | trunc 5 | upper }}`.

Functions documented on the page include: `upper`, `lower`, `title`, `trunc`, `trim`, `replace`, `regexReplaceAll`, `printf`, `default`, `contains`, `hasPrefix`, `eq`, `date`, `unixToTime`, `duration_seconds`, and math functions `add`, `sub`, `mulf`, `divf`, `float64`. Boolean functions combine with `and`/`or` and `if`/`else if`/`else`.

`default` outputs a fallback when the source string is empty, useful for fields that may be missing.

Gotchas
- Extracted label names are sanitized to Prometheus conventions by the parsers (letters, digits, underscores, colons).
- Backtick-quote templates to avoid escaping double quotes and backslashes.
- `label_format` can also rename a label (`dst=src`) or set it from a template.

## Verify
Run in Explore and compare one raw line to its formatted counterpart; test conditionals with a known error entry.

## Checked
2026-11-03. Confirmed against the Loki template functions page (functions, `__line__`, `__timestamp__`, pipelines, `default`, `regexReplaceAll`, `float64`, `mulf`) and the log queries parser section (label sanitization, template form of `label_format`). Removed: `ToLower`, `user.id` becoming `user_id` example, and the claims that missing fields render empty, that downstream filters see the new text, and that high-cardinality labels bloat output.
Method: documentation only; no commands were run.
