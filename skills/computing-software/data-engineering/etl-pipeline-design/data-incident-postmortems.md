---
id: computing-software.data-engineering.etl-pipeline-design.data-incident-postmortems
name: data-incident-postmortems
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, data-postmortem, incident-management, blameless, root-cause-analysis]
level: practitioner
status: draft
description: "Run blameless postmortems for data incidents: timeline, impact on consumers and decisions, root and contributing causes, detection gaps, and tracked action items."
sources:
  - https://sre.google/sre-book/postmortem-culture/
  - https://sre.google/workbook/postmortem-culture/
  - https://www.atlassian.com/incident-management/postmortem
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data incident postmortems

**Goal:** each significant data incident makes the platform measurably more reliable, without blame.

## When to write one
Wrong data reached consumers (dashboards, customers, ML models), an SLA was breached for a critical dataset, data was lost, or a near miss that could have done either.

## Template
1. **Summary**: one paragraph: what happened, impact, duration.
2. **Impact**: which datasets/dashboards/models; who used wrong data and for what decisions (reports sent, campaigns targeted, invoices); data volume affected; time window of bad data vs time to detect.
3. **Timeline** (UTC): first bad data written, detection, acknowledgement, mitigation, data repaired, consumers notified.
4. **Root cause and contributing factors**: e.g. source changed currency field semantics (root); no contract/test on value ranges, alert routed to an unowned channel (contributing). Ask "why" until you reach process/system gaps, not people.
5. **Detection**: how was it found? By a user = detection gap. Which test/monitor would have caught it?
6. **Repair**: how data was fixed (backfill, restatement), verification done, consumers informed.
7. **Action items**: owner, due date, ticket; categories prevent / detect / mitigate.

## Data-specific points
- Measure **time-to-detect** separately from time-to-fix; it is usually the larger number.
- Identify downstream copies (extracts, reverse ETL syncs, ML features) that also need correction.
- Record which decisions were made on bad data so owners can revisit them.

## Process
Draft within 2-3 business days; review meeting with producers and consumers; publish to a shared, searchable place; track action items to completion in regular reviews.

## Verify
Quarterly: action items closed, and recurring incident categories decreasing.
