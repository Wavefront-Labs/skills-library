---
id: computing-software.digital-privacy-hygiene.device-hardening.linux-full-disk-encryption-with-luks
name: linux-full-disk-encryption-with-luks
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, luks, cryptsetup, disk-encryption, linux, systemd-cryptenroll, tpm, fido2]
level: advanced
status: docs-checked
description: "Set up, audit and maintain LUKS2 full-disk encryption on Linux: install-time setup, key slots, header backup, Argon2id, and TPM2/FIDO2 unlock with systemd-cryptenroll."
sources:
  - "https://gitlab.com/cryptsetup/cryptsetup"
  - "https://wiki.archlinux.org/title/Dm-crypt/Encrypting_an_entire_system"
  - "https://www.freedesktop.org/software/systemd/man/latest/systemd-cryptenroll.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux full-disk encryption with LUKS

**Goal:** a stolen Linux laptop reveals nothing; you can still recover if a passphrase or header is lost.

## Set it up at install (easiest)
- Most distro installers offer an encrypted-install option (look for disk encryption or encrypted LVM
  in the storage step). `/boot` and the EFI partition usually stay unencrypted.
- Encrypting an existing device in place is possible (`cryptsetup reencrypt --encrypt --type luks2
  --reduce-device-size 32m /dev/plaintext_device`, from the cryptsetup-reencrypt man page)
  but needs a full backup first; reinstalling is usually safer.

## Audit an existing system
```bash
lsblk -f                                 # look for TYPE crypto_LUKS
sudo cryptsetup luksDump /dev/nvme0n1p3  # version (want LUKS2), key slots, PBKDF
```
- LUKS2 supports different PBKDF algorithms; `luksConvertKey` converts an existing LUKS2 keyslot to
  new PBKDF parameters (see the cryptsetup-luksConvertKey man page). LUKS1 has no such conversion.

## Key slots and backups
```bash
sudo cryptsetup luksAddKey /dev/nvme0n1p3          # add a second (recovery) passphrase
sudo cryptsetup luksKillSlot /dev/nvme0n1p3 2      # remove a slot
sudo cryptsetup luksHeaderBackup /dev/nvme0n1p3 --header-backup-file luks-header.img
```
A damaged header destroys the data permanently; store the header backup offline (it plus an old passphrase
unlocks the disk, so protect it like a key).

## Hardware-backed unlock (systemd-cryptenroll)
```bash
sudo systemd-cryptenroll --fido2-device=auto /dev/nvme0n1p3           # security key
sudo systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 /dev/nvme0n1p3 # TPM bound to chosen PCRs
```
PCRs bind the key to specific software versions and system state; read the PCR section of the man page
before choosing. Enrolled methods are also listed in the volume's `/etc/crypttab` options (see crypttab(5)).
TPM-only unlock is convenient but means the disk opens for whoever powers the laptop on; add a TPM PIN
(`--tpm2-with-pin=yes`) for real protection.

## Gotchas
- Power off rather than suspend when leaving the laptop somewhere risky.
- Keep a passphrase slot even after enrolling TPM/FIDO2.

## Checked
2026-11-01. Confirmed against the cryptsetup man pages (luksAddKey, luksKillSlot, luksHeaderBackup, luksDump, luksConvertKey, reencrypt options) and the systemd-cryptenroll page (fido2, tpm2, PCRs, tpm2-with-pin, crypttab). Removed: installer menu names, argon2id-default claim, initramfs step, suspend key-in-RAM claim.
Method: documentation only; no commands were run.

## Verify
- [ ] `lsblk -f` shows crypto_LUKS under root and swap.
- [ ] `luksDump` shows LUKS2, argon2id, and at least two usable slots.
- [ ] Header backup stored offline.
