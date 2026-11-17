---
id: computing-software.general-digital-literacy.internet-navigation.security-questions
name: security-questions
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-authentication, security-questions, account-recovery, passwords]
level: intro
status: docs-checked
description: "Handle security questions safely: why real answers are guessable from social media, how to use random answers stored in a password manager, and when to replace them with 2FA."
sources:
  - https://pages.nist.gov/800-63-4/sp800-63b.html
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
  - https://www.cisa.gov/secure-our-world
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Security questions

## The problem
- "Mother's maiden name", "first pet", "school" are often on social media, family-history sites, or guessable. Attackers use them to reset passwords and phone-company accounts.
- NIST SP 800-63B (revision 4) says verifiers and credential providers shall not prompt subscribers to use knowledge-based authentication or security questions when choosing passwords; many services still do.

## Use fake, random answers
- Treat the answer as a password: "First pet?" > `correct-violin-harbour-58`.
- Store question and answer in your **password manager** entry for that account (notes field or custom fields).
- Spoken answers to phone support need to be pronounceable: use random words, not symbols.
- Different answers for every site.

## Prefer stronger recovery
- Where offered, replace questions with **2-step verification**, an authenticator app, passkeys, recovery codes and a recovery email/phone you control.
- Mobile carriers: set a PIN or password on the account (FTC advice against SIM swapping).

## Gotchas
- Social media quizzes that ask for a first pet, street or school can harvest answers; don't play.
- If you used real answers before, change them on important accounts (email, bank, carrier).

## Verify
- [ ] Important accounts have random answers saved in the password manager, or no questions at all.

## Checked

Checked 2026-10-27 against NIST SP 800-63B revision 4 and FTC SIM-swap advice. Confirmed: verifiers shall not prompt subscribers to use knowledge-based authentication or security questions when choosing passwords.

Method: documentation only; no commands were run.
