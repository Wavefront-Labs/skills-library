---
id: computing-software.cybersecurity-defensive.security-operations.alert-severity-and-risk-score-design
name: alert-severity-and-risk-score-design
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-engineering, alert-severity-design, risk-scoring, risk-based-alerting, asset-criticality, confidence-impact, triage-priority]
level: advanced
status: draft
description: "Design alert severity and risk scores so the queue sorts itself: confidence x impact, asset and identity modifiers, RBA thresholds, and calibrating against dispositions."
sources: ["https://docs.splunk.com/Documentation/ES/latest/Admin/Analyzerisk", "https://learn.microsoft.com/en-us/azure/sentinel/detect-threats-custom", "https://www.elastic.co/guide/en/security/current/rules-ui-create.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alert severity and risk score design

When every rule is "High", severity carries no information and analysts work the queue by age.

## Two independent axes
- **Confidence (fidelity)**: how likely is this alert malicious? Measured from history:
  TP / (TP + FP + benign TP) per rule.
- **Impact**: how bad if true? Technique stage (credential dumping > discovery), asset criticality
  (DC, payment server), identity privilege (domain admin, cloud global admin), data sensitivity.
Severity = f(confidence, impact). A simple matrix:
| | Low impact | Medium | High |
|---|---|---|---|
| High confidence | Medium | High | Critical |
| Medium | Low | Medium | High |
| Low | Informational (risk only) | Low | Medium |

## Dynamic severity
Compute at alert time rather than per rule:
- Splunk ES: asset/identity `priority` multiplies risk scores; notable `urgency` = severity x priority.
- Sentinel: `alertDetailsOverride` with a `severity` column from the query
  (`extend Sev = iff(isAdmin, "High", "Medium")`).
- Elastic: severity override and risk score override mapped from source fields.

## Risk-based alerting (RBA)
Low-confidence rules write risk events (score on user/host) instead of alerts; an aggregate rule
fires when an entity crosses a threshold or shows several distinct ATT&CK tactics in 24h.
- Scores: 10-30 for weak signals, 50-80 for strong, modifiers for privileged entities.
- Threshold tuned so the aggregate alert rate is manageable (e.g. score >= 100 in 24h OR >= 3 tactics).

## Calibration loop
Monthly: per rule, compare assigned severity with actual outcomes (dispositions, escalations).
- High severity, mostly benign TP -> lower confidence, add context conditions.
- Low severity rules that often became incidents -> raise.
Track queue time by severity: critical/high should be picked up within the SLA.

## Gotchas
- Asset criticality data quality decides whether modifiers help; stale CMDB tags make things worse.
- Severity inflation by rule authors: require justification in the detection's ADS doc.
- Do not let attackers lower severity easily (e.g. by using an unlisted asset); unknown assets
  should default to medium criticality, not low.

## Verify
After changes, the proportion of TPs in critical/high rises and the median time-to-triage for
confirmed incidents drops.
