---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-appsec-rule-syntax
name: crowdsec-appsec-rule-syntax
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [appsec-rules, waf-rules, zones, transforms, match-types, libinjection, rule-labels]
level: advanced
status: docs-checked
description: "Write CrowdSec AppSec rules: zones, variables, transforms, match types, and combining conditions with and/or."
sources: ["https://docs.crowdsec.net/docs/appsec/rules_syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rule files have `name`, `description`, `rules` and `labels`.

```yaml
name: crowdsecurity/example-rule
description: "Detect example pattern"
rules:
  - zones:
      - URI
    transform:
      - lowercase
    match:
      type: contains
      value: this-is-a-appsec-rule-test
labels:
  type: exploit
  service: http
  behavior: "http:exploit"
  confidence: 3
  spoofable: 0
```

Each condition needs `zones` and `match`; `variables` and `transform` are optional. Conditions group with `and` (all must match) and `or` (any); with no operator at rule level they are treated as `or`.

## Zones

`ARGS`, `ARGS_NAMES`, `BODY_ARGS`, `BODY_ARGS_NAMES`, `COOKIES`, `COOKIES_NAMES`, `FILES`, `FILES_NAMES`, `HEADERS`, `HEADERS_NAMES`, `METHOD`, `PROTOCOL`, `URI`, `URI_FULL`, `RAW_BODY`, `FILENAMES`, `FILES_TOTAL_SIZE`.

## Variables

Restrict a keyed zone (`ARGS`, `BODY_ARGS`, `HEADERS`, `COOKIES`) to particular keys by name, or by RE2 regexp wrapped in slashes, for example `/pattern_.*/`. With the default `base-config`, form, multipart, XML and JSON bodies are decoded; for `application/json` variable names are prefixed with `json.`.

## Match types

`regex` (RE2), `equals`, `startsWith`, `endsWith`, `contains`, `libinjectionSQL`, `libinjectionXSS`, numeric `gt`, `lt`, `gte`, `lte`, and `eq` (numeric equality; use `equals` for strings). The `length` transform converts the target to its string length. Quote `value` when YAML could read it as a boolean or number: unquoted `off`, `no`, `y` and `1` are not strings.

## Checked

2026-11-03. Confirmed against the AppSec 'WAF Rules Syntax' page: file directives, conditions, and/or grouping, zones, variables and RE2 slashes, base-config decoders and the json. prefix, match types (including eq and the YAML quoting tip), the length transform. Removed: nothing.

Method: documentation only; no commands were run.
