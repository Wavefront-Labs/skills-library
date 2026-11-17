---
id: business-finance.risk-management.operational-risk-management.rcsa-loss-events-and-kris
name: rcsa-loss-events-and-kris
category: business-finance
field: risk-management
product: operational-risk-management
tags: [operational-risk-management, risk-management, operational-risk, oprisk, rcsa, risk-and-control-self-assessment, process-mapping, control-design, control-effectiveness, loss-event-data, incident-management, near-miss, basel-event-types, key-risk-indicators, kri, thresholds, remediation-tracking, issue-management, root-cause, second-line, three-lines-model, operational-resilience]
level: practitioner
status: draft
description: "Run the core operational-risk toolkit: a process-based RCSA that challenges self-scores, loss-event and near-miss capture with root cause, KRIs with thresholds, and remediation tracked to closure."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RCSA, loss events and KRIs — the operational-risk toolkit that actually works

**Goal:** find where processes, people and systems can fail before they do, learn from the
failures that happen, and track early signals — using three linked tools rather than three
separate compliance exercises.

## 1. Risk and control self-assessment (RCSA)
Run per business process (e.g. "supplier payments", "client onboarding"), not per department.
1. **Map the process** at a level of 8–15 steps with the people who run it.
2. For each step ask what can go wrong: errors, fraud (internal/external), system failure,
   third-party failure, legal/regulatory breach, people dependency.
3. Score **inherent risk** (impact × likelihood on the ERM scales).
4. List the **controls** for each risk: preventive or detective, manual or automated, frequency,
   owner, evidence. Rate **design** (would it work?) and **operating effectiveness** (does it?).
5. Score **residual risk** and decide: accept, or raise an action.

**Second-line challenge is the point.** Self-assessments drift optimistic. Challenge scores
with evidence: recent incidents, audit findings, KRI trends, control test results. A
"strong" control with three incidents last quarter isn't strong.

## 2. Loss events and near misses
Capture every operational event above a threshold (and near misses below or at zero loss):
- date of occurrence, discovery and recognition; business unit; process;
- **event type** — Basel's seven level-1 categories are a widely used taxonomy: internal
  fraud; external fraud; employment practices and workplace safety; clients, products and
  business practices; damage to physical assets; business disruption and system failures;
  execution, delivery and process management;
- gross loss, recoveries (insurance, chargebacks), net loss;
- **root cause** (people, process, systems, external) and the failed or missing control.
Then **link** the event back to the RCSA: was this risk identified? Was the control rated
effective? If yes, the RCSA was wrong — update it.
Set a low reporting threshold (some firms use zero) and celebrate near-miss reporting;
otherwise people hide small events and you only learn from big ones.

## 3. Key risk indicators (KRIs)
Pick metrics that move **before** losses: failed reconciliations aged > 5 days, manual
payment overrides, system downtime minutes, staff turnover in a key team, overdue access
reviews, open audit actions past due, complaints volume, trade breaks.
For each: definition, data source, owner, frequency, and **green/amber/red thresholds**
calibrated to appetite. Amber requires a documented response; red escalates.
Retire KRIs that never move or never predict anything.

## 4. Remediation tracking
Every action from RCSA, events, KRI breaches or audit gets: owner, due date, closure
evidence, and second-line validation for higher-rated items. Report overdue actions by
age and owner — overdue remediation is itself a KRI.

## 5. Bring it together
Quarterly operational-risk report per business area: top residual risks, material events
and root causes, KRI dashboard, overdue actions, and the themes that cut across them (e.g.
"manual workarounds after system migration appear in 4 events, 2 KRIs and the RCSA").

## Gotchas
- RCSA as a once-a-year spreadsheet refresh copied from last year.
- Too many risks (hundreds per process) — nobody can manage them; consolidate.
- Controls described as policies ("we have a policy") rather than actions someone performs.
- Loss data with no root cause is just accounting.
- KRIs that are really lagging loss metrics (e.g. "number of frauds").
- Boundary events: credit or market losses caused by an operational failure (a wrong
  trade booking) should be flagged so they aren't missed in either data set.

## Verify
- [ ] RCSA built from a process map; controls have owners, frequency and evidence.
- [ ] Residual scores challenged with incident, audit and KRI evidence.
- [ ] Loss events record dates, event type, gross/net loss, root cause and failed control.
- [ ] Each KRI has a definition, owner, source and thresholds; breaches have responses.
- [ ] Remediation actions tracked to validated closure; overdue items reported.

Related: business-finance.risk-management.enterprise-risk-management.risk-register-and-appetite-statement; business-finance.auditing.internal-controls-testing.
