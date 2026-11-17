---
id: computing-software.digital-privacy-hygiene.password-managers.master-password-hints
name: master-password-hints
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, master-password-hint, master-password, vault-account-security]
level: practitioner
status: draft
description: "Why to leave a password manager's master password hint empty, what Bitwarden's hint email exposes, and safer ways to make the passphrase recoverable."
sources:
  - "https://bitwarden.com/help/master-password/"
  - "https://bitwarden.com/help/forgot-master-password/"
  - "https://support.1password.com/forgot-account-password/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Master password hints

**Goal:** don't give an attacker who controls your email a clue to the one password that opens everything.

## How hints work
- **Bitwarden:** optional hint set at registration or in Settings > Security > Master password. Anyone can
  request it at the login page ("Get master password hint"); it is emailed in plaintext to the account email.
- **1Password:** no hint. Recovery is via the Emergency Kit or a family organiser.
- **KeePassXC:** no hint; the database is just a file.

## Why leave it empty
- The hint goes to your email: anyone who has taken over your email, or reads it on a shared device, gets it.
- Hints for strong random passphrases tend to leak structure ("dog + street + year").
- An attacker with a stolen encrypted vault plus the hint can tailor a cracking wordlist.

## What to do instead
- Use a diceware passphrase you practise with spaced recall until it's automatic.
- Write the passphrase on paper in a sealed envelope in a safe or with your will (this is the emergency kit
  model), or set up emergency access / family recovery.
- If you already set a Bitwarden hint, clear it: Settings > Security > Master password > change it (re-enter
  current password, leave hint blank). Clearing a hint requires the change-password form.

## Gotchas
- A hint that is "see envelope in safe" is fine: it tells an attacker nothing they can use remotely.
- Never put any part of the passphrase in a note inside the same vault.
