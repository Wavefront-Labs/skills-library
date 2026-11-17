---
id: computing-software.cybersecurity-defensive.endpoint-security.luks-disk-encryption
name: luks-disk-encryption
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [full-disk-encryption, luks, luks2, cryptsetup, tpm2-unlock, systemd-cryptenroll, clevis, tang, network-bound-disk-encryption]
level: practitioner
status: draft
description: "Encrypt Linux disks with LUKS2: install-time setup, key slots, TPM2 or Clevis/Tang unattended unlock for servers, header backup and recovery."
sources: ["cryptsetup and LUKS2 documentation (gitlab.com/cryptsetup)", "systemd-cryptenroll man page", "Red Hat Enterprise Linux 9 Security Hardening - Encrypting block devices with LUKS and NBDE (Clevis/Tang)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LUKS disk encryption

**Goal:** Linux laptops and servers keep data encrypted at rest, servers can still boot
unattended, and keys can be recovered.

## Setup
Best done at install time (distribution installer "Encrypt my data"). For a data volume:
```
cryptsetup luksFormat --type luks2 --pbkdf argon2id /dev/sdb1
cryptsetup open /dev/sdb1 data
mkfs.xfs /dev/mapper/data
```
Add to `/etc/crypttab` and `/etc/fstab`. Check: `cryptsetup luksDump /dev/sdb1` (cipher `aes-xts-plain64`, 512-bit key = AES-256).

## Key slots
LUKS2 has multiple key slots: add a recovery passphrase stored in your vault, plus machine unlock:
```
cryptsetup luksAddKey /dev/sda3                     # recovery passphrase
systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 /dev/sda3   # TPM2 unlock bound to Secure Boot state
```
Then `rd.luks.options=tpm2-device=auto` / crypttab `tpm2-device=auto` for automatic unlock.

## Servers: Network-Bound Disk Encryption (Clevis + Tang)
Tang servers on the internal network; disks unlock only when the server can reach Tang (stolen
disks/servers taken off-site stay locked):
```
clevis luks bind -d /dev/sda3 tang '{"url":"http://tang1.example.internal"}'
dracut -fv --regenerate-all     # include clevis in initramfs
```
Use `sss` pin for thresholds (e.g. 1 of 2 Tang servers, or TPM + Tang).

## Header backup and recovery
```
cryptsetup luksHeaderBackup /dev/sda3 --header-backup-file sda3-luks-header.img
```
Store header backups and recovery passphrases securely (vault); a damaged header without a backup means data loss.

## Gotchas
- TPM PCR binding to firmware state (PCR 0/2) breaks unlock after firmware updates; PCR 7 (Secure Boot) is more stable, then re-enrol after changes.
- Cloud VMs: provider disk encryption is usually simpler; LUKS inside VMs needs key delivery at boot.
- Removing the last passphrase slot without a recovery key is irreversible.

## Verify
- [ ] `lsblk -f` shows crypto_LUKS for data/root volumes; recovery passphrase tested.
- [ ] Server boots unattended on the network and stays locked when Tang is unreachable (test).
