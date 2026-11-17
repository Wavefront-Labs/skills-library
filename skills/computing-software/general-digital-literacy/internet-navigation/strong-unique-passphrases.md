---
id: computing-software.general-digital-literacy.internet-navigation.strong-unique-passphrases
name: strong-unique-passphrases
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, authentication, passphrase, strong-passwords, three-random-words, password-manager, diceware]
level: intro
status: docs-checked
description: "Create strong, memorable passphrases with three random words or diceware, use a unique one for every account via a password manager, and check for reuse and breaches."
sources:
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online/use-a-strong-and-separate-password-for-email
  - https://pages.nist.gov/800-63-4/sp800-63b.html
  - https://www.eff.org/dice
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strong unique passphrases

**Goal:** passwords that are long, unique per site, and memorable only where you actually need to remember them.

## What makes a password strong
- **Length** beats complexity. NIST SP 800-63B (revision 4) requires at least 15 characters for passwords used alone (8 when used only as part of multi-factor sign-in), says services should allow at least 64, and says they should not impose composition rules.
- **Unique:** reusing one password means one breach opens every account.
- Not guessable: names, birthdays, teams, `Password1!`, keyboard patterns.

## Make a passphrase
- **Three (or more) random words** (NCSC advice): `kettle-orbit-meadow`. Add a fourth word or a number/symbol if a site demands it: `kettle-orbit-meadow-42`.
- Truly random beats "random": use **diceware** (roll dice, look up words on the EFF word list, eff.org/dice) or your password manager's passphrase generator.
- Avoid famous quotes, song lyrics and related words ("red-white-blue").

## Remember only a few
Memorise passphrases for: your **email account**, your **password manager** master, your **device** login. Everything else: let the **password manager** generate 20+ random characters and fill them.

## Check and fix
- Your password manager's security report: many managers flag reused, weak and breached passwords (NCSC).
- **haveibeenpwned.com/Passwords** checks if a password appeared in breaches; only the first 5 characters of its SHA-1 hash are sent (k-anonymity).
- Change reused passwords on important accounts first: email, banking, shopping with stored cards, social media.

## Gotchas
- NIST says services shall not require periodic password changes, but shall force a change if there is evidence of compromise.
- Passkeys are stronger still; use them where offered, keep a passphrase as backup.
- Never share passwords by text or email; use the password manager's sharing feature.

## Verify
- [ ] Email and password manager have unique passphrases; reused-password count in the checkup is zero.

## Checked

Checked 2026-10-27 against NIST SP 800-63B revision 4, NCSC three random words and password manager guidance, the EFF dice page and the Have I Been Pwned Passwords page. Confirmed: 15-character minimum for single-factor passwords (8 for MFA-only), 64-character maximum should be permitted, no composition rules, no periodic changes, three random words, EFF dice, k-anonymity with the first 5 SHA-1 characters.

Method: documentation only; no commands were run.
