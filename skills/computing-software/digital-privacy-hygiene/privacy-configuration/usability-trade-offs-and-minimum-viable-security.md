---
id: computing-software.digital-privacy-hygiene.privacy-configuration.usability-trade-offs-and-minimum-viable-security
name: usability-trade-offs-and-minimum-viable-security
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, security-tradeoffs, threat-modeling, minimum-viable-security, usability]
level: practitioner
status: docs-checked
description: "Pick a minimum viable security baseline people will actually keep, weigh usability against protection, and decide which extra steps are worth it."
sources:
  - "https://ssd.eff.org/module/your-security-plan"
  - "https://www.privacyguides.org/en/basics/threat-modeling/"
  - "https://www.cisa.gov/secure-our-world"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Usability trade-offs and minimum viable security

**Goal:** security that survives real life. A perfect setup abandoned after a week protects nothing.

## The baseline that covers most people (CISA Secure Our World)
CISA's page lists four core steps for everyone:
1. Avoid and report phishing scams.
2. Use strong passwords.
3. Use multifactor authentication and a password manager.
4. Update software.
Additions beyond the CISA page (this skill's judgement): device passcode and encryption, backups.

## Why trade-offs matter
Privacy Guides: everything is a trade-off, the more secure something is the more restricting or inconvenient it
generally is, and tools that are too hard to start using do not get used. There is high security, but never full
security. EFF: weigh convenience, cost and privacy against your risk assessment, and note your financial, technical
and social constraints.

## Weighing an extra step
Ask for each proposed measure:
- **What threat does it stop?** Is that threat in my plan?
- **Cost:** time per day, money, things it breaks (sites, sharing with family).
- **Failure mode:** what happens when I get it wrong (locked out forever vs mild inconvenience)?
- **Will I still do it in six months?**

Illustrative judgements (this skill's own, not from the cited pages):

| Example | Usually worth it | Often not worth it for average risk |
|---|---|---|
| Passkeys / security keys on email | Yes | |
| Tor for daily browsing | | Slower and breaks some sites; use when needed |
| Disabling JavaScript everywhere | | Constant breakage |
| Separate phone for banking | High-risk only | |

## Signs a setting is too strict
Workarounds appear: passwords written on notes, 2FA turned off "temporarily", family sharing passwords by text.
Loosen it and fix the root cause instead.

## Gotchas
- Different household members can need different baselines; protect shared accounts to the highest one.
- Re-assess after life changes (new job, public role, separation); EFF says to revisit the plan frequently.

## Checked
Checked 2026-11-08 against the full text of EFF "Your Security Plan", Privacy Guides "Threat Modeling" and the CISA
Secure Our World page (read through a page fetch; it lists four core steps). Corrected the baseline to CISA's four
steps, flagged additions and the example table as this skill's own judgement, and removed the Lockdown Mode row
and the claim that MFA belongs on specific accounts.
Method: documentation only; no commands were run.
