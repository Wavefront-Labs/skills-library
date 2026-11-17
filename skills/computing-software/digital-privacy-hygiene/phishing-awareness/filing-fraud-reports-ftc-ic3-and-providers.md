---
id: computing-software.digital-privacy-hygiene.phishing-awareness.filing-fraud-reports-ftc-ic3-and-providers
name: filing-fraud-reports-ftc-ic3-and-providers
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, ftc-report, ic3-report, report-to-provider, report-phishing, reportfraud-ftc-gov, report-phishing-apwg, google-safe-browsing-report, action-fraud]
level: intro
status: draft
description: "Report phishing and scams to the right places: FTC (reportfraud.ftc.gov), FBI IC3, the impersonated company, email/SMS providers, Safe Browsing and APWG; what each does."
sources:
  - "https://reportfraud.ftc.gov/"
  - "https://www.ic3.gov/"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
  - "https://apwg.org/reportphishing/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Filing fraud reports

**Goal:** reports protect others (blocklists, takedowns) and support your own recovery.
Know which report does what.

## Where (US-centric; other countries noted)
| Report to | When | What it does |
|---|---|---|
| **reportfraud.ftc.gov** | Any scam or fraud, with or without loss | Feeds Consumer Sentinel used by law enforcement; gives next steps |
| **ic3.gov** (FBI) | Internet-enabled crime, especially money lost via wire/crypto/BEC | Investigations; Recovery Asset Team for recent wires |
| **identitytheft.gov** | Your identity was misused | FTC Identity Theft Report + recovery plan |
| **7726** | Spam/scam texts | Carriers block senders |
| Impersonated company | Fake bank/PayPal/Amazon email or site | Many have `phishing@` or `reportphishing@` addresses (check their site) |
| Email provider | Phishing email | Gmail "Report phishing", Outlook "Report > Phishing" trains filters |
| Browser/Safe Browsing | Phishing website | Google Safe Browsing report form / browser "Report deceptive site"; blocks site for Chrome/Firefox/Safari users |
| APWG | Phishing emails/URLs | Forward to `reportphishing@apwg.org`; shared with industry |
| Platform | Scam accounts on social media/marketplaces | In-app report |
UK: Action Fraud / Report Fraud, forward emails to `report@phishing.gov.uk`, texts to 7726.

## Include
Full email (as attachment or with headers), URLs (defanged in prose: `hxxps://evil[.]tld`),
phone numbers, payment details, timeline, screenshots.

## Verify
- [ ] For a real loss: FTC + IC3 + bank reports filed with reference numbers saved.
