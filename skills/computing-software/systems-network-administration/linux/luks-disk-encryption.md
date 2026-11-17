---
id: computing-software.systems-network-administration.linux.luks-disk-encryption
name: luks-disk-encryption
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, luks, luks2, cryptsetup, disk-encryption, encryption, crypttab, dm-crypt, keyfile, luks-header, header-backup, clevis, tang, tpm2, systemd-cryptenroll, full-disk-encryption, storage, rhcsa, sysadmin, luks-keyslots, luks-resize, luks-convert]
level: practitioner
status: docs-checked
description: "Encrypt a block device with LUKS2 via cryptsetup, open it at boot through crypttab, and manage key slots, header backups and TPM/Tang auto-unlock."
sources:
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-luksFormat.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-luksHeaderBackup.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-convert.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/FAQ.md
  - https://github.com/systemd/systemd/blob/main/man/systemd-cryptenroll.xml
  - https://github.com/systemd/systemd/blob/main/man/crypttab.xml
  - https://github.com/latchset/clevis/blob/master/src/luks/clevis-luks-bind.1.adoc
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# LUKS disk encryption — encrypt a data volume and still be able to boot and recover it

**Goal:** put a LUKS2 container on a block device, map it as `/dev/mapper/<name>`, mount it
at boot, and never lose the data to a forgotten passphrase or a scribbled header.

## 1. Create and open
```bash
cryptsetup luksFormat --type luks2 /dev/sdb1        # DESTROYS data; asks for passphrase, type YES
cryptsetup open /dev/sdb1 data                      # -> /dev/mapper/data
mkfs.xfs /dev/mapper/data
cryptsetup luksDump /dev/sdb1                       # key slots, cipher, PBKDF
```
- Format the **partition or LV**, then put the filesystem inside the mapping. LVM-on-LUKS
  (one encrypted PV, several LVs) is the usual layout for whole disks; LUKS-on-LVM is for
  encrypting one volume.
- LUKS2 is the default format; `--type luks1` selects LUKS1 (PBKDF2 only).
- Argon2's memory cost is a maximum that the benchmark or available RAM can lower, and it needs real physical RAM:
  out-of-memory failures abort cryptsetup operations. On small machines set `--pbkdf-memory` (kilobytes, for example `262144`) explicitly.

## 2. Mount at boot: crypttab + fstab
```
# /etc/crypttab   name   device                                    keyfile  options
data   UUID=<luks-uuid-of-/dev/sdb1>   none   luks,discard
# /etc/fstab
/dev/mapper/data   /srv/data   xfs   defaults,nofail,x-systemd.device-timeout=30   0 0
```
- The UUID in crypttab is the LUKS container's (`blkid /dev/sdb1`), not the filesystem's.
- `none` prompts at boot (`systemd-ask-password`); a keyfile path unlocks silently. Keep a
  keyfile at `/etc/luks/data.key`, mode `0400`, owned by root — and only when root itself is
  encrypted or the threat model accepts it.
- `discard` allows TRIM requests through to the device (`--allow-discards`).
- Root-on-LUKS: regenerate the initramfs after editing crypttab (`update-initramfs -u` on Debian-like systems, `dracut -f` on Fedora-like systems).

## 3. Key slots (8 in LUKS1, 32 in LUKS2)
```bash
cryptsetup luksAddKey /dev/sdb1                      # add a second passphrase
cryptsetup luksAddKey /dev/sdb1 /etc/luks/data.key   # add a keyfile
cryptsetup luksChangeKey /dev/sdb1
cryptsetup luksKillSlot /dev/sdb1 1                   # remove by slot number (needs another valid passphrase)
cryptsetup luksRemoveKey /dev/sdb1                    # remove by supplying the passphrase
```
Always keep ≥2 independent unlock methods (human passphrase + keyfile or TPM); never kill
the last slot you can actually use.

## 4. Auto-unlock without a human
- **TPM2 (laptops, servers with TPM):**
  `systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 /dev/sdb1` and add `tpm2-device=auto`
  to the crypttab options. PCR 7 is the Secure Boot policy (it changes when Secure Boot is toggled or firmware
  certificates change); the systemd documentation says encrypted volumes are typically bound to PCRs 7, 11 and 14,
  and that PCRs such as 0 and 2 are usually unnecessary because the certificates measured into PCR 7 already cover them. Add
  `systemd-cryptenroll --recovery-key /dev/sdb1` and store it off-box.
- **Network-bound (datacentre):** Clevis + Tang. `clevis luks bind -d /dev/sdb1 tang '{"url":"http://tang.example"}'`;
  this adds a keyslot, so the existing passphrase still works, and automatic unlock needs the Tang server. Enable a Clevis LUKS unlocker
  (see clevis-luks-unlockers(7)) and, with dracut, network in the initramfs (`rd.neednet=1` brings up the network).
- FIDO2 keys: `systemd-cryptenroll --fido2-device=auto`.

## 5. Header backup and recovery
```bash
cryptsetup luksHeaderBackup /dev/sdb1 --header-backup-file sdb1-luks-header.img
cryptsetup luksHeaderRestore /dev/sdb1 --header-backup-file sdb1-luks-header.img
```
The header holds the key slots (the default LUKS2 header is 16 MiB). A dead header means unrecoverable
data even with the passphrase. Back it up **after every key change** and store it where
the disk isn't. Note: the backup and a passphrase valid at backup time still decrypt the data after that passphrase was changed or removed — killing a slot is not
revocation while an old header backup exists.

## 6. Resizing, reencrypting, and performance
- Grow: extend the partition/LV, then `cryptsetup resize data` (resizes the active mapping), then `xfs_growfs`.
- Change cipher, volume key or sector size: `cryptsetup reencrypt`; convert between formats with `cryptsetup convert --type luks2` (not possible with extra LUKS2 features, and LUKS2 to LUKS1 needs all keyslots on PBKDF2).
  Take a header backup first; an interrupted reencrypt is resumed with `reencrypt --resume-only`.
- Throughput: `cryptsetup benchmark` is memory-only and informative. `--perf-no_read_workqueue --perf-no_write_workqueue` (open/refresh; persist via `--persistent`) bypass the dm-crypt workqueue.

## Failure modes
- A wrong UUID in crypttab (it must be the LUKS container's UUID) leaves the volume unopened; `nofail` in fstab keeps a non-root volume from blocking boot.
- After a Secure Boot or firmware-certificate change the PCR 7 binding no longer matches and TPM unlock stops: use the recovery
  key, then re-enroll (`systemd-cryptenroll --wipe-slot=tpm2 --tpm2-device=auto /dev/sdb1`; `tpm2` wipes all slots unlocked by a TPM2 chip).

## Verify
- [ ] `lsblk -f` shows `crypto_LUKS` on the device and the filesystem on `/dev/mapper/<name>`.
- [ ] Reboot: the volume mounts (or prompts) without dropping to emergency mode.
- [ ] `cryptsetup luksDump` shows the expected slots/tokens; header backup restored to a
      test copy opens with the passphrase.

## Checked

Checked against the cryptsetup main branch (man pages and FAQ, configure.ac), systemd man/systemd-cryptenroll.xml and man/crypttab.xml, and latchset/clevis (README, clevis-luks-bind), documentation fetched 2026-10-25.
Confirmed: LUKS2 is the default format; 8 keyslots in LUKS1 and up to 32 in LUKS2 (FAQ); luksAddKey/luksRemoveKey/luksChangeKey behaviour; header backup semantics; default LUKS2 header size 16 MiB; `cryptsetup resize` and `convert` behaviour; systemd-cryptenroll `--tpm2-device=auto`, `--tpm2-pcrs`, `--recovery-key`, `--fido2-device=auto`, `--wipe-slot=tpm2`; PCR 7 is the Secure Boot policy; `clevis luks bind -d DEV tang '{"url":...}'` adds a keyslot; `rd.neednet=1`.
Fixed: the Argon2 memory claim ("half of RAM up to 1 GiB") is not documented, and the PCR 0+7 advice contradicts the systemd guidance. Removed unconfirmed claims: LUKS1 GRUB version gate, initramfs hook behaviour, the Clevis package names, the keyboard-layout and 90-second boot hang failure modes, and the multi-GB/s throughput remark.

Method: documentation only; no commands were run.
