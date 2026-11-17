---
id: computing-software.digital-privacy-hygiene.two-factor-auth.totp-seed-backup-and-authenticator-migration
name: totp-seed-backup-and-authenticator-migration
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, totp, authenticator-migration, qr-code-backup, otpauth-uri, aegis-export, ente-auth-export, encrypted-backup, 2fas-export, authy-migration, seed-secret]
level: practitioner
status: draft
description: "Back up and migrate TOTP seeds between authenticator apps without a screenshot in a camera roll, a lost export password, or a frantic re-enrollment scramble on every site."
sources:
  - "https://github.com/beemdevelopment/Aegis/blob/master/docs/vault.md"
  - "https://ente.io/auth/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TOTP seed backup and authenticator migration

**Goal:** have an encrypted, restorable backup of every TOTP (6-digit code)
secret before you ever need it — a phone that dies, is lost, or is simply
replaced shouldn't mean re-enrolling two-factor on every single account one at
a time, which for a well-secured person can be 30+ accounts.

## 1. What's actually at stake in the seed itself
The TOTP **secret** (the shared key the `otpauth://` URI/QR code encodes) is
what generates every future 6-digit code — anyone who has it can generate valid
codes indefinitely, same as having a password. Treat the raw seed/QR with the
same sensitivity as a password, not as something safe to screenshot into a
photo-sharing camera roll that syncs to a cloud photo library you haven't
otherwise audited.

## 2. The backup, done properly
- **Aegis** (Android, open source): Settings → export the vault as an
  **encrypted** backup file (password-protected, separate from the app's own
  unlock), store that file somewhere durable (password manager attachment,
  encrypted cloud folder, or offline). Aegis can also export individual entries
  as plain `otpauth://` URIs if needed for migration — treat that export as
  unencrypted and handle it the same way as a password-manager CSV export (see
  `computing-software.digital-privacy-hygiene.password-managers.migrating-vaults-between-password-managers`
  section 1: create it, use it immediately, destroy it).
- **Ente Auth** (cross-platform, end-to-end encrypted cloud sync): backup is
  continuous via its own encrypted sync rather than a manual export step —
  verify you can actually restore onto a second device before trusting it as
  your only copy.
- **2FAS**: similar encrypted-backup model; check current docs for exact steps.
- Whichever tool: **test a restore onto a spare device or fresh install**
  before you need it for real — an export that silently fails to restore is
  worse than no backup, because it creates false confidence.

## 3. What NOT to do
- **Screenshotting the QR code** into your phone's camera roll — this photo
  then lives, unencrypted relative to the seed it contains, in whatever cloud
  photo backup you have, indefinitely, outside any security review.
- **Storing the raw seed in a plain text note** (a notes app without
  encryption, an email draft) — same exposure as writing a password in plain
  text.
- Relying on **Authy** for long-term storage: Authy retired its desktop apps in
  2024 and has made bulk export difficult by design — if you still have
  accounts enrolled there, plan a one-by-one migration (disable 2FA, re-enroll
  in the new app, re-enable) rather than assuming a clean bulk export exists;
  I can't confirm Authy's current export capabilities — check before relying on any.

## 4. Migrating to a new authenticator app
- If the old app supports a seed export (`otpauth://` URIs or a QR), import
  directly into the new app and **verify each one** by comparing the generated
  code against the old app at the same moment before deleting the old app's
  copy.
- If no export path exists (or you're moving off a password-manager-stored
  TOTP, which some sites require re-registering from scratch anyway): go
  account by account — disable the old 2FA method on the site, re-enroll
  fresh in the new app, confirm login works, then move to the next account.
  Tedious but reliable; don't try to shortcut it with a half-working bulk tool.
- Update your **backup codes** too (section 6 of
  `computing-software.digital-privacy-hygiene.two-factor-auth.setting-up-mfa-and-backup-methods`)
  if re-enrolling resets them, which many sites do.

## 5. Replacing a phone (not changing apps)
- Move the authenticator app's data **before** wiping the old phone — most
  modern authenticator apps support an in-app encrypted transfer or at minimum
  an export/import between two installs of the same app; don't erase the old
  device until you've confirmed codes generate correctly on the new one for a
  sample of accounts.
- If the app offers no transfer and the old phone is already gone, you're in
  the "account by account" recovery flow of
  `computing-software.digital-privacy-hygiene.two-factor-auth.account-recovery-after-losing-your-second-factor`.

## Gotchas
- A successful-looking QR export doesn't guarantee the import parsed every
  field correctly — spot-check generated codes against the old app before
  deleting anything.
- Keeping TOTP only inside the same password manager that also holds the
  account's password collapses two independent factors into one vault — fine
  as a convenience trade-off for low-value accounts, worth avoiding for email
  and the password manager's own account.
- Uncertain: specific export/import compatibility between different
  authenticator apps (Aegis ↔ Ente ↔ 2FAS) shifts with app updates — verify
  the current state before a migration, don't assume last year's compatibility
  holds.

## Verify
- [ ] An encrypted backup of the authenticator app's vault exists somewhere
      durable, separate from the phone itself.
- [ ] A restore has actually been tested on a spare device or fresh install,
      not just assumed to work.
- [ ] No raw seed or QR code lives as a plain screenshot in a cloud-synced
      camera roll.
- [ ] After any migration, a sample of accounts was spot-checked for matching
      codes before the old app/device was wiped.
