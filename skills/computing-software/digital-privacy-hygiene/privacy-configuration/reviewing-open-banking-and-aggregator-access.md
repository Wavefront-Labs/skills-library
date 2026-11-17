---
id: computing-software.digital-privacy-hygiene.privacy-configuration.reviewing-open-banking-and-aggregator-access
name: reviewing-open-banking-and-aggregator-access
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, open-banking-access, plaid, financial-privacy, data-aggregators]
level: practitioner
status: draft
description: "Find and revoke budgeting apps, Plaid connections and open-banking consents that can read your bank transactions, and handle shared login risks."
sources:
  - "https://my.plaid.com/"
  - "https://www.openbanking.org.uk/"
  - "https://www.consumerfinance.gov/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reviewing open-banking and aggregator access

**Goal:** know which apps can still read your bank accounts, and cut off the ones you no longer use.

## Where access is granted
- **US aggregators (Plaid, MX, Finicity, Yodlee)** connect budgeting, investing and payment apps to your bank, via API
  tokens or (older) screen scraping with your bank password.
- **UK/EU open banking (PSD2)**: you grant a regulated provider consent through your bank's app; the bank lists active
  consents.

## Review
1. **Plaid**: sign in at **my.plaid.com** with your phone number; see every app connected via Plaid and disconnect.
2. **Your bank app**: look for "Connected apps", "Third-party access", "Open banking", or "Data sharing"; revoke unknown
   or unused ones.
3. **The apps themselves**: delete the account in old budgeting apps (Mint shut down in 2024; its connections should be
   gone, but check).
4. **Payment apps** (PayPal, Venmo, Cash App, Wise): linked banks list.

## Prefer
- API/OAuth connections over giving your bank password to an app; if you gave it, change the bank password.
- Read-only access for budgeting tools.
- Apps that state data retention and don't sell transaction data.

## Rules in flux
The US CFPB's personal financial data rights rule (Section 1033, finalised in 2024) has faced litigation and
revision; rights and timelines may change. UK consents are regulated by the FCA.

## Gotchas
- Revoking access in the app doesn't always revoke the bank token; revoke at the bank too.
- Transaction data reveals health, religion, relationships and location as much as any app.
