---
id: computing-software.digital-privacy-hygiene.phishing-awareness.recalling-a-scam-payment
name: recalling-a-scam-payment
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, payment-recall, phishing-incident-response, wire-recall, chargeback, zelle-fraud, gift-card-refund, crypto-scam, ic3-report]
level: practitioner
status: draft
description: "Maximise the chance of getting money back after a scam: payment-method-specific steps (card chargeback, wire recall, Zelle/ACH, gift cards, crypto) in the first hours."
sources:
  - "https://consumer.ftc.gov/articles/what-do-if-you-were-scammed"
  - "https://www.ic3.gov/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recalling a scam payment

**Goal:** speed matters more than anything; recovery chances drop sharply after the
first 24-72 hours.

## By payment method (FTC guidance, summarised)
| Paid with | Do now |
|---|---|
| Credit/debit card | Call issuer: report fraud, dispute charge (**chargeback**), new card |
| Bank transfer / ACH / wire | Call bank fraud dept: request **recall/reversal**; for wires ask them to send a recall and contact the receiving bank; file **IC3** quickly (FBI's Recovery Asset Team works on recent large wires) |
| Zelle / P2P (Venmo, Cash App, PayPal) | Report in the app and to your bank; policies differ for "authorised" payments, push anyway |
| Gift cards | Contact the card issuer (number on the card/receipt) immediately; keep the cards and receipts |
| Cryptocurrency | Contact the exchange you sent from; report to IC3 with transaction hashes; recovery is rare |
| Cash by mail/courier | Contact USPS/courier to intercept if in transit; police report |
| Money transfer (Western Union, MoneyGram) | Call their fraud line to stop pickup |

## Also
- Police report (some institutions require it).
- Gather evidence: messages, numbers, transaction IDs, timestamps.
- Beware **recovery scams** (see
  `computing-software.digital-privacy-hygiene.phishing-awareness.avoiding-recovery-scams-after-a-loss`).

## Verify
- [ ] Every payment channel used has a fraud report with reference number.
- [ ] IC3 filed within 72 hours for transfers.
