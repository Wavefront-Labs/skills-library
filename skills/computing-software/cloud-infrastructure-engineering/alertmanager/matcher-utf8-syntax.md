---
id: computing-software.cloud-infrastructure-engineering.alertmanager.matcher-utf8-syntax
name: matcher-utf8-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, matchers, utf8-matchers, label-matching]
level: advanced
status: docs-checked
description: "UTF-8 matcher syntax in Alertmanager: three tokens, the four operators, unquoted literals versus double-quoted strings and reserved characters."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# UTF-8 matchers

Label matchers match alerts to routes, silences and inhibition rules. A UTF-8 matcher consists of three tokens:

1. A label name: an unquoted literal or a double-quoted string.
2. An operator: `=` equals, `!=` not equal, `=~` matches the regular expression, `!~` does not match the regular expression.
3. A label value or regular expression: an unquoted literal or a double-quoted string.

Unquoted literals may contain all UTF-8 characters except the reserved characters: whitespace and any of `{ } ! = ~ , \ " '` and the backtick. Examples of valid unquoted literals are `foo` and `[a-zA-Z]+`, and non-Latin words also work.

Double-quoted strings may contain all UTF-8 characters with no reserved characters, but literal double quotes and backslashes must be escaped with a single backslash.

Because the right-hand side is required in UTF-8 matchers, `foo=` (valid in classic syntax) must be written `foo=""`.

```yaml
matchers:
  - alertname = Watchdog
  - severity =~ "warning|critical"
  - env !~ preprod
```

Classic matchers (the pre-0.27 parser) use a valid Prometheus label name, the same four operators, and a UTF-8 string, optionally in double quotes. The third token may be empty. OpenMetrics escaping applies: `\"` for a double quote, `\n` for a line feed, `\\` for a backslash.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: the UTF-8 matcher syntax. Removed: nothing.

Method: documentation only; no commands were run.
