---
id: engineering-technology.chemical-engineering.process-safety.hazop-recording-and-action-tracking
name: hazop-recording-and-action-tracking
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-hazard-identification, hazop-recording-and-action-tracking, hazop-report, hazop-worksheet, action-tracking, recommendations, revalidation, pha-report, closure, risk-ranking]
level: practitioner
status: verified
description: "Record HAZOP results (worksheet fields, wording, risk ranking) and track recommendations to closure with owners, dates, management of change and revalidation."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HAZOP recording and action tracking

**Goal:** a record that stands up to audit and drives actions to completion.

## Worksheet fields
Node, deviation (guideword and parameter), cause, consequence, safeguards, severity/likelihood/risk rank (as per the matrix), recommendation, action number, responsible person, due date, status. Add comments, drawing references and the documents reviewed.

## Writing quality
- Causes: specific equipment or events ("FV-101 fails closed").
- Consequences: what happens to people, environment, assets, in physical terms ("overpressure of V-101 above MAWP, loss of containment of flammable liquid"), not just "trip".
- Safeguards: only items that are independent of the cause and actually present; name tags (PSV-101, PAH-101).
- Recommendations: actionable and not prescriptive of design when options exist ("evaluate high-level trip on V-101").

## Reporting
1. Draft the report within a few weeks of the sessions: scope, team attendance, drawings and revisions, methodology, risk matrix, worksheets, action list, and the key findings summary.
2. Circulate for review and agreement.

## Action tracking
1. Enter every recommendation in a tracking register (software or a controlled spreadsheet) with a due date and priority.
2. Responsible parties give written responses (accept, reject with reason, alternative) approved by the HAZOP leader or management.
3. Closure needs evidence (modified drawing, procedure issued, test result), not just a status change.
4. Changes resulting from actions go through **management of change** (see the `management-of-change` skill); high-risk actions must be completed before start-up or by a set deadline.
5. Report progress to management and keep the register for audits.

## Revalidation
Regulations may require periodic revalidation (at least every five years after the initial PHA under OSHA 29 CFR 1910.119(e)(6) in the United States, checked against the eCFR text; confirm the current requirement for your jurisdiction). Plan revalidations from the previous report and the changes since.

## Gotchas
- Actions without an owner and a date do not get done.
- Rejecting an action without a documented reason is a common audit finding.

## Verify
- [ ] Register shows every recommendation with owner, due date, response and closure evidence.
- [ ] Revalidation date set.
