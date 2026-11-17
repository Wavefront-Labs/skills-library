---
id: computing-software.cloud-infrastructure-engineering.alertmanager.inhibit-equal-missing-labels
name: inhibit-equal-missing-labels
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, inhibit-rules, equal-labels, missing-labels]
level: advanced
status: docs-checked
description: "Inhibition gotcha: a missing label equals an empty label, so a rule whose equal labels are absent from both alerts still applies."
sources: ["https://prometheus.io/docs/alerting/latest/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The equal list and missing labels

Semantically, a missing label and a label with an empty value are the same thing in Alertmanager. This has a direct consequence for `inhibit_rules`:

If all label names listed in `equal` are missing from both the source and target alerts, the inhibition rule applies.

Reading it through the empty-equals-missing rule:
- Every alert normally has `alertname`, so `equal: ['alertname']` compares real values.
- If you list a label such as `cluster` in `equal` and neither alert carries it, both sides count as having an empty value, so the values are equal and the target is muted.

## Checked

2026-11-08. Confirmed against the Alertmanager configuration reference source (prometheus/alertmanager, docs/configuration.md, main branch, read in full), the published form of the cited prometheus.io page: the missing-label equals empty-label rule for equal. Removed: the README example block and README purpose statement (README is not a cited source).

Method: documentation only; no commands were run.
