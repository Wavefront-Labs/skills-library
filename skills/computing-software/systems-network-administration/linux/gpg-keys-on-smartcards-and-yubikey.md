---
id: computing-software.systems-network-administration.linux.gpg-keys-on-smartcards-and-yubikey
name: gpg-keys-on-smartcards-and-yubikey
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, gpg-smartcard, yubikey, openpgp-card, keytocard, gpg-agent, scdaemon]
level: practitioner
status: docs-checked
description: "Move GnuPG subkeys to an OpenPGP smartcard or YubiKey: offline primary key, keytocard, PIN and touch policies, using the card for SSH and signing, and recovery."
sources:
  - https://developers.yubico.com/PGP/YubiKey_5.2.3_Enhancements_to_OpenPGP_3.4.html
  - https://github.com/gpg/gnupg/blob/master/doc/gpg-card.texi
  - https://github.com/Yubico/yubikey-manager/blob/main/ykman/_cli/openpgp.py
  - https://github.com/drduh/YubiKey-Guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GPG keys on smartcards and YubiKey

**Goal:** the private subkeys live on hardware and can't be copied; the primary (certify) key stays offline.

## Plan
1. Generate the primary key (certify only) and three subkeys (sign, encrypt, auth) on an offline machine or live USB.
2. Back up the full secret key and a revocation certificate to encrypted offline media.
3. Move the subkeys to the card; remove the primary secret from the daily machine.

## Generate
```bash
export GNUPGHOME=$(mktemp -d)
gpg --quick-generate-key 'Alice Example <alice@example.com>' ed25519 cert 2y
FPR=$(gpg -k --with-colons alice@example.com | awk -F: '/^fpr/{print $10; exit}')
gpg --quick-add-key $FPR ed25519 sign 1y
gpg --quick-add-key $FPR cv25519 encr 1y
gpg --quick-add-key $FPR ed25519 auth 1y
gpg --armor --export-secret-keys $FPR > primary-and-subkeys.asc   # to the offline backup
gpg --gen-revoke $FPR > revoke.asc
```
YubiKey firmware before 5.2.3 has no elliptic-curve support in its OpenPGP application, so use RSA there; elliptic curves need firmware 5.2.3 or later (Yubico PGP documentation). Check the key types your card supports with `gpg --card-status`.

## Prepare the card
```bash
gpg --card-status
gpg --edit-card      # "--card-edit" is an alias; type help for the command list
  passwd        # change or unblock the PINs (YubiKey OpenPGP defaults: PIN 123456, admin PIN 12345678, no reset code)
  name / url    # optional: url = where your public key lives, used by the card's 'fetch' command and gpg --fetch
```
YubiKey touch requirement: `ykman openpgp keys set-touch sig on` (key slots are `sig`, `dec`, `aut` and `att`; policies are `on`, `off`, `fixed`, `cached`, `cached-fixed`); `cached` keeps touch valid for 15 s after use.

## Move subkeys
```bash
gpg --edit-key $FPR
  key 1  -> keytocard -> 1 (Signature)   ; key 1 (deselect)
  key 2  -> keytocard -> 2 (Encryption)  ; key 2
  key 3  -> keytocard -> 3 (Authentication)
  save
```
`keytocard` replaces the local secret with a stub once you `save`; do it from a copy of GNUPGHOME if you want a second card with the same keys. In `gpg -K` a `>` after `sec`/`ssb` marks a key stored on a smartcard and a `#` marks a secret key that is currently not usable (taken offline, e.g. after `--export-secret-subkeys`).

## Daily use
```bash
gpg --import pubkey.asc; gpg --card-status    # import the public key, then read the card
echo 'enable-ssh-support' >> ~/.gnupg/gpg-agent.conf
export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)
ssh-add -L                                    # card auth key as an SSH public key
git config --global user.signingkey $FPR!; git config --global commit.gpgsign true
```
If the card is also used through a PC/SC daemon, `scdaemon.conf` has `disable-ccid` (use PC/SC instead of the built-in CCID driver) and `pcsc-shared` (shared PC/SC access; the manual calls it somewhat dangerous because scdaemon assumes exclusive access).
Active cards are always offered by gpg-agent's SSH support, so no `sshcontrol` entry is needed for a card key.

## Recovery
- PIN blocked after the retry limit: unblock with the admin PIN or reset code (`gpg --edit-card`, then `passwd`).
- Admin PIN blocked: factory reset (`ykman openpgp reset` on a YubiKey, or `factory-reset` in `gpg-card`) deletes all keys and resets the PINs; reload the subkeys from backup.
- Lost card: revoke or rotate subkeys from the offline primary, publish updated public key.

## Verify
- [ ] `gpg -K` shows `ssb>` for the subkeys on the card; signing prompts for PIN (and touch).
- [ ] Removing the card makes signing fail; `ssh -T git@github.com` works with the card inserted.

## Checked
Checked 2026-10-27 against the GnuPG documentation source (github.com/gpg/gnupg, doc/gpg.texi, gpg-card.texi, gpg-agent.texi, scdaemon.texi), the Yubico PGP page for firmware 5.2.3 and the ykman OpenPGP source (github.com/Yubico/yubikey-manager).
- Elliptic-curve support in the YubiKey OpenPGP application starts at firmware 5.2.3.
- `ykman openpgp keys set-touch` takes slots `sig`, `dec`, `aut`, `att` (not `enc`) and policies including `cached` (15 s); `ykman openpgp reset` exists; default PIN 123456 and admin PIN 12345678 are echoed by ykman.
- `keytocard` replaces the secret key with a stub after `save`; `>` and `#` listing markers; `--edit-card` with alias `--card-edit`; `PASSWD`, `NAME`, `URL`, `FETCH`, `FACTORY-RESET` commands in gpg-card.
- `--quick-generate-key` and `--quick-add-key` take `algo usage expire`; scdaemon options `disable-ccid` and `pcsc-shared`; gpg-agent `enable-ssh-support`, active cards always offered.
- Corrected: `enc` slot name, and the removed `admin` step and PIN-block count that no document confirmed.
Method: documentation only; no commands were run.
