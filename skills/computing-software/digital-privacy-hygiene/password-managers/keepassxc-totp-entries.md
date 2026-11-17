---
id: computing-software.digital-privacy-hygiene.password-managers.keepassxc-totp-entries
name: keepassxc-totp-entries
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [keepassxc-totp, keepassxc, totp, two-factor-auth, password-managers]
level: practitioner
status: docs-checked
description: "Add and use TOTP codes in KeePassXC entries: setup from a secret or otpauth URI, copying, auto-type, CLI, and the single-vault trade-off."
sources: ["https://keepassxc.org/docs/KeePassXC_UserGuide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeePassXC TOTP entries

**Goal:** generate 6-digit codes in the same vault as the password, knowingly.

## Set up
1. Get the secret string from the site or app you are authenticating to (often shown next to the QR code).
2. Right-click the entry, choose **TOTP > Set up TOTP...**, paste the secret, adjust custom settings only if the site
   requires them (rare), then press OK.
3. Save the database.

KeePassXC calculates codes like any authenticator app. Typical codes are six digits and change every 30 seconds.

## Use
- Menu shortcuts: Copy TOTP is Ctrl+T, Copy Password and TOTP is Ctrl+Y, Show TOTP is Ctrl+Shift+T.
- An entry with TOTP shows a clock icon; the preview pane can reveal the current code, and the TOTP menu can show it
  in a separate window.
- Auto-Type: use the `{TOTP}` placeholder (current TOTP value) in the sequence, or the Auto-Type selection dialog menu.
- The browser extension can also fill TOTP codes.
- The TOTP menu can show the secret and settings as a QR code, for exporting to a phone.
- `keepassxc-cli` exists for terminal access to a database (see `man keepassxc-cli` or `keepassxc-cli [command] -h`
  for the per-command options).

## Trade-off
The guide warns that storing TOTP codes in the same database as the password removes the advantage of two-factor
authentication, and recommends, for maximum security, a separate database that you unlock only when needed. Use the
combined entry for lower-risk accounts; keep banking, email and the vault itself on a separate factor.

## Gotchas
- Your computer clock must be synchronised with an internet time source, or codes will be invalid.
- Do not paste secrets into chat or notes. Test the code before closing the site's setup page, and save the site's
  recovery codes elsewhere.
- Database backups: KeePassXC can write a backup before saving, or on demand via Database > Save Database Backup.

## Verify
Log out of the site and back in with the generated code.

## Checked
Confirmed 2026-11-08 against the KeePassXC User Guide: the Set up TOTP dialog path, six-digit/30-second description,
shortcuts, `{TOTP}` placeholder, browser extension support, QR export, the clock-sync note, the separate-database
recommendation and the backup options. Removed: RFC 6238 and SHA-1 defaults, the claim about 8-digit and SHA-256/512
and Steam modes, the `otp` attribute name, the `keepassxc-cli show -t` invocation, and the sample Auto-Type sequence,
none of which the guide states.
Method: docs-only read of cited pages, 2026-11-08
