---
id: engineering-technology.biomedical-engineering.device-verification-validation.capa-process
name: capa-process
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [capa-process, post-market-surveillance, capa, corrective-action, preventive-action, root-cause-analysis, effectiveness-check, nonconformance]
level: practitioner
status: gated
description: "Run a CAPA process: triggers, risk-based initiation, root cause tools, action plans, effectiveness checks and records under ISO 13485 and FDA expectations."
sources: ["ISO 13485 Medical devices - Quality management systems (clauses on corrective and preventive action; confirm edition)", "21 CFR Part 820 (QMSR) https://www.ecfr.gov/current/title-21/part-820", "ISO/TR 24971 Guidance on the application of ISO 14971 (risk linkage)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CAPA (corrective and preventive action)

Under the QMSR text of 21 CFR Part 820 (checked on eCFR, October 2026) the quality system requirement is 820.10, which requires a QMS complying with ISO 13485 (incorporated by reference in 820.7); the old stand-alone CAPA section 820.100 is not in the current part, so CAPA obligations come from the ISO 13485 clauses on corrective and preventive action (clause text (gated: unconfirmed, source is paywalled or blocked)).

**Goal:** fix the cause of real or potential nonconformities so they do not recur, and prove the fix worked.

## Triggers
Complaints and adverse events, nonconforming product, audit findings, trends in process or inspection data, supplier problems, returned products, management review, post-market surveillance signals, risk file updates.

## Process
1. **Intake and screening:** record the issue, source, product, quantity affected, date. Decide if a CAPA is warranted using a documented, risk-based rule (severity, frequency, regulatory impact); not every nonconformance needs a CAPA, but every decision is recorded.
2. **Containment and correction:** stop shipment, quarantine, segregate, rework or recall decisions; evaluate field actions (consult regulatory for reporting).
3. **Investigation and root cause:** collect data and use structured tools (5 whys, fishbone diagram, fault tree, comparison of good and bad lots, designed experiments). Verify the cause with evidence (reproduce it); "human error" is rarely a root cause alone: look at the system that allowed the error.
4. **Corrective and preventive action plan:** actions with owners, dates and resources; include extension to similar products, processes and suppliers (preventive scope). Examples: design change (see design-change-control), process validation update, training, supplier controls, labelling change, software fix.
5. **Verification or validation of the action before implementation** (and that it does not adversely affect the device).
6. **Implementation** with change control and updated documents (and update to the risk file).
7. **Effectiveness check** at a defined time with defined criteria (for example no recurrence in three consecutive lots or six months of complaint data; process capability restored; illustrative, set your own criteria). A CAPA is not closed on the basis of "actions completed" alone.
8. **Management review:** CAPA metrics (open, overdue, age, effectiveness failures), trends and resources.

## Gotchas
- Closing on completion of training as the only action.
- Effectiveness criteria that cannot fail.
- Missing the link to complaint trending and the risk file.

## Verify
- [ ] Each CAPA has risk rating, root cause evidence, plan and effectiveness criteria.
- [ ] Overdue CAPAs reviewed by management.
- [ ] Sample of closed CAPAs shows no recurrence.
