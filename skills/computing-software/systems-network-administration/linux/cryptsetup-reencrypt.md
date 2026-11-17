---
id: computing-software.systems-network-administration.linux.cryptsetup-reencrypt
name: cryptsetup-reencrypt
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, luks, cryptsetup-reencrypt, luks-reencrypt, encrypt-existing-disk, volume-key-rotation, luks2]
level: advanced
status: docs-checked
description: "Use cryptsetup reencrypt (LUKS2) to encrypt an existing filesystem in place, rotate the volume key or change cipher online, with resilience modes, backups and resume."
sources:
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/cryptsetup-reencrypt.8.adoc
  - https://gitlab.com/cryptsetup/cryptsetup/-/blob/main/man/common_options.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cryptsetup reencrypt

**Uses:** encrypt a disk that was installed unencrypted; rotate the master (volume) key after a
compromise suspicion (changing a passphrase does NOT change the volume key); move to a new cipher.

## Always: backup and header backup first
Interruptions are designed to be recoverable (resilience journal), but power loss + bugs + bad disks exist.

## Encrypt an existing filesystem in place
```bash
# the last 32 MiB of the device must be unused (--reduce-device-size 32M): shrink the filesystem first
e2fsck -f /dev/sdb1 && resize2fs /dev/sdb1 <size-minus-32M>      # XFS cannot shrink: needs a new device or detached header
cryptsetup reencrypt --encrypt --type luks2 --reduce-device-size 32M /dev/sdb1
cryptsetup open /dev/sdb1 data && mount /dev/mapper/data /data
```
Then add `/etc/crypttab` and change fstab to `/dev/mapper/data`.

## Rotate the volume key / change cipher (online, while mounted)
```bash
cryptsetup reencrypt /dev/nvme0n1p3                                  # new volume key, same params
cryptsetup reencrypt /dev/nvme0n1p3 --cipher aes-xts-plain64 --key-size 512
```
With an active mapping this is online LUKS2 reencryption; without one it is offline. The process may be interrupted safely (SIGINT or SIGTERM). To resume, run the reencrypt command again, or `cryptsetup reencrypt --resume-only /dev/nvme0n1p3` to avoid accidentally starting a new operation. After a crash, recovery runs at the next `open` or via `cryptsetup repair`.

## Decrypt
`cryptsetup reencrypt --decrypt --header /export/hdr.img /dev/sdb1` exports the LUKS2 header to a new file (which must not exist yet) and decrypts; with an existing detached header pass that file. Never put the exported header on a filesystem on the device being decrypted.

## Gotchas
- `--token-id` or `--token-type` selects keyslots by token, and all other keyslots are removed after reencryption finishes.
- If you need both `luksChangeKey` and `reencrypt` (for example after a leak), run luksChangeKey first.
- `--resilience checksum` (default; needs atomic sector writes), `journal` (data written twice) or `none` (no protection). Resilience cannot be changed for encryption started with `--reduce-device-size`.
- For LUKS1 the device must be offline and the working directory writable; the LUKS1 code is not resistant to hardware or kernel failures.

## Verify
- [ ] `cryptsetup luksDump` shows no reencryption still in progress; your own data checksums are unchanged.

## Checked

Checked against the cryptsetup main branch (man/cryptsetup-reencrypt, common_options), documentation fetched 2026-10-25.
Confirmed: encrypt/decrypt/reencrypt modes; `--reduce-device-size 32M` with the last 32 MiB unused; `--resume-only`; resilience modes and the checksum default; `--decrypt --header` semantics; token-based keyslot selection; LUKS1 offline requirement; luksChangeKey-then-reencrypt order.
Removed unconfirmed claims: resize2fs after opening, the `cryptsetup status` progress display, TPM/FIDO2 re-enrolment advice, the `online-reencrypt` luksDump string, and the throughput remark.

Method: documentation only; no commands were run.
