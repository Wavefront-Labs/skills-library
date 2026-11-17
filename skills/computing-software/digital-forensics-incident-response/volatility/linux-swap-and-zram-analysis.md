---
id: computing-software.digital-forensics-incident-response.volatility.linux-swap-and-zram-analysis
name: linux-swap-and-zram-analysis
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [swap-analysis, zram, linux-swap, linux-memory-forensics, dfir]
level: advanced
status: docs-checked
description: "Analyse Linux swap partitions, swap files and zram: collecting them, string and YARA searching, encrypted swap, compressed zram pages in memory images, and what each can prove."
sources: ["https://man7.org/linux/man-pages/man8/swapon.8.html", "https://docs.kernel.org/admin-guide/blockdev/zram.html", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux swap and zram analysis

Pages evicted from RAM go to swap (partition or file) or to zram: a compressed RAM-based block device (`/dev/zram<id>`) that can be used as a swap device. Both can hold passwords, commands, decrypted data and fragments of malware long after the process ended.

## Identify what is in use
Live: `swapon --show` (the older `swapon -s` / `/proc/swaps` output is marked deprecated in favour of it). For zram, `/sys/block/zram0/comp_algorithm` shows the algorithm. Offline: `/etc/fstab` lists swap devices and files.

## Collecting
- Swap partition or swap file: image it like any block device or file (from a forensic boot, or on a live system after memory capture). Swap files live on a file system and are in the disk image.
- zram: its contents live in RAM, so capture full memory first. A live read of the block device (for example `dd if=/dev/zram0`) is an option; record that it was read live (practitioner guidance, not covered by the kernel page).
- Encrypted swap: if the key is not kept, the swap is unreadable after shutdown (practitioner guidance); capture while live.

## Analysis
Swap has no file system; this skill treats it as unstructured data (the Volatility 3 documentation read here does not describe swap-aware translation for Linux):
```bash
strings -a -t d swap.dd | grep -iE 'password=|BEGIN (RSA|OPENSSH) PRIVATE|bash -i|/dev/tcp/'
yara -r rules/ swap.dd
```
Linking swap content back to processes requires page tables from a memory image taken at the same time, which is rarely practical: report findings as present on the host, not attributed to a process unless otherwise corroborated.

zram compresses pages in RAM; the kernel page lists the algorithms (lzo, lz4, zstd and others, shown in `comp_algorithm`, with the active one in brackets). A raw memory image therefore holds compressed data that plain strings will not see.

## Gotchas
- Swap content is persistent across reboots until overwritten; old data may predate the incident. Date it by content.

## Verify
Hits reported from swap or zram include the offset, the surrounding bytes, and a clear statement that process attribution is or is not established.

## Checked

- Confirmed: swapon --show, zram as RAM block device usable as swap, compression algorithm selection. Forensic handling advice is practitioner guidance, not source-confirmed.

Method: docs-checked 2026-11-09 against man7 swapon(8) (--show, /proc/swaps deprecation note) and kernel zram admin-guide page (comp_algorithm, /dev/zram<id>, swap use). DFRWS and bulk_extractor sources were unreadable/unchecked and dropped, along with zsmalloc, zramctl, zram-generator, partition type, hibernation and encrypted-swap specifics.
