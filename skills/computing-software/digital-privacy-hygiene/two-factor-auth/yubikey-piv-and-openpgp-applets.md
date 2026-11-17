---
id: computing-software.digital-privacy-hygiene.two-factor-auth.yubikey-piv-and-openpgp-applets
name: yubikey-piv-and-openpgp-applets
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, yubikey-piv, yubikey-openpgp, yubikey, openpgp]
level: practitioner
status: gated
description: "Change default PINs on a YubiKey's PIV and OpenPGP applets, load keys, set touch policies, and know what each applet is used for."
sources:
  - "https://docs.yubico.com/software/yubikey/tools/ykman/PIV_Commands.html"
  - "https://docs.yubico.com/software/yubikey/tools/ykman/OpenPGP_Commands.html"
  - "https://support.yubico.com/hc/en-us/articles/360013790259-Using-Your-YubiKey-with-OpenPGP"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# YubiKey PIV and OpenPGP applets

**Goal:** if you use these applets, they're not running on factory-default PINs, and you understand the reset
consequences.

## What they're for
- **PIV:** smart-card certificates (Windows smart-card login, SSH via PKCS#11, code signing, S/MIME).
- **OpenPGP:** GPG signing/encryption/authentication keys on the card (email, git signing, SSH via gpg-agent).

## PIV defaults and changes
Defaults: PIN `123456`, PUK `12345678`, management key well-known default.
```
ykman piv info
ykman piv access change-pin
ykman piv access change-puk
ykman piv access change-management-key --generate --protect   # store protected by PIN
ykman piv keys generate 9a pubkey.pem
```

## OpenPGP defaults and changes
Defaults: user PIN `123456`, admin PIN `12345678`.
```
ykman openpgp info
gpg --card-edit        # then: admin, passwd  (change user and admin PIN)
gpg --edit-key <id>    # keytocard to move subkeys
ykman openpgp keys set-touch sig on      # require touch for each signature
```
Keep an offline backup of the primary key before `keytocard`: moving keys to the card deletes them from the
local keyring.

## Lockouts
3 wrong PINs block the PIN; PUK/admin PIN unblocks; 3 wrong PUK/admin PINs = applet must be reset (keys gone).
`ykman piv reset` / `ykman openpgp reset` wipe only that applet, not FIDO2.

## Gotchas
- Unused applets are harmless, but a stolen key with default PIV PIN can sign as "you" if you loaded certs.
- Touch policy "fixed" can't be changed without resetting.

## Checked

- Date: 2026-11-02.
- Confirmed against: ykman piv access change-pin / change-puk / change-management-key (--generate, --protect), piv keys generate 9a pubkey.pem, piv reset and openpgp reset, set-touch, factory PIN 123456 (Yubico ykman command references).
- Not confirmed: the OpenPGP admin PIN default, lockout counts of 3 and keytocard behaviour (Yubico support article returned a stub) (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
