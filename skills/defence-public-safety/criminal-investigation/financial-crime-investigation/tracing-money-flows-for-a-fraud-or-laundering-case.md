---
id: defence-public-safety.criminal-investigation.financial-crime-investigation.tracing-money-flows-for-a-fraud-or-laundering-case
name: tracing-money-flows-for-a-fraud-or-laundering-case
category: defence-public-safety
field: criminal-investigation
product: financial-crime-investigation
tags: [criminal-investigation, financial-crime-investigation, financial-investigation, fraud-investigation, money-laundering, aml, follow-the-money, bank-records, production-order, subpoena, sar, str, suspicious-activity-report, fiu, fincen, placement-layering-integration, net-worth-analysis, source-and-application-of-funds, flow-chart, i2-analyst-notebook, asset-restraint, confiscation, poca, civil-forfeiture, crypto-tracing]
level: advanced
status: draft
description: "Follow the money for prosecution: obtain records lawfully, build a transaction schedule, chart flows, use net-worth or source-and-application analysis, and restrain assets early."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracing money flows for a fraud or laundering case

**Goal:** prove where money came from, where it went and who controlled it, in a form a
jury can follow, and freeze it before it disappears. Financial evidence is unusually strong —
documents don't change their story — but only if the analysis is accurate and sourced.

## 1. Frame the case
- **Fraud:** what was the false representation (or abuse of position, or failure to disclose),
  who was deceived, what was obtained? Quantify loss per victim.
- **Laundering:** the stages placement → layering → integration are a model, not elements;
  the offence elements are usually dealing with property that is (known/suspected to be)
  criminal proceeds. Identify the predicate criminality you can prove, or the circumstances
  from which criminal origin can be inferred.
- Set the **relevant period** and the accounts/entities in scope early, or the data explodes.

## 2. Obtain records lawfully
- Banks and institutions: production orders/account monitoring orders (UK POCA 2002),
  grand jury subpoenas or warrants (US). Request statements, account-opening documents,
  signature cards, KYC files, device/IP data for online banking, and correspondence.
- Financial intelligence: Suspicious Activity Reports via the FIU (UK NCA; US FinCEN).
  SARs are intelligence and their existence is usually not disclosed to the subject or shown
  in court — use them to direct production orders.
- Company records, land registry, vehicle registers, tax data (via proper gateways),
  overseas records by Mutual Legal Assistance (slow — request early).
- Seized devices and paperwork often reveal accounts you didn't know about.

## 3. Build the transaction schedule
- Import statements into a structured spreadsheet/database: date, account, counterparty,
  amount, direction, description, source reference (exhibit and page).
- Reconcile opening/closing balances against the bank's figures — if they don't reconcile,
  your import is wrong.
- Tag transactions: victim inflows, transfers between controlled accounts, cash withdrawals,
  spending on assets, onward transfers out of reach.

## 4. Analyse
- **Flow charts** (e.g. i2 Analyst's Notebook or equivalent): show money moving from victims
  through layers to end uses. Keep court charts simple; detail lives in the schedule.
- **Source and application of funds:** all money in vs all money out over the period;
  unexplained credits are the issue.
- **Net-worth method:** change in assets plus living expenses minus legitimate income =
  unexplained income. Classic for tax and proceeds cases; living-expense estimates must be conservative.
- **Cash:** structuring below reporting thresholds is itself evidence of intent in many regimes.
- **Crypto:** blockchain analytics can trace flows through addresses; exchanges with KYC
  are the identification points. Tools give probabilistic clustering — present it as such.

## 5. Restrain early
Apply for restraint/freezing orders (UK POCA restraint orders, account freezing orders;
US seizure warrants and forfeiture) as soon as the risk of dissipation is evident — usually
before the suspect learns of the investigation. Confiscation/forfeiture after conviction
depends on what was preserved.

## 6. Presenting it
An independent financial investigator or forensic accountant produces a statement
explaining method, sources and assumptions. Every figure traces back to an exhibit page.

## Gotchas
- Transcription errors in a 50,000-row schedule; use imports and reconciliation, not retyping.
- Charting every transaction until the chart is unreadable.
- Overlooking legitimate explanations (loans, inheritances) that the defence will produce.
- Tipping off subjects through careless enquiries with small institutions.

## Verify
- [ ] Every account in scope has complete, reconciled statements for the period.
- [ ] Each charted flow links to schedule rows and exhibit references.
- [ ] Legitimate-income explanations considered and documented.
- [ ] Restraint considered at the outset and recorded.

*Uncertainty:* UK/US legal tools summarised; procedures and thresholds differ by jurisdiction.
