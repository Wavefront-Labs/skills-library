---
id: computing-software.digital-privacy-hygiene.two-factor-auth.yubikey-otp-slots
name: yubikey-otp-slots
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, yubikey-otp-slots, yubikey, security-keys]
level: practitioner
status: docs-checked
description: "Understand YubiKey OTP slots, inspect and clear them with ykman, and avoid static-password configurations."
sources:
  - "https://docs.yubico.com/software/yubikey/tools/ykman/OTP_Commands.html"
  - "https://docs.yubico.com/software/yubikey/tools/ykman/Base_Commands.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# YubiKey OTP slots

**Goal:** know what the "OTP" part of a YubiKey does, and manage its slots deliberately.

## What it is
The YubiKey provides two keyboard-based slots (1 and 2) that can each hold a credential. Supported types include
Yubico OTP, HMAC-SHA1 challenge-response, OATH-HOTP and a static password. A slot configuration can be
write-protected with an access code, which stops it being overwritten without that code.

## Commands (`ykman otp`)
```
ykman otp info                       # status of the OTP slots
ykman otp delete 1                   # delete the configuration in slot 1
ykman otp chalresp --generate 2      # random challenge-response credential in slot 2
ykman otp swap                       # swap the two slot configurations
```
Options such as `--touch` on `chalresp` require a touch to generate a response. Deletion removes the stored
configuration; check `ykman otp info` first and make sure nothing you use depends on the slot.
`ykman config` enables or disables applications; see Yubico's ykman config page for the exact syntax.

## Static passwords: avoid
`ykman otp static` configures a slot to type a fixed password (it can generate a random one, for example
`--generate 2 --length 38`). Anyone holding the key can type that password, and a fixed secret cannot be revoked
independently of the key. Use a slot access code if you do keep one.

## Gotchas
- Mode-switching the YubiKey is not possible while a slot has an access code set.

## Checked
2026-11-01. Confirmed in the ykman OTP commands and base commands pages: two slots, credential types, access code
write protection, the four commands above, `--touch`, static password generation, access code and mode-switching
note. Removed: factory contents of slot 1 and the `cccccc` string, long-touch timing, KeePassXC use, the exact
`ykman config usb --disable OTP` syntax (config page not read), and the FIDO2 usage statement.
Method: documentation only; no commands were run.
