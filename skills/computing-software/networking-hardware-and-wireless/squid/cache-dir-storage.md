---
id: computing-software.networking-hardware-and-wireless.squid.cache-dir-storage
name: cache-dir-storage
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cache-dir, ufs, aufs, diskd, rock]
level: practitioner
status: docs-checked
description: "Configure the disk cache with cache_dir: store types ufs, aufs, diskd and rock, size fields and options."
sources:
  - https://www.squid-cache.org/Doc/config/cache_dir/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache_dir storage
Syntax: `cache_dir Type Directory-Name Fs-specific-data [options]`. Multiple lines spread the cache over partitions. Default: no disk cache, memory only.

Types:
- `ufs`: `cache_dir ufs Directory-Name Mbytes L1 L2`; the only type built by default
- `aufs`: ufs format with POSIX-thread disk I/O
- `diskd`: ufs format with a helper process; queue limits Q1 (64) and Q2 (72)
- `rock`: fixed-size slot database, the only SMP-aware type

Fields: Mbytes defaults to 100 (for a whole disk subtract about 20%); L1 defaults to 16; L2 to 256. The directory must exist and be writable by Squid.

Options: `no-store`, `min-size`, `max-size` (smallest max-size first), and for rock `max-swap-rate`, `swap-timeout`, `slot-size` (default 16 KBytes).

The other types need `--enable-storeio`.

## Checked

2026-11-04. Read the cache_dir directive page and confirmed the types, ufs field defaults, diskd Q1 and Q2 defaults, rock slot-size default and the common options. Nothing was removed.

Method: documentation only; no commands were run.
