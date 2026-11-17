---
id: computing-software.systems-network-administration.linux.encrypted-swap
name: encrypted-swap
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, encrypted-swap, swap, crypttab, random-key, luks, hibernation, plain-dm-crypt]
level: practitioner
status: docs-checked
description: "Encrypt swap so memory contents never hit disk in clear: random-key swap via crypttab, stable device references, the hibernation exception, and zram as an alternative."
sources:
  - https://github.com/systemd/systemd/blob/main/man/crypttab.xml
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/common_options.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted swap

**Why:** swap can contain passwords, keys and decrypted data. On an otherwise-encrypted system, clear swap defeats the encryption.

## Random key per boot (no hibernation)
`/etc/crypttab`:
```
cryptswap  /dev/disk/by-partuuid/0a1b2c3d-...  /dev/urandom  swap,cipher=aes-xts-plain64,size=512,sector-size=4096
```
`/etc/fstab`:
```
/dev/mapper/cryptswap  none  swap  defaults  0 0
```
The `swap` option (implies plain mode) formats the mapping with mkswap after setting it up, destroying the contents of the underlying partition at every boot. Reboot (or `systemctl daemon-reload && systemctl start systemd-cryptsetup@cryptswap`).

**Use a stable device path (for example under `/dev/disk/by-partuuid/`, `by-partlabel/` or `by-id/`), never `/dev/sdX`.** If `sdX` names shift, mkswap overwrites the wrong partition. crypttab documents the second field as a block device path or file, or `UUID=`; a filesystem UUID on the swap partition changes whenever it is re-formatted.

## With hibernation
A random key per boot cannot survive a reboot, so it cannot be used to resume from hibernation. Put swap inside a persistent encrypted container (for example a swap LV in an encrypted PV) and point the kernel `resume=` parameter at that device (distribution-specific setup).

## Alternatives
- zram (compressed RAM swap, not written to disk).
- A swap file on an already-encrypted root filesystem is encrypted by the underlying LUKS (check that your filesystem supports swap files).

## Verify
- [ ] `swapon --show` lists `/dev/mapper/cryptswap` (or `dm-N`); `cryptsetup status cryptswap` shows the cipher.

## Checked

Checked against systemd man/crypttab.xml (main branch, fetched 2026-10-25) and the cryptsetup man pages.
Confirmed: the `swap` option implies plain mode, formats with mkswap and destroys the partition contents on every boot; `/dev/urandom` as key file gives a randomised key; `cipher=`, `size=` and `sector-size=` options; the second field accepts a path or `UUID=`.
Removed unconfirmed claims: the `sgdisk -c` PARTLABEL step, `lsblk` output, and the TPM/passphrase swap-partition resume recipe.

Method: documentation only; no commands were run.
