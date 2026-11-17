---
id: computing-software.general-digital-literacy.email-clients.invoice-and-payment-change-fraud
name: invoice-and-payment-change-fraud
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, phishing, invoice-fraud, business-email-compromise, payment-diversion]
level: practitioner
status: draft
description: "Spot and stop invoice and bank-detail change fraud by email: verify payment changes by phone, red flags, and what to do within hours if money was sent."
sources:
  - https://www.ncsc.gov.uk/collection/phishing-scams
  - https://www.ic3.gov
  - https://www.actionfraud.police.uk
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Invoice and payment-change fraud

**The scam:** a criminal (often inside a hacked supplier or customer mailbox, or a lookalike domain)
emails "our bank details have changed, please pay the attached invoice to this account". Also hits
home buyers (solicitor deposit), tradespeople and HR (salary bank change).

## Red flags
- Any change of bank details, especially near a payment date.
- Urgency or secrecy ("CEO in a meeting, pay today, don't call").
- Sender address subtly different (`accounts@acme-ltd.co` vs `acme.co.uk`), or reply-to differs
  from the From address.
- Reply is in the middle of a real thread (attacker in the mailbox).
- Bank name/country doesn't match the supplier.

## The control that works
**Verify every bank-detail change by calling a number you already have** (contract, previous invoice,
official website), never one in the email. Two people approve changes and first payments. Send a
small test payment and confirm receipt by phone.

## If you've paid
1. **Call your bank immediately** (hours matter) and ask for a recall / fraud claim. UK: also
   ask about the APP fraud reimbursement scheme.
2. Report: Action Fraud (UK) / IC3.gov (US) / local police cyber unit.
3. Tell the real supplier; they may have a hacked mailbox.
4. Check your own mailbox for forwarding rules and change passwords (they may be in yours).
5. Keep emails with full headers as evidence.

## Verify
- [ ] Written procedure: payment changes require a call-back to a known number and a second approver.
