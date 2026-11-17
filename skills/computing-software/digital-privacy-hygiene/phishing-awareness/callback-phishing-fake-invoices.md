---
id: computing-software.digital-privacy-hygiene.phishing-awareness.callback-phishing-fake-invoices
name: callback-phishing-fake-invoices
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, callback-phishing, tech-support-scam, remote-access-scam-cleanup]
level: practitioner
status: draft
description: "Spot callback phishing: fake renewal invoices from Geek Squad, Norton, PayPal or McAfee that push you to call a number where scammers take remote control."
sources:
  - "https://consumer.ftc.gov/articles/how-spot-avoid-and-report-tech-support-scams"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Callback phishing fake invoices

**Goal:** never call the number in an unexpected invoice.

## How it works
Email or PDF "invoice" for an auto-renewal you don't recognise (antivirus, Geek Squad, PayPal, Amazon, crypto
exchange), often $300-$600, with "call us within 24 hours to cancel". No links, so filters pass it. On the phone, a
"refund agent" asks you to install a remote-access tool (AnyDesk, TeamViewer, ScreenConnect), then "accidentally"
refunds too much and asks you to send the difference, or logs into your bank.

## Spot it
- You don't have that subscription, or not with that company.
- Sent from a free email account or unrelated domain; the PDF has the phone number as the only action.
- Amount is large enough to scare, small enough to be plausible.

## Verify
Log into the real account (typed URL/app) and check subscriptions and charges. Check your card statement. Call the
company using the number on its official website.

## If you called
- Hang up as soon as they ask to install software or access your bank.
- If they connected: see remote-access scam cleanup (disconnect, uninstall tool, scan, change passwords, call bank).

## Gotchas
- Scammers also use real PayPal/QuickBooks invoice features, so the email comes from a legitimate domain; the phone
  number in the note is the tell.
