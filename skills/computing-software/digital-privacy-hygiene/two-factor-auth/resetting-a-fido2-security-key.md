---
id: computing-software.digital-privacy-hygiene.two-factor-auth.resetting-a-fido2-security-key
name: resetting-a-fido2-security-key
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, fido2-reset, ykman, yubikey, security-keys, blocked-pin, resale, applet-reset, oath-reset]
level: practitioner
status: draft
description: "Reset a security key's FIDO2 applet (after a blocked PIN or before giving it away), knowing exactly which credentials and other applets it destroys."
sources:
  - "https://docs.yubico.com/software/yubikey/tools/ykman/FIDO_Commands.html"
  - "https://support.yubico.com/hc/en-us/articles/360016648899-Resetting-the-FIDO2-Application-on-Your-YubiKey"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resetting a FIDO2 security key

**Goal:** recover a key whose PIN is blocked, or wipe it before reuse, without
surprises.

## What a FIDO reset does
- Deletes **all FIDO2 and U2F credentials** on the key, including passkeys and every
  "security key" 2FA registration (U2F registrations stop working because the key's
  master secret changes).
- Clears the FIDO2 PIN.
- Does **not** touch other YubiKey applets: OATH (TOTP), PIV, OpenPGP and OTP slots
  (challenge-response) are separate and have their own reset commands.

## Before resetting
Use your key inventory to list every account where this key is registered; you will
need to remove the dead registration and enroll it again (or rely on the backup key).

## How
```bash
ykman fido reset
```
YubiKeys require the reset within a few seconds of inserting the key, then a touch; the
command tells you when to remove and reinsert. Yubico Authenticator app has the same
under Passkeys > Reset. Windows: Settings > Accounts > Sign-in options > Security key >
Manage > Reset. Chrome: `chrome://settings/securityKeys` > Reset.

## Other applets if fully wiping
```bash
ykman oath reset
ykman piv reset
ykman openpgp reset
ykman otp delete 1 ; ykman otp delete 2
```

## Afterwards
- Set a new FIDO2 PIN.
- On each account: delete the old registration of this key, register it again.

## Verify
- [ ] `ykman fido info` shows no PIN set before re-setup.
- [ ] `ykman fido credentials list` (after PIN) shows only new credentials.
