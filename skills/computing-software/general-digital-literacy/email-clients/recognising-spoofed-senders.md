---
id: computing-software.general-digital-literacy.email-clients.recognising-spoofed-senders
name: recognising-spoofed-senders
category: computing-software
field: general-digital-literacy
product: email-clients
tags: [email-clients, email-security, phishing, spoofed-sender, display-name-spoofing, lookalike-domain, reply-to, business-email-compromise, sender-verification]
level: intro
status: draft
description: "Spot spoofed and impersonated email senders: display-name tricks, lookalike domains, mismatched Reply-To, and urgent payment or gift-card requests from the boss."
sources:
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
  - https://www.cisa.gov/secure-our-world
  - https://consumer.ftc.gov/features/scam-alerts
  - https://support.google.com/mail
  - https://support.microsoft.com/en-us/outlook
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recognising spoofed senders

**Goal:** know when an email only pretends to come from someone you trust.

## Tricks to look for
- **Display name only:** "PayPal Support" <support@pp-secure-help.com>. Click/tap the name to
  reveal the real address. On phones the address is hidden by default.
- **Lookalike domains:** `rnicrosoft.com` (r+n), `paypa1.com`, `amazon-billing.co`,
  `yourcompany.co` instead of `.com`, extra words (`hmrc-refunds.uk`).
- **Reply-To differs** from From: hit Reply and check the To field before sending anything.
- **Free webmail** for a "CEO", "lawyer" or "supplier" (`ceo.office.urgent@gmail.com`).
- **External sender banners** (Microsoft 365, Google Workspace) on mail that claims to be internal.

## Typical scenarios
- "Boss" asks for gift cards, an urgent wire transfer or to keep it confidential.
- "Supplier" says bank details have changed for the next invoice (business email compromise).
- "Bank/HMRC/IRS/delivery company" asks you to log in via a link.

## What to do
Verify through a **known channel**: call the number you already have (not one in the email), or
type the website address yourself. Payment detail changes always get a phone check. Then report it
(see `computing-software.general-digital-literacy.email-clients.checking-email-headers` to look deeper).

## Gotchas
- A genuine-looking address can still be a compromised real account; the request is the clue.
- Gmail/Outlook warnings ("This message seems dangerous", "be careful with this message") are worth
  heeding.

## Verify
- [ ] You can display the full sender address in your mail app on desktop and phone.
