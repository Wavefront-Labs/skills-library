---
id: computing-software.cloud-infrastructure-engineering.alertmanager.inhibit-rule-fields
name: inhibit-rule-fields
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, inhibit-rules, source-matchers, target-matchers]
level: practitioner
status: docs-checked
description: "Fields of an Alertmanager inhibit_rule: name, source_matchers, target_matchers, equal, and the deprecated match fields."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# inhibit_rules fields

An inhibition rule mutes target alerts when a source alert matching another set of matchers exists. Both source and target alerts must have the same values for the label names in `equal`.

```yaml
inhibit_rules:
- name: critical-mutes-warning
  source_matchers:
    - severity="critical"
  target_matchers:
    - severity="warning"
  equal: ['alertname']
```

Fields:
- `name`: optional; duplicate names are allowed but affect the per-rule metrics.
- `target_matchers`: matchers that must be fulfilled by the alerts to be muted.
- `source_matchers`: matchers for which one or more alerts must exist for the inhibition to take effect.
- `equal`: label names whose values must be equal in source and target.
- Deprecated: `target_match`, `target_match_re`, `source_match`, `source_match_re`; use the `*_matchers` forms.

Self-inhibition guard: an alert that matches both the target and the source side of a rule cannot be inhibited by alerts for which the same is true, including itself. The documentation recommends choosing matchers so alerts never match both sides, since that is easier to reason about.

Timing link: `group_wait` exists partly so inhibiting alerts can arrive before the first notification; if they arrive late, target alerts might not be inhibited.

## Checked

2026-11-03. Confirmed against the Alertmanager Configuration page (prometheus.io/docs/alerting/latest/configuration): inhibit_rule fields, deprecated fields, self-inhibition note.

Method: documentation only; no commands were run.
