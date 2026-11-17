---
id: computing-software.cloud-infrastructure-engineering.thanos.ruler-rule-files-and-partial-response
name: ruler-rule-files-and-partial-response
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-rule, rule-files, partial-response-strategy, rules-check]
level: practitioner
status: docs-checked
description: "Write Thanos rule files with partial_response_strategy per group and validate them with rules-check."
sources: ["https://thanos.io/tip/components/rule.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ruler rule files and partial response

Rule files use Prometheus YAML (`groups:` with `name`, `interval`, `rules:`), with `record`/`expr` for recording rules and `alert`/`expr`/`for`/`labels`/`annotations` for alerting rules. Thanos adds a group field:

```yaml
groups:
- name: "warn strategy"
  partial_response_strategy: "warn"
  rules:
  - alert: "some"
    expr: "up"
- name: "default is abort"
  rules:
  - alert: "some"
    expr: "up"
```

`abort` is the default and is recommended for alerts, since a partial response can hide symptoms.

Rules in a group run sequentially at the group's interval; recording rules precompute expensive expressions for dashboards.

**Validation.** `thanos tools rules-check --rules rules/*.yaml` applies the same validation as the Ruler. It matches `promtool check rules` plus the extended syntax, because `promtool` rejects `partial_response_strategy`. Exit code is 1 on failure, 0 on success.

## Checked

2026-11-03. Confirmed against the Thanos Ruler page (components/rule.md) and the Thanos tools page (rules-check): defaults, HA external labels and alert.label-drop, mon1/eu1 label example, partial_response_strategy default abort, stateless mode via remote write, rules-check behaviour and exit codes. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
