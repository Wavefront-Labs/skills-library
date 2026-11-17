---
id: computing-software.cybersecurity-defensive.security-operations.alert-queue-prioritisation
name: alert-queue-prioritisation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [alert-queue-prioritisation, alert-triage, soc, sla, alert-fatigue, risk-based-alerting, queue-management]
level: practitioner
status: draft
description: "Prioritise a SOC alert queue: ordering by severity x asset criticality x confidence, SLA timers, grouping, and handling overload without losing true positives."
sources: ["https://www.splunk.com/en_us/blog/security/risk-based-alerting.html", "https://www.sans.org/white-papers/", "https://learn.microsoft.com/en-us/defender-xdr/incident-queue"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Alert queue prioritisation

## Order of work
Sort by a priority score, not arrival time:
`priority = alert severity (rule fidelity x impact) x asset/identity criticality x signal confidence`
- Rule fidelity from history: true-positive rate per rule over 90 days.
- Criticality from asset/identity data (domain controllers, executives, crown-jewel apps).
- Confidence boosts: multiple detections on the same entity, threat intel match, EDR prevented vs
  only detected.
Implement as urgency (Splunk ES), incident severity plus tags (Sentinel/Defender), or a SOAR
enrichment step writing a score.

## SLAs
Per priority, e.g. P1 acknowledge 15 min / triage 1 h; P2 1 h / 4 h; P3 4 h / next business day;
P4 batch weekly. Display SLA remaining in the queue; page on P1 breach.

## Reduce queue volume
- Group: one incident per entity per time window (Sentinel alert grouping, Defender correlation,
  SOAR dedup by entity+rule).
- Suppress duplicates for already-open incidents.
- Route informational/low-fidelity signals to risk scoring instead of the queue.

## Overload protocol
1. Freeze P4 work; triage P1/P2 only.
2. Bulk-review by rule: if one rule floods, sample 10 alerts; if all benign, temporarily suppress
   with a ticket to tune and an expiry.
3. Call in on-call/second shift per escalation matrix.
4. Record what was deferred; review after.

## Gotchas
- Never auto-close by age without review; adversaries benefit from backlog purges.
- "Severity" from vendors is not your risk; recalibrate per environment.
- Track queue age percentiles (p50, p90), not only counts.

## Verify
Weekly: P1/P2 SLA attainment, p90 queue age, true positives found in deferred/batched work (should
be near zero; if not, re-rank).
