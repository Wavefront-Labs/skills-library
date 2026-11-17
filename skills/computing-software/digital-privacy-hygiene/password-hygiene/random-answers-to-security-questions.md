---
id: computing-software.digital-privacy-hygiene.password-hygiene.random-answers-to-security-questions
name: random-answers-to-security-questions
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, security-question-fake-answers, remove-security-questions, security-questions, account-recovery, osint, custom-fields]
level: intro
status: draft
description: "Answer security questions with random, stored answers instead of true facts, and remove or replace them where accounts allow, since true answers are public."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://ssd.eff.org/module/creating-strong-passwords"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Random answers to security questions

**Goal:** "mother's maiden name", "first school", "city you were born in" are on social
media, genealogy sites and data broker profiles. They are passwords anyone can look up.

## Rule
Treat each answer as a **password**: random, unique per site, stored in the vault.

## Procedure
1. When a site asks for security questions, generate a passphrase-style answer
   (`copper-lantern-58`): pronounceable, because you may need to read it to a call centre.
2. Save in the login item as hidden custom fields `SQ: <question>` (see
   `computing-software.digital-privacy-hygiene.password-managers.custom-fields-pins-and-security-answers`).
3. Avoid "funny" fake answers you reuse everywhere ("Batman"); reuse breaks it.

## Removing or replacing existing ones
- Visit security settings of older accounts (banks, utilities, old email, Apple accounts
  from before two-factor): many let you **delete** questions once 2FA is on, or change them.
- Apple: accounts upgraded to two-factor no longer use security questions.
- Where you can't remove them, replace true answers with random ones now; attackers
  may already have your true ones from a breach.

## Call centres
Some agents get confused by random answers ("That's not a city"). Say calmly that it's a
password you set; read it exactly. For phone access prefer a verbal password (see
`computing-software.digital-privacy-hygiene.password-hygiene.verbal-passwords-with-banks-and-carriers`).

## Verify
- [ ] No account uses a true fact as a security answer.
- [ ] All answers retrievable from the vault.
