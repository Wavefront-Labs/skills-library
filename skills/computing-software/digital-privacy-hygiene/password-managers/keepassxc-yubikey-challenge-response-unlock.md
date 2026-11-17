---
id: computing-software.digital-privacy-hygiene.password-managers.keepassxc-yubikey-challenge-response-unlock
name: keepassxc-yubikey-challenge-response-unlock
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, yubikey-challenge-response, keepassxc, kdbx, yubikey, hmac-sha1, ykman, backup-yubikey, keepassxc-composite-key]
level: advanced
status: docs-checked
description: "Add a YubiKey HMAC challenge-response to a KeePassXC database, write the same secret to a backup key with ykman, and avoid lockout."
sources:
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_yubikey_challenge_response"
  - "https://docs.yubico.com/software/yubikey/tools/ykman/OTP_Commands.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeePassXC YubiKey challenge-response

**Goal:** a stolen `.kdbx` plus a captured password is not enough without the physical key.

## How it works
KeePassXC supports key files and hardware keys such as YubiKey and OnlyKey as extra credentials beyond the password. With a hardware key configured, it must be connected to unlock the database.

## Program two keys with the same secret
The KeePassXC guide advises a backup replica key, with the same HMAC key written to both, and the secret stored somewhere safe (for example on paper) so another key can be recreated. Because `ykman otp chalresp --generate` creates a secret you never see, supply your own for a backup:
```bash
# guide's example: 20-byte hex secret
dd status=none if=/dev/random bs=20 count=1 | xxd -p -c 40
ykman otp chalresp --touch 2 <HEX_SECRET>    # repeat with the backup key inserted
```
ykman: usage is `ykman otp chalresp [OPTIONS] {1|2} [KEY]`; KEY is hex (base32 only with `--totp`); omit KEY and it prompts. `--touch` requires a physical touch before each response. `--generate` cannot be combined with KEY. The guide uses slot 2 because slot 1 holds the YubiKey OTP out of the box. A slot protected by an access code cannot be overwritten without it.

## Add to the database
Database Security, Add YubiKey Challenge-Response, plug in the key and press refresh, then save. When unlocking, choose the key in the dialog (refresh if it is not listed).

## Gotchas
- Losing both keys and the stored secret means you cannot recreate a key.
- `ykman otp delete {1|2}` clears the configuration in that slot (`-f` skips the prompt), which would break unlock for that key.
- Check that your other clients (mobile) support challenge-response before relying on it; the cited pages do not cover this.

## Verify
- [ ] Database opens with password plus key A, and with password plus key B.
- [ ] Stored copy of the secret exists offline.

## Checked
Method: 2026-11-08 read the KeePassXC guide's security, unlock and "Creating a YubiKey backup" parts and the Yubico ykman OTP commands page. Dropped as unsupported: the specific mobile apps (KeePassDX, Strongbox, KeePassium), the Flatpak USB permission note, the claim that challenge-response is separate from FIDO2 resets, and the master-seed description. The guide's own backup steps use ykpersonalize; ykman equivalents are from the Yubico page.
