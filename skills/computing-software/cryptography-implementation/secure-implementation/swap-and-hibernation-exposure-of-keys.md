---
id: computing-software.cryptography-implementation.secure-implementation.swap-and-hibernation-exposure-of-keys
name: swap-and-hibernation-exposure-of-keys
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, encrypted-swap, mlock, hibernation, crash-dumps, secure-memory, key-exposure]
level: practitioner
status: docs-checked
description: "Keep keys out of swap, hibernation images and crash dumps: random-key encrypted swap, mlock, disabling hibernation on key hosts, and dump controls."
sources: ["https://man7.org/linux/man-pages/man2/mlock.2.html", "https://wiki.archlinux.org/title/Dm-crypt/Swap_encryption", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/memory-dump-file-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swap and hibernation exposure of keys

## Paths out of RAM
- **Swap**: pages with keys written to disk in clear and persist after process exit.
- **Hibernation**: entire RAM image written to disk.
- **Core dumps / crash reports**: process memory sent to disk or to vendors (systemd-coredump, Windows Error
  Reporting, apport).

## Controls
- **Encrypt swap** with an ephemeral random key per boot (`/etc/crypttab`: `swap <stable-device-path> /dev/urandom swap,cipher=aes-xts-plain64,size=512`),
  or run without swap on key servers. A random-key swap is discarded at shutdown, so it rules out suspend-to-disk.
  Never name the device as `/dev/sdX#`: names change between boots and crypttab will reformat whatever is there; use a
  stable by-id, PARTUUID or PARTLABEL path (see the Arch wiki page).
- **mlock** key pages: `mlock(2)` or libsodium `sodium_mlock`. Locking is bounded by `RLIMIT_MEMLOCK` unless the
  process has `CAP_IPC_LOCK`.
- **Hibernation**: disable it on key servers; on laptops keep the hibernation image on an encrypted volume.
- **Dumps**: disable or protect core dumps and crash reports for key-holding processes; check your OS documentation.

## Checked

2026-10-31. Confirmed in the Arch wiki dm-crypt swap page (random-key crypttab entry, discarded at shutdown, no suspend-to-disk, device-name warning, swapon -s and lsblk crypt check), mlock(2) (RLIMIT_MEMLOCK, CAP_IPC_LOCK) and libsodium memory management (sodium_mlock avoids swapping). Removed: default limit sizes, sodium_malloc, systemd hibernate/LimitMEMLOCK/LimitCORE, prctl/madvise, Windows pagefile and dump details (not confirmed in fetched pages).

Method: documentation only; no commands were run.

## Verify
- [ ] `swapon -s` and `lsblk` show swap on a `crypt` device or no swap; a test crash produces no core containing a
  canary key.
