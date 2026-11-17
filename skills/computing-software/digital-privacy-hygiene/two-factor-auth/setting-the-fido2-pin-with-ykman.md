---
id: computing-software.digital-privacy-hygiene.two-factor-auth.setting-the-fido2-pin-with-ykman
name: setting-the-fido2-pin-with-ykman
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, fido2-pin, ykman, yubikey, security-keys, user-verification, pin-retries, windows-security-key-settings]
level: practitioner
status: docs-checked
description: "Set and change a YubiKey's FIDO2 PIN with ykman: length rules, forcing a change, verifying the PIN, and what a FIDO reset wipes."
sources:
  - "https://docs.yubico.com/software/yubikey/tools/ykman/FIDO_Commands.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting the FIDO2 PIN

**Goal:** the PIN is what makes a found or stolen key much less useful for passkey logins.

## Why it matters
For passkeys (passwordless), the key does **user verification** with a PIN or biometric.
Managing stored discoverable credentials with ykman also requires a PIN to be set first.
Fingerprint management is available only when a FIDO PIN is set.

## ykman commands
```bash
ykman fido info                       # display status of the FIDO2 application
ykman fido access change-pin          # set or change the PIN
ykman fido access verify-pin          # verify the PIN; resets the retries counter on FIDO2 keys
ykman fido access force-change        # force a change before next use (ykman 5.3.0+)
ykman fido access set-min-length LEN  # set the minimum PIN length (ykman 5.3.0+)
```
`change-pin` takes `-P/--pin` (current) and `-n/--new-pin`; leave them off to be prompted
rather than typing a PIN into shell history. On Windows, `ykman fido` commands need an
administrator Command Prompt or PowerShell.

## PIN rules
- The FIDO2 PIN must be at least 4 characters and can be any alphanumeric characters;
  some YubiKeys can be configured to require longer.
- On a YubiKey FIPS (4 Series) a PIN can be set for FIDO U2F with `--u2f`; it must be at
  least 6 characters.
- Retry limits and lockout behaviour are not covered by the ykman reference; check
  Yubico's PIN documentation for your model before relying on a number.
- `ykman fido reset` wipes all FIDO credentials, including U2F, and removes the PIN; it
  runs right after the key is inserted and needs a touch. See
  `computing-software.digital-privacy-hygiene.two-factor-auth.resetting-a-fido2-security-key`.

## Store the PIN
In your password manager against the key's name. Different PINs per key are fine but
must be recorded.

## Verify
- [ ] `ykman fido info` reports the PIN as set.
- [ ] A passkey login prompts for the PIN.

## Checked
Checked 2026-11-08 against the ykman FIDO Commands page. Removed: the 3-then-8 retry
figures, the Yubico Authenticator, Windows Settings and Chrome menu paths, and the
retries-remaining output, because the Yubico PIN support article could not be read and
the ykman page does not give them.

Method: docs-only read of cited pages, 2026-11-08
