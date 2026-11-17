---
id: computing-software.digital-privacy-hygiene.two-factor-auth.government-portal-sign-in-security
name: government-portal-sign-in-security
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, login-gov, mfa-rollout, security-keys]
level: practitioner
status: draft
description: "Secure Login.gov and ID.me accounts used for the IRS, Social Security and benefits: phishing-resistant methods, backup methods and recovery."
sources:
  - "https://www.login.gov/help/get-started/authentication-methods/"
  - "https://help.id.me/hc/en-us/articles/360017833054"
  - "https://www.ssa.gov/myaccount/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Government portal sign-in security

**Goal:** the accounts that unlock your tax records, benefits and Social Security can't be taken over to redirect
refunds or payments.

## Login.gov methods (strongest first)
1. Security key (FIDO).
2. Face or touch unlock (passkey on your device).
3. PIV/CAC card (government employees).
4. Authentication app.
5. Backup codes.
6. Text/voice (weakest).
Login.gov asks for at least two methods; pick a security key and an authenticator app, plus backup codes on paper.

## ID.me
Account > Sign in & security: enable an authenticator app or security key; remove SMS if alternatives are set;
review devices.

## Where they're used (US)
IRS online account, SSA my Social Security, USAJOBS, VA, SBA, many state agencies.

## Recovery
- Login.gov: if you lose all methods, you must delete and recreate the account (identity verification again).
  That's why two methods plus backup codes matter.
- Keep the email on the account protected with strong 2FA.

## Gotchas
- Scam texts mimic IRS/SSA login prompts; type login.gov / irs.gov yourself.
- Create these accounts **before** a criminal does with your SSN; an existing account blocks them.
