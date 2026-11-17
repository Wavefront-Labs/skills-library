---
id: computing-software.digital-privacy-hygiene.two-factor-auth.choosing-an-authenticator-app
name: choosing-an-authenticator-app
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, authenticator-app-selection, authenticator-app, totp, aegis, ente-auth, 2fas, google-authenticator, microsoft-authenticator, yubico-authenticator, encrypted-backup]
level: intro
status: draft
description: "Choose a TOTP authenticator app on encrypted backup, export, open source, app lock and cloud-sync trade-offs; Aegis, Ente Auth, 2FAS, Google and Microsoft compared."
sources:
  - "https://www.privacyguides.org/en/multi-factor-authentication/"
  - "https://getaegis.app/"
  - "https://ente.io/auth/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing an authenticator app

**Goal:** pick an app you can back up, export and lock, so a lost phone doesn't
cost you 40 accounts.

## Criteria
1. **Encrypted backup** you control (file or end-to-end encrypted sync).
2. **Export** in a standard format (`otpauth://` URIs, encrypted JSON) so you can leave.
3. **App lock** (biometric/PIN) independent of the phone unlock.
4. **Open source / audited** code.
5. Platforms you need (both Android and iOS for households with both).

## Comparison (verify current features)
| App | Platforms | Backup | Export | Notes |
|---|---|---|---|---|
| Aegis | Android | Encrypted vault file, automatic to a folder | Yes | Open source; Privacy Guides recommendation |
| Ente Auth | Android, iOS, desktop, web | End-to-end encrypted cloud sync | Yes | Open source, audited; good cross-platform choice |
| 2FAS | Android, iOS | Encrypted backup (iCloud/Drive) | Yes | Open source |
| Google Authenticator | Android, iOS | Google account sync (not E2EE by default when introduced) | QR transfer | Convenient; check sync encryption state |
| Microsoft Authenticator | Android, iOS | iCloud/Microsoft account backup | Limited | Needed for Microsoft push/passwordless |
| Yubico Authenticator | All | Secrets on YubiKey (OATH, max ~32-64 per key) | No (by design) | Secrets can't be copied off the key; register a second key |

## Recommendation pattern
- Android-only: Aegis with automatic encrypted backups to a synced folder.
- Mixed household: Ente Auth.
- High-value accounts: hardware-backed (Yubico OATH or better, FIDO2) rather than any app.
- Keep Microsoft Authenticator only for Microsoft accounts if you need its push.

## Gotchas
- Moving all codes to a new app: follow
  `computing-software.digital-privacy-hygiene.two-factor-auth.totp-seed-backup-and-authenticator-migration`.
- Avoid apps requiring a phone number account (SMS-recoverable backups) for sync.

## Verify
- [ ] Encrypted backup exists outside the phone and was restored once.
- [ ] App lock enabled.
