---
id: computing-software.cybersecurity-defensive.security-operations.soc-case-quality-review
name: soc-case-quality-review
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [case-quality-review, soc-management, quality-assurance, alert-triage, peer-review, soc-metrics]
level: practitioner
status: draft
description: "Run SOC case quality assurance: sampling cases, scoring rubric for triage, evidence, disposition and documentation, feedback loops and calibration sessions."
sources: ["https://www.ncsc.gov.uk/collection/building-a-security-operations-centre", "https://www.sans.org/white-papers/", "https://www.first.org/standards/frameworks/csirts/csirt_services_framework_v2.1"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Case quality assurance reviews

## Sampling
- Weekly random sample per analyst (e.g. 5 closed cases), plus all cases auto-closed by
  automation (sample), all reopened cases and all cases closed as false positive on high-severity
  rules.
- Stratify by alert type so rare types are reviewed.

## Rubric (score 0-2 each)
1. **Triage steps**: runbook steps followed; key pivots performed (user, host, process, network).
2. **Evidence**: queries/screenshots/links attached; enough for someone else to reach the same result.
3. **Disposition correctness**: reviewer agrees with TP/BTP/FP classification.
4. **Escalation**: escalated when criteria met; not escalated needlessly.
5. **Documentation**: clear summary, timeline, actions, time zone stated.
6. **Timeliness**: SLA met.
Critical fail: wrong disposition on a true positive.

## Process
- Reviewer (senior analyst/lead) records scores in a QA tracker linked to case IDs.
- Feedback to analyst within a week, framed as learning; patterns become training topics or runbook
  updates.
- Monthly calibration session: leads score the same 3 cases independently and reconcile to keep
  scoring consistent.

## Metrics
QA score average per analyst/team, critical-fail rate, top recurring defects, runbook changes made
from QA findings.

## Gotchas
- QA used punitively makes analysts hide uncertainty; separate QA from performance discipline except
  for repeated negligence.
- Reviewing only failed cases biases scores; sample randomly.

## Verify
Quarterly: critical-fail rate trending down, every critical fail followed by a documented corrective action.
