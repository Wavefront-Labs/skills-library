---
id: computing-software.digital-forensics-incident-response.incident-response-process.bec-wire-fraud-recall
name: bec-wire-fraud-recall
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [wire-recall, business-email-compromise, bec, financial-fraud, ic3, fraud-response, dfir]
level: practitioner
status: draft
description: "Respond to BEC wire fraud: immediate bank recall, the FBI IC3 Financial Fraud Kill Chain, evidence for the bank and insurer, and stopping further payments."
sources: ["https://www.ic3.gov/", "https://www.fbi.gov/how-we-can-help-you/scams-and-safety/common-scams-and-crimes/business-email-compromise"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BEC wire fraud recall

**Goal:** recover money sent to a fraudster's account. Speed decides everything: recall
success drops sharply after 24-72 hours as funds move.

## First hour
1. **Call your bank's fraud desk** (not the relationship manager by email). Request a wire
   recall / SWIFT gpi recall (or ACH reversal) citing fraud. Get a reference number.
2. **File with FBI IC3** (ic3.gov) immediately; for qualifying US domestic wires
   (generally recent, above a threshold) the **Financial Fraud Kill Chain** lets FBI work
   with FinCEN and the receiving bank to freeze funds. Include all transaction details.
3. Contact the receiving bank's fraud department directly if known.
4. Notify the cyber insurer (social engineering/fraud coverage often has specific conditions).

## Information to have ready
Sending account, amount, currency, date/time, beneficiary name/account/IBAN/SWIFT, receiving
bank, intermediary bank, MT103/payment reference, the fraudulent emails with full headers,
and the legitimate counterparty's real details.

## Stop the bleeding
- Freeze pending payments to the fraudulent account and any recently changed vendor bank
  details; call vendors on known phone numbers to verify.
- Investigate the mailbox compromise (yours or the vendor's): inbox rules, sign-ins,
  lookalike domains (`contoso-inc.example` vs `contoso.example`).
- Report lookalike domains to the registrar for takedown.

## Prevent recurrence
Out-of-band verification for any bank detail change (call-back to a number on file), dual
approval for payments over threshold, DMARC enforcement, external email tagging.

## Gotchas
- Whose mailbox was compromised determines liability discussions; preserve evidence on
  both sides.
- International wires are much harder to recall; act faster, not slower.

## Verify
Track recall status with the bank daily; document recovered amount and file a final update
with IC3.
