---
id: business-finance.banking.payments-operations.nostro-reconciliation-and-payment-exceptions
name: nostro-reconciliation-and-payment-exceptions
category: business-finance
field: banking
product: payments-operations
tags: [banking, payments-operations, payments, nostro, vostro, reconciliation, breaks, swift, mt103, mt940, mt950, iso-20022, camt-053, camt-056, pacs-008, pacs-004, gpi, uetr, payment-investigations, payment-repairs, suspense-account, maker-checker, settlement, clearing, correspondent-banking]
level: practitioner
status: docs-checked
description: "Reconcile nostro accounts daily, classify and age breaks, handle payment repairs, returns, investigations and recalls, and control suspense items with maker-checker."
sources: ["https://www.swift.com/standards/iso-20022/iso-20022-standards", "https://www.frbservices.org/resources/financial-services/wires/faq/iso-20022/format", "https://www.iso20022.org/catalogue-messages/iso-20022-messages-archive"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nostro reconciliation and payment exception handling

**Goal:** make sure every payment the bank sent or received actually settled as
recorded, and clear breaks and exceptions before they become losses, customer
complaints or regulatory issues.

*Draft: message names reflect SWIFT's move from MT to ISO 20022 (MX) for cross-border
payments; check which formats your bank and correspondents currently use. Swift ended coexistence for cross-border payment instructions on 22 November 2025, but statement messages (MT940/MT950) were not withdrawn then; Swift's roadmap maps them to camt.053 with a later end of coexistence, so check the current roadmap.*

## 1. What you're reconciling
- **Nostro** = the bank's account held at a correspondent ("our money at them").
  The correspondent's statement (MT940/MT950, or ISO 20022 **camt.053**; MT941/MT942 map to **camt.052** and debit/credit confirmations MT900/MT910 to **camt.054**) is matched against the bank's internal ledger.
- **Vostro** = accounts other banks hold with you. Also scheme settlement accounts
  (RTGS, ACH, card schemes) against their settlement reports.

## 2. Daily matching
1. Load statements and ledger entries into the reconciliation tool.
2. Auto-match on reference (end-to-end ID, **UETR** for SWIFT gpi payments,
   transaction reference), amount, value date and currency.
3. Work the unmatched items ("breaks"), classify each:
   - **Timing** — booked one side, not yet the other (cut-off, value-date).
   - **Amount difference** — usually correspondent charges deducted (charge code
     SHA/OUR/BEN mismatch) or FX conversion.
   - **Missing on statement** — payment not received/processed by the correspondent.
   - **Unknown credit** — money arrived with no matching instruction.
   - **Duplicate** — same payment sent twice.
4. Age breaks; escalate by age and amount (e.g. >3 days or > a set threshold →
   team lead; >30 days → finance/ops risk). *(Thresholds are bank-specific.)*

## 3. Exception handling for outgoing payments
- **Repairs:** payments failing validation (invalid IBAN/BIC, missing beneficiary
  data, sanctions hit). Fix only from the original instruction or by contacting the
  customer through a verified channel — never "guess" a beneficiary detail.
- **Sanctions/screening hits:** go to the screening team; ops must not release.
- **Returns/rejects** (pacs.004 / pacs.002 negative status): book the return,
  notify the customer, re-process only with corrected instructions.
- **Investigations:** beneficiary says funds not received → trace by UETR on gpi
  tracker, then query the correspondent. Recall/cancellation requests (e.g.
  **camt.056**, answered by **camt.029**) are requests, not guarantees: the receiving bank accepts or refuses the request in its camt.029 answer.

## 4. Unknown and suspense items
Park unidentified credits in a suspense account with an owner and an ageing limit.
Research using sender reference and ordering customer, contact the remitter's bank.
Never credit a customer on a "best guess". Return funds to the sender if unresolved
within policy time.

## 5. Controls
- Maker-checker on all manual matches, write-offs and repairs.
- Write-offs only within authority limits, with documented reason and GL impact.
- Daily sign-off of the nostro position; month-end certification.
- Report recurring break causes to fix them upstream (static data, charge settings).

## Gotchas
- **Payment fraud** often surfaces as "urgent" changes to beneficiary details or a
  recall request from a spoofed source — verify via known contacts.
- **Cut-off times** differ by currency and correspondent; late releases become
  value-date breaks and overdraft charges on the nostro.
- **Matching too loosely** (amount only) clears breaks wrongly and hides duplicates.
- Ageing must use value date, not booking date, for interest claims.

## Verify
- [ ] All nostros reconciled daily with breaks categorised and aged.
- [ ] No break above threshold is older than the escalation limit without an owner.
- [ ] Repairs trace back to an original instruction or verified customer contact.
- [ ] Suspense balances have owners and are within ageing policy.
- [ ] Manual matches and write-offs show maker-checker evidence.

## Checked

Date checked: 2026-10-25. Jurisdiction: International (Swift / ISO 20022); US Fedwire FAQ.
Sources read (via search results): Swift ISO 20022 standards and roadmap pages (MT940 and MT950 map to camt.053; MT941/MT942 to camt.052; MT900/MT910 to camt.054; coexistence for payment instructions ended 22 November 2025; statement messages were not withdrawn then); Federal Reserve Financial Services ISO 20022 FAQ (camt.056 is the return request, camt.029 accepts or refuses it, pacs.004 returns funds, pacs.002 reports status).
Operational thresholds (break ageing days) are bank-specific and already marked as such.

Method: documentation only; no commands were run.
