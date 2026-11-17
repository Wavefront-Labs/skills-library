---
id: computing-software.digital-privacy-hygiene.password-managers.passphrase-generator-settings
name: passphrase-generator-settings
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, passphrase-generator, password-generator, diceware]
level: practitioner
status: draft
description: "Configure a password manager's passphrase generator: word count, separator, capitalisation and number options, with the entropy each choice buys."
sources:
  - "https://bitwarden.com/help/generator/"
  - "https://www.eff.org/dice"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_password_generator"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Passphrase generator settings

**Goal:** generate memorable passphrases (for the master password, device logins, Wi-Fi) with known strength.

## Strength math
With the EFF long wordlist (7,776 words) each random word adds about 12.9 bits.
| Words | Bits | Use |
|---|---|---|
| 4 | ~52 | Low-value, rate-limited online logins |
| 5 | ~65 | Device login, Wi-Fi |
| 6 | ~78 | Master password, disk encryption |
| 7 | ~90 | Long-term offline-attack targets (encrypted backups) |
Separators, capitals and an appended digit add only a few bits; length (word count) is what matters.

## Bitwarden
Generator > Passphrase: Number of words (3-20), Word separator, Capitalize, Include number. Uses the EFF long list.
Copy from history if you close the dialog by accident (Generator history).

## 1Password
Password generator > Memorable Password: words, separator (hyphens, spaces, periods, commas, underscores,
digits), Capitalize, Full words.

## KeePassXC
Tools > Password Generator > Passphrase tab: word count, word list (EFF large default), separator, word case.

## Choosing options
- Use spaces or hyphens if you type it on phones; avoid separators that switch keyboard layers.
- "Full words" off (1Password) can produce syllables; keep full words for memorability.
- For site logins you never type, use a random 20+ character password instead; passphrases are for things
  you must type.

## Gotchas
- Never "improve" a generated passphrase by swapping in your own words; human choice kills the entropy.
- Some sites cap length; check before saving a 7-word phrase there.
