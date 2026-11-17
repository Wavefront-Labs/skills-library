---
id: computing-software.digital-forensics-incident-response.evidence-handling.forensic-boot-media-for-acquisition
name: forensic-boot-media-for-acquisition
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [forensic-boot-media, write-blocking, software-write-blocker, disk-imaging, dfir]
level: practitioner
status: draft
description: "Acquire disks by booting forensic Linux media (CAINE, Paladin, Tsurugi): firmware settings, read-only mounting policy, imaging and verification."
sources: ["https://www.caine-live.net/", "https://sumuri.com/paladin/", "https://tsurugi-linux.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forensic boot media for acquisition

**Goal:** image a drive that cannot easily be removed (soldered storage, ultrabooks, servers with
hardware RAID) by booting a forensic live OS that does not auto-mount or write to internal disks.

## Prepare
- Use a known distribution (CAINE, Paladin, Tsurugi) and validate it on a test machine first:
  boot, attach a hashed test disk, image it, confirm the source hash is unchanged.
- External evidence drive formatted (exFAT/ext4) with enough space; label it.

## Firmware
- Enter firmware setup: record BIOS/UEFI clock vs real UTC (photograph it) - this is your clock offset.
- Disable Secure Boot if the media is not signed (Paladin and CAINE support Secure Boot on recent versions).
- Set one-time boot to USB; never let the internal OS start.
- Note storage mode (RAID/Intel RST vs AHCI): RST may hide NVMe drives from Linux; switching to
  AHCI is a change to firmware settings - document it, or image the RAID volume via the OS instead.

## Acquire
```bash
lsblk -o NAME,SIZE,MODEL,SERIAL,RO      # identify internal disk; confirm RO=1 where tool sets it
blockdev --getro /dev/nvme0n1           # 1 = read-only
ewfacquire -t /media/evid/CASE-001 -c best -f encase6 -S 0 /dev/nvme0n1
# or: guymager (GUI) / dc3dd if=/dev/nvme0n1 hof=img.dd hash=sha256 log=acq.log
```

## Gotchas
- Apple T2 / Apple silicon Macs cannot boot third-party Linux for internal disk access; use target disk/share mode instead.
- BitLocker drives image as ciphertext; capture recovery key or image live first.
- Some live distributions auto-mount on double-click in the file manager; never browse internal partitions.

## Verify
Source hash matches image hash, the RO state was recorded, and the firmware clock offset is documented.
