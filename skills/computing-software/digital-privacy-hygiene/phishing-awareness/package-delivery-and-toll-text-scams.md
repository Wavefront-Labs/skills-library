---
id: computing-software.digital-privacy-hygiene.phishing-awareness.package-delivery-and-toll-text-scams
name: package-delivery-and-toll-text-scams
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, delivery-scam-text, toll-text-scam, smishing, card-harvesting, reply-y-trick, 7726, sms-spam-filtering]
level: intro
status: draft
description: "Spot 'your package can't be delivered' and 'unpaid toll' texts that harvest card details, why they ask you to reply Y, and what to do if you entered card data."
sources:
  - "https://consumer.ftc.gov/articles/how-recognize-and-report-spam-text-messages"
  - "https://www.ic3.gov/PSA/2024/PSA240412"
  - "https://www.usps.com/smishing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Package delivery and toll text scams

**Goal:** these mass smishing campaigns (USPS/Royal Mail/DHL redelivery fees, E-ZPass/
toll "unpaid balance", DMV fines) are the most common scam texts. Recognise them on sight.

## Tells
- Urgent small fee ($1.99 redelivery, $4.15 toll) with a penalty threat.
- Link to a lookalike domain (`usps-redelivery-help.top`, `ezpass-tolls.xyz`), often
  new TLDs, sometimes from email-to-SMS addresses or foreign numbers.
- "Reply Y and reopen this message to activate the link": iMessage disables links from
  unknown senders; replying enables them and confirms your number is live.
- Carriers and postal services don't text links asking for payment unless you signed up
  for tracking with that exact item.

## What to do
- Don't click or reply. Check deliveries by typing the carrier's site or in the retailer's
  app; tolls via your toll account directly.
- Report: forward to **7726** (SPAM) in the US/UK, use "Report Junk" in iMessage /
  "Report spam" in Google Messages, then delete.
- Turn on filtering: iPhone Settings > Apps > Messages > **Filter Unknown Senders**;
  Google Messages spam protection on.

## If you entered card details
Call the card issuer: cancel the card, review recent charges. The site may also have
taken your name/address/phone for follow-up "bank" calls, so expect vishing (see
`computing-software.digital-privacy-hygiene.phishing-awareness.bank-fraud-department-impersonation-calls`).
Some kits also capture a one-time code to add your card to the scammer's mobile wallet;
tell the bank if you entered a code.

## Verify
- [ ] Unknown sender filtering on; household knows "reply Y" is a trick.
