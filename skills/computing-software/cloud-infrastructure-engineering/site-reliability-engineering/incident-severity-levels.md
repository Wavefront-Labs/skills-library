---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-severity-levels
name: incident-severity-levels
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, incident-management, incident-severity-levels, sev1, declaring-incidents, escalation]
level: practitioner
status: docs-checked
description: "Define incident severity levels with objective criteria and typical responses, treat unclear cases as the higher level, and decide which levels count as major incidents."
sources: ["https://response.pagerduty.com/before/severity_levels/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident severity levels

**Goal:** everyone classifies incidents the same way and severity drives the response. The structure below
follows the PagerDuty incident response documentation, which says its levels are generic versions of its
internal definitions.

## Scheme (PagerDuty example)
Lower numbers are more urgent, and at higher severity you can take riskier moves to resolve. Anything above
SEV-3 is a "major incident" with a more intensive response.
| Sev | Meaning (examples from the page) | Typical response |
|---|---|---|
| SEV-1 | Critical, actively impacting a large number of customers; long severe impairment breaking SLA; customer-data-exposing security vulnerability | Major incident response: page an incident commander, notify internal stakeholders, public notification |
| SEV-2 | Critical system issue actively impacting many customers; core functions severely impaired; app unavailable or severely degraded for most users | Major incident response, page an IC |
| SEV-3 | Stability or minor customer-impacting issues needing immediate attention; partial loss of functionality; could become SEV-2; no redundancy left | High-urgency page to the service team; prioritise; roll back if tied to a recent deploy; trigger incident response if needed |
| SEV-4 | Minor issues not affecting customers' ability to use the product (performance delays, single host failure, non-critical job failures) | Low-urgency page to the service team |
| SEV-5 | Cosmetic issues or bugs | Ticket assigned to the owner |

## Rules from the page
- If unsure between two levels, treat the incident as the higher one; do not argue severity during the incident,
  review it in the postmortem.
- Not every major incident must be SEV-2: if you need a coordinated response, trigger the incident process
  anyway; the incident commander decides whether full response is needed.
- Make your own definitions specific and metric-driven, usually referring to a percentage of users or accounts
  affected, and publish them where responders look.

## Checked
2026-11-01. Confirmed against the PagerDuty incident response page Severity Levels: the five levels, major
incident threshold, higher-level-when-unsure rule, IC determination, metric-driven advice. Removed: comms
cadences, error-budget burn thresholds, mandatory postmortem rule and four-to-five level limit, which the page
does not state.
Method: documentation only; no commands were run.
