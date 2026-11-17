---
id: computing-software.digital-privacy-hygiene.two-factor-auth.prioritising-accounts-for-mfa
name: prioritising-accounts-for-mfa
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, mfa-priority-list, mfa-rollout, multi-factor-authentication, account-inventory, reset-chain, cisa-secure-our-world, 2fa]
level: intro
status: draft
description: "Order the MFA rollout by blast radius (vault, email, phone carrier, platform accounts, money, then the rest) so one evening protects most of what matters."
sources:
  - "https://www.cisa.gov/secure-our-world/turn-mfa"
  - "https://ssd.eff.org/module/how-enable-two-factor-authentication"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prioritising which accounts get MFA first

**Goal:** people abandon "turn on 2FA everywhere" at account 6. Do the accounts that
can reset or drain others first.

## Priority tiers
**Tier 0 (tonight)**
1. Password manager account.
2. Primary email (and any email that is the recovery address for others).
3. Mobile carrier account (port-out PIN too).
4. Apple / Google / Microsoft account (device and backup root).

**Tier 1 (this week)**
5. Banks, brokerage, pensions, PayPal, crypto exchanges.
6. Domain registrar and DNS (if you own a domain used for email).
7. Cloud storage holding documents (often the same as tier 0 platforms).
8. Work-critical accounts not covered by employer SSO (GitHub, cloud consoles).

**Tier 2 (this month)**
9. Social media and messaging (scam vector to friends).
10. Shopping with stored cards (Amazon, eBay), utility and tax portals.

**Tier 3 (as you log in)**
Everything else with "Enable 2FA" available. The password manager's "inactive 2FA"
report lists sites that support 2FA where you haven't turned it on (it uses the 2fa.directory
dataset).

## How to find the reset chain
For each Tier 0/1 account, write: "resets via -> email X / phone Y". If several
point to one email, that email is your most important account.

## Verify
- [ ] Tier 0 complete with phishing-resistant method where offered.
- [ ] Reset-chain note written; every email in it is MFA-protected.
