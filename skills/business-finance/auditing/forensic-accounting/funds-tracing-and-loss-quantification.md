---
id: business-finance.auditing.forensic-accounting.funds-tracing-and-loss-quantification
name: funds-tracing-and-loss-quantification
category: business-finance
field: auditing
product: forensic-accounting
tags: [forensic-accounting, auditing, fraud-examination, funds-tracing, flow-of-funds, bank-statement-analysis, source-and-application-of-funds, net-worth-method, lowest-intermediate-balance-rule, fifo-tracing, commingled-funds, loss-quantification, embezzlement, asset-misappropriation, chain-of-custody, cfe, acfe, expert-report, litigation-support, disbursement-fraud, shell-company]
level: advanced
status: draft
description: "Trace misappropriated funds through bank records and quantify the loss defensibly: evidence preservation, a flow-of-funds schedule, commingling rules, and a reconcilable loss calculation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Funds tracing and loss quantification — follow the money so it stands up

**Goal:** show where the money went, transaction by transaction, and produce a loss figure
that reconciles to source records and survives challenge by the other side's expert.

## 1. Preserve evidence first
- Before anyone confronts a suspect, secure records: export accounting data and audit
  logs, image relevant laptops and mailboxes (forensic IT, not "copy the folder"), and
  stop any routine deletion.
- Keep a **chain of custody**: who obtained each item, when, from where, how it was stored.
- Work on copies; keep originals untouched. Note hashes for electronic evidence.
- Agree scope and privilege with counsel early — in many jurisdictions work done at
  counsel's direction can be privileged; work done ad hoc may be disclosable.

## 2. Get the right records
- Company bank statements and payment files for the full period (and a buffer before it).
- The accounting ledger, vendor master file change history, payroll records.
- For outflows to third parties: account details from payment instructions. Records of
  the recipient's account usually need a court order, subpoena or the recipient's consent —
  *the mechanism varies by jurisdiction; counsel obtains these*.
- Request statements as bank-issued originals or direct from the bank; PDFs from the
  suspect can be edited.

## 3. Build the flow-of-funds schedule
One row per transaction: date, source account, destination account, amount, reference,
supporting document, and your classification (legitimate / suspicious / unexplained).
- Start from the known suspicious payments and follow each hop.
- Match amounts across accounts, allowing for fees, FX and splits/aggregations.
- Visualise with a flow diagram (accounts as boxes, totals on arrows) — it's what a judge,
  board or jury will actually look at.
- Look for patterns: round sums, payments just under approval limits, new vendors sharing
  an address or bank account with an employee, payments on weekends, sequential invoice
  numbers from a "supplier".

## 4. Commingled funds
When stolen money lands in an account with legitimate money and some is spent, you need a
tracing convention. Common ones (legal acceptance varies):
- **Lowest intermediate balance rule (LIBR)** — the traceable amount can't exceed the
  lowest balance the account fell to after the deposit. Widely used in US and
  common-law tracing.
- **FIFO / LIFO** conventions, or pro-rata allocation.
State the method and why, and show the result under alternatives if they differ materially.
*Which rule a court applies is a legal question — confirm with counsel.*

## 5. Quantify the loss
- **Direct loss** = sum of misappropriated amounts, less legitimate value received, less
  recoveries. Show it reconciling: total suspicious outflows → exclusions → net loss.
- Add **consequential costs** only where the claim allows: investigation costs, lost
  interest (state the rate and method), tax penalties caused by the fraud.
- Where records are missing, indirect methods (net worth, source and application of funds)
  can estimate unexplained income — label them as estimates with stated assumptions.
- Give ranges where judgement drives the number; never overstate.

## 6. Report
Write for a non-accountant: scope, sources relied on, methods, findings, the loss figure
and limitations. Every number in the report must tie to a schedule; every schedule line
to a document. Separate **facts** from **opinions**; guilt or intent is for the court, not
the accountant. If you may be an expert witness, follow the court's expert-duty rules
(independence to the court, not to the client).

## Gotchas
- Confronting or tipping off the suspect before evidence is secured.
- Using the suspect's own reconciliations or spreadsheets as evidence of the true position.
- Double counting a payment that moved through several accounts.
- Ignoring legitimate offsets (genuine goods actually received) — the other side won't.
- Working outside your competence on digital forensics; hire it in.

## Verify
- [ ] Evidence preserved with chain-of-custody notes before any interviews.
- [ ] Flow-of-funds schedule ties every transaction to a source document.
- [ ] Commingling method stated and justified, alternatives shown if material.
- [ ] Loss figure reconciles from gross outflows to net loss with each adjustment explained.
- [ ] Report separates fact from opinion and lists limitations.

Related: business-finance.compliance.internal-compliance-investigations; business-finance.auditing.audit-analytics.
