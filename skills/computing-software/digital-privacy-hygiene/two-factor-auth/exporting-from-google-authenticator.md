---
id: computing-software.digital-privacy-hygiene.two-factor-auth.exporting-from-google-authenticator
name: exporting-from-google-authenticator
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, google-authenticator-export, authenticator-migration, totp]
level: practitioner
status: docs-checked
description: "Move TOTP accounts out of Google Authenticator using transfer QR codes, decide on Google account sync, and decode migration QRs offline if needed."
sources:
  - "https://support.google.com/accounts/answer/1066447"
  - "https://github.com/scito/extract_otp_secrets"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Exporting from Google Authenticator

**Goal:** migrate codes to a new phone or another app without re-enrolling every site.

## Phone to phone (same app)
- If you sign in to your Google Account in Authenticator on the new device, synced codes
  arrive automatically (sync needs Android 6.0+ and app 6.0+, or iOS and app 4.0+).
- Manual transfer (also for use without a Google Account): on the new device install the
  app, tap Get Started and sign in. On the old device (latest app version): Menu >
  **Transfer codes** > **Export codes**, unlock the device, select accounts, Next. More than
  one account may produce more than one QR code. On the new device: Menu > Transfer codes >
  **Import codes** and scan each QR. Test the codes before wiping the old phone.

## To another app
Aegis's README lists Google Authenticator among its import sources. For other apps check
their documentation. The export QR holds an `otpauth-migration://offline?data=...` URL.

## Extracting secrets offline
If the target app cannot read migration QRs, decode them on an offline machine with
`extract_otp_secrets` (github.com/scito/extract_otp_secrets). Its README describes:
prebuilt executables, Docker images for amd64 and arm64, or running the Python script
after `pip install -U -r requirements.txt` (the zbar library is recommended for QR
reading). It accepts QR images or a text file of `otpauth-migration://` lines and can write
CSV, JSON, text or URL output (`--csv`, `--json`, `--txt`, `--urls`). Delete screenshots and
output files afterwards: they contain all your seeds.

## Google account sync
Authenticator can sync codes to your Google Account; Google says codes are encrypted in
transit and at rest. Tradeoffs: it survives device loss, but your Google Account becomes
a path to all your codes, so enrol in additional 2-Step Verification and consider passkeys
(Google's best-practice list). To avoid sync, choose "Use without an account" (when you
first open the app, or via the profile picture); that removes codes from your Google
Accounts and stores them on the device only, not on your other devices.

## Gotchas
- Deleting a code in a synced setup deletes it on every synced device.
- Version 7.0 removed the time correction setting; the app uses the operating system time,
  so incorrect codes often mean a wrong device clock.
- Lost or stolen device: remote-erase it; synced codes can also be removed by removing the
  device from your Google Account. Unsynced codes mean visiting every site to re-link.
- Turn on Privacy Screen (Menu > Settings) to require a PIN, pattern or biometric.

## Checked
Checked 2026-11-08 against the Google Authenticator help page (1066447) and the
extract_otp_secrets README. Removed: the "Transfer accounts" wording (the page says
Transfer codes), claims that 2FAS, Ente Auth and Bitwarden scan the QR, the screenshot-
blocking and "batch-limited" remarks, the "test 3 sites" count and the unverified PyPI note.

Method: docs-only read of cited pages, 2026-11-08
