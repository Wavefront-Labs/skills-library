---
id: computing-software.general-digital-literacy.internet-navigation.standalone-password-manager-apps
name: standalone-password-manager-apps
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-authentication, bitwarden, password-manager, 1password, keepass]
level: intro
status: docs-checked
description: "Set up a standalone password manager such as Bitwarden, 1Password or KeePassXC: master password, import from the browser, autofill on phone, sharing and emergency access."
sources:
  - https://bitwarden.com/pricing/
  - https://support.1password.com/travel-mode/
  - https://keepassxc.org/
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online/password-managers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Standalone password manager apps

Browser password managers (Google, Apple Passwords, Edge) are fine for many people. A standalone manager can work across platforms (iPhone, Windows, Android) and add secure sharing and emergency access; features vary by product and plan.

## Choosing
- **Bitwarden**: its free plan covers passwords across all your devices; the paid Premium plan adds an integrated authenticator, emergency access and security reports (Bitwarden pricing page).
- **1Password**: subscription product; Travel Mode, included with every subscription, removes vaults from your devices when you travel.
- **KeePassXC**: free and open source, cloud-free; you store and sync the database yourself, so it takes more effort.
- Other products exist; compare using NCSC's checklist (cross-device use, password generation, price, sharing, breach alerts).

## Set up
1. Create a **master password**: a long passphrase of random words you never use elsewhere. NCSC says many managers offer recovery such as hints or emergency access through trusted contacts, so check what yours offers before relying on memory alone.
2. Turn on **2-step verification** for the manager account (NCSC advice); save any recovery code it gives you.
3. **Import** from the browser. In Chrome: More › Passwords and autofill › Google Password Manager › Settings › Export passwords › Download file. Import the file into the manager, then **delete the exported file** (it contains your passwords in readable form) and turn off the browser's own save prompts.
4. Install the browser extension and the phone app; choose it as the **autofill provider** in your phone's settings (menu names vary by OS version).

## Use well
- Let it generate passwords (you can set length and character set). Fix reused or weak ones flagged in its report, most important accounts first.
- Shared family logins: shared vault/collection instead of texting passwords.
- If your plan offers **emergency access**, set it up.

## Verify
- [ ] Autofill works on phone and computer; the vault health report shows no reused passwords on email or banking.

## Checked

Checked 2026-10-27 against the Bitwarden pricing page, 1Password Travel Mode support page, keepassxc.org, NCSC password manager guidance and Chrome Help (export passwords). Confirmed: Bitwarden free versus Premium features, Travel Mode included with every subscription, KeePassXC free open source and cloud-free, NCSC advice on 2-step verification and recovery options, Chrome export path.

Method: documentation only; no commands were run.
