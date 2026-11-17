---
id: computing-software.digital-privacy-hygiene.password-managers.integrated-totp-in-the-vault-trade-off
name: integrated-totp-in-the-vault-trade-off
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, integrated-totp, totp, bitwarden, factor-separation, convenience-tradeoff]
level: practitioner
status: docs-checked
description: "Decide which accounts may keep their TOTP secret in the password manager (fast autofill) and which need a separate authenticator, then set it up in Bitwarden."
sources:
  - "https://bitwarden.com/help/integrated-authenticator/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TOTP inside the password manager

**Goal:** make a deliberate, per-account choice about collapsing two factors into one vault.

## The trade-off (judgement, not a vendor claim)
- **For**: the code is available right after autofill, so people actually enable 2FA everywhere.
- **Against**: whoever has the unlocked vault has both factors. It still helps against a password leaked from the
  site, but not against vault compromise.

## Decision rule
| Account | TOTP in vault? |
|---|---|
| The password manager account itself | Never |
| Primary email (the reset root) | No; use a security key or separate app |
| Banking, brokerage, crypto exchange | No, unless the only alternative is SMS |
| Domain registrar, cloud admin | No; use a security key |
| Everything else (forums, shops, SaaS) | Yes, fine |

## Setup in Bitwarden
- Storing the key is available to all accounts; generating codes needs premium or membership of a paid
  organisation (Families, Teams or Enterprise).
- Web or extension: edit the item and fill the **Authenticator key** field; the extension can also scan a QR
  code shown on the current page.
- Mobile: edit the item, **Set up authenticator key**, then scan the QR code or enter the key manually.
- **Copy TOTP automatically** is under Settings > Autofill (on by default for extension autofill).
- Other managers have their own TOTP fields; read their help pages.

## Gotchas
- When enrolling, save the TOTP in the vault **before** confirming on the site, then type the generated code to
  confirm; otherwise a failed save means lockout.
- Keep the site's recovery codes elsewhere (not in the same item) for high-value accounts.

## Verify
- [ ] Accounts with in-vault TOTP exclude email, bank and the vault itself.
- [ ] Code generated in the vault accepted by the site at enrolment.

## Checked
2026-11-01. Confirmed against bitwarden.com/help/integrated-authenticator/: premium or paid-organisation
requirement for generating codes, Authenticator key field, QR scanning, mobile setup path, Copy TOTP automatically
location and default. The decision table is marked as judgement. Removed as unconfirmed: 1Password and KeePassXC
setup, default period and digits claims, the phishing-resistance and attack-share statements, and the other URLs.
Method: documentation only; no commands were run.
