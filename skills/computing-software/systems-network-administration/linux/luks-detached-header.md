---
id: computing-software.systems-network-administration.linux.luks-detached-header
name: luks-detached-header
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, luks, cryptsetup, detached-header, luks-header-backup, plausible-deniability, crypttab, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Use LUKS2 with the header stored separately from the data (USB stick/boot media): create, open, crypttab with header=, header backup/restore, and the operational risks."
sources:
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/common_options.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-luksHeaderBackup.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-luksHeaderRestore.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-reencrypt.8.adoc
  - https://github.com/systemd/systemd/blob/main/man/crypttab.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUKS with a detached header

**Goal:** the encrypted disk contains only ciphertext (the LUKS header is stored elsewhere) and can't be opened without the separate header file — and you don't lock yourself out.

## 1. Create
```bash
cryptsetup luksFormat --type luks2 --header /mnt/usb/disk1.hdr /dev/sdb
cryptsetup open --header /mnt/usb/disk1.hdr /dev/sdb secure
mkfs.xfs /dev/mapper/secure
cryptsetup luksDump /mnt/usb/disk1.hdr          # dump the header file, not the disk
```
With a file name as the `--header` argument, luksFormat creates the file if it does not exist. The ciphertext device and header are stored separately; there is no check that a device belongs to a given header, so use the right pair.

## 2. Boot-time unlock
```
# /etc/crypttab
secure  /dev/disk/by-id/wwn-0x5000c500a1b2c3d4  none  luks,header=/boot/keys/disk1.hdr
# header on a separate filesystem: header=/disk1.hdr:UUID=<usb-fs-uuid> (path relative to that filesystem's root)
```
Root-on-LUKS with a detached header requires the header to be reachable from the initramfs (distribution-specific). Use a stable `by-id` path for the ciphertext device.

## 3. Back up the header — twice
Losing or corrupting the header means the data cannot be decrypted; no passphrase can help.
```bash
cryptsetup luksHeaderBackup --header /mnt/usb/disk1.hdr --header-backup-file /secure/disk1.hdr.bak
# with a header file, copying the file is also a backup; keep copies in two places, protected like keys
cryptsetup luksHeaderRestore --header /mnt/usb/disk1.hdr --header-backup-file /secure/disk1.hdr.bak
```
Note: the backup file and a passphrase valid at the time of the backup allow decryption even if the passphrase was later changed or removed, and a backup means you can no longer wipe the device securely just by overwriting the header: erase all backups or overwrite the data area. `luksHeaderRestore` replaces all keyslots, and requires that volume key size and data offset match. Changing a passphrase does not change the volume key; use `cryptsetup reencrypt` for that.

## 4. Convert an existing LUKS disk
For an existing LUKS2 device, `cryptsetup reencrypt --decrypt --header <new-file> <device>` exports the header to a file while decrypting; to keep the data encrypted, back up the data, run `luksFormat --header` freshly and restore. To encrypt a plaintext device with a detached header: `cryptsetup reencrypt --encrypt --type luks2 --header <file> <device>`. Never put an exported header on a filesystem on the device being decrypted.

## Gotchas
- Opening without `--header` fails because the device carries no LUKS header: expected, but document it.
- Header file on the root fs of the same encrypted system = chicken-and-egg at boot.

## Verify
- [ ] `cryptsetup isLuks /dev/sdb` reports no LUKS header on the ciphertext device.
- [ ] Opening with the header file works after reboot via crypttab.
- [ ] Header backup restores successfully onto a scratch copy (test it).

## Checked

Checked against the cryptsetup main branch (man/common_options `--header`, luksHeaderBackup, luksHeaderRestore, reencrypt) and systemd man/crypttab.xml, documentation fetched 2026-10-25.
Confirmed: `luksFormat --header <file>` creates the file; `open --header`; `luksHeaderBackup --header-backup-file`, `luksHeaderRestore` semantics and the security caveats; crypttab `header=path:UUID=...` syntax; reencrypt `--header` for encrypt and decrypt.
Removed unconfirmed claims: the 16 MiB truncate step, that the data starts at offset 0, the `blkid` result, the systemd 247 gate, the dracut `install_items` line, the TRIM/deniability remark and the quoted error string. Header size calculation: see the cryptsetup FAQ.

Method: documentation only; no commands were run.
