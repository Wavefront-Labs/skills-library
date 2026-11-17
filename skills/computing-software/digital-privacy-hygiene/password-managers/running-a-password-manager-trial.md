---
id: computing-software.digital-privacy-hygiene.password-managers.running-a-password-manager-trial
name: running-a-password-manager-trial
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, password-manager-trial, password-manager-selection, password-manager-pricing]
level: practitioner
status: draft
description: "Run a two-week password manager trial with a test vault: import a sample, exercise autofill, sharing, recovery and export before moving everything."
sources:
  - "https://www.privacyguides.org/en/passwords/"
  - "https://ssd.eff.org/module/choosing-the-password-manager-thats-right-for-you"
  - "https://bitwarden.com/help/import-data/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Running a password manager trial

**Goal:** find the deal-breakers in two weeks with throwaway data, not after you've moved 400 logins.

## Setup (day 1)
- Create the account with a **new** master passphrase you won't use elsewhere.
- Import 10-20 real but low-value logins (forums, newsletters), not banking.
- Install on all devices (see platform support check).

## Daily-use tests (days 1-10)
- [ ] Autofill on login forms with separate username and password pages (Google, Microsoft).
- [ ] Save a new login when signing up; edit a password change flow.
- [ ] Generate a password on a site with character rules.
- [ ] Mobile autofill in apps (banking apps often block, note which).
- [ ] TOTP if you plan to store codes; passkey creation on a test site (webauthn.io).
- [ ] Vault timeout behaviour: does it re-prompt at sensible times?

## Failure tests (days 10-14)
- [ ] Export the vault (encrypted and plain) and open it: is everything there, including attachments?
- [ ] Log out and log in on a new device: what does it require (2FA, Secret Key, device approval)?
- [ ] Set up emergency access / family recovery and walk through it with the other person.
- [ ] Turn off Wi-Fi: can you still unlock and read logins?

## Pricing check
Note what you used that is paid-only (TOTP, attachments, emergency access, family sharing) and price the
plan you actually need for the household for 3 years.

## Decide
If every box passes, do the full migration. If one fails, try the next candidate; delete the trial account
(and its export files) when done.
