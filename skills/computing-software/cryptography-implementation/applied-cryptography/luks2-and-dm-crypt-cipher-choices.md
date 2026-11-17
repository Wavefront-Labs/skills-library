---
id: computing-software.cryptography-implementation.applied-cryptography.luks2-and-dm-crypt-cipher-choices
name: luks2-and-dm-crypt-cipher-choices
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, luks2-cipher, luks2, luks, dm-crypt, cryptsetup, aes-xts, argon2id, disk-encryption, adiantum, header-backup]
level: practitioner
status: gated
description: "Configure LUKS2 with cryptsetup: aes-xts-plain64 key size, Argon2id PBKDF tuning, header backup, keyslot management, Adiantum and integrity options."
sources: ["https://gitlab.com/cryptsetup/cryptsetup/-/wikis/FrequentlyAskedQuestions", "https://man7.org/linux/man-pages/man8/cryptsetup.8.html", "https://www.kernel.org/doc/html/latest/admin-guide/device-mapper/dm-crypt.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUKS2 and dm-crypt cipher choices

## Format with explicit, reviewed parameters
```
cryptsetup luksFormat --type luks2 \
  --cipher aes-xts-plain64 --key-size 512 \
  --pbkdf argon2id --pbkdf-memory 1048576 --pbkdf-parallel 4 --iter-time 2000 \
  /dev/nvme0n1p3
cryptsetup luksDump /dev/nvme0n1p3      # confirm cipher, keyslots, PBKDF params
```
- `--key-size 512` with XTS means AES-256 (XTS splits the key in two).
- `--pbkdf argon2id` is set explicitly; the LUKS2 default PBKDF is chosen at compile time (see `cryptsetup --help`). `--pbkdf-memory` is in KiB (1 GiB above) and is a maximum that the benchmark or available RAM can lower; `--pbkdf-parallel` goes up to 4. Benchmarked memory cost stays between 64 MiB and 1 GiB; larger values need `--pbkdf-memory`. Memory-hard settings must still
  fit the smallest machine that must unlock (initramfs, recovery media).
- Check speed and hardware support: `cryptsetup benchmark`.

## Keyslots
```
cryptsetup luksAddKey /dev/X                # add passphrase or keyfile
cryptsetup luksKillSlot /dev/X 1            # remove a slot
systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 /dev/X   # TPM-bound slot
systemd-cryptenroll --fido2-device=auto /dev/X
```
Keep a recovery passphrase or `systemd-cryptenroll --recovery-key` slot stored offline.

## Header backup (do this)
```
cryptsetup luksHeaderBackup /dev/X --header-backup-file luks-header.img
```
A corrupted header is unrecoverable data loss. Store the backup encrypted and offline; it can be attacked with the
old passphrases, so regenerate it after removing a slot (gated: unconfirmed, source is paywalled or blocked).

## Alternatives
- Low-end CPUs without AES instructions: Adiantum (`--cipher xchacha12,aes-adiantum-plain64`) (gated: unconfirmed, source is paywalled or blocked).
- Authenticated disk encryption: `--integrity hmac-sha256` (dm-integrity; slower, initialisation wipes the device).
- Re-encrypt in place to change cipher or rotate the volume key: `cryptsetup reencrypt /dev/X`.

## Gotchas
- `luksChangeKey` changes a passphrase, not the volume key; after a compromise run `cryptsetup reencrypt`.
- Detached headers (`--header`) hide that the disk is LUKS but you must not lose the header file.
- TRIM (`--allow-discards`, a `cryptsetup open` option) leaks which blocks are in use (gated: unconfirmed, source is paywalled or blocked); decide explicitly.

## Verify
- [ ] `luksDump` shows aes-xts-plain64, 512-bit key, argon2id.
- [ ] Header backup exists offline and restores on a test copy.
- [ ] Recovery passphrase unlocks on a clean boot medium.

## Checked

- Date: 2026-11-02.
- Confirmed against: cryptsetup-luksFormat man page (--pbkdf argon2id, --pbkdf-memory in kilobytes and a maximum, --pbkdf-parallel up to 4, --iter-time, --key-size, --integrity, LUKS2 default PBKDF set at compile time, benchmarked memory range), cryptsetup man page (luksChangeKey changes an existing passphrase, luksHeaderBackup), cryptsetup-open (--allow-discards), systemd-cryptenroll man page (--tpm2-device, --tpm2-pcrs, --fido2-device, --recovery-key).
- Removed: the claim that Argon2id is the LUKS2 default.
- Gated: the Adiantum cipher string, header-backup attack remark and TRIM leakage remark (the cryptsetup FAQ wiki returned an empty page).

Method: documentation only; no commands were run.
