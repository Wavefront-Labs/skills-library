---
id: computing-software.systems-network-administration.linux.btrfs-space-accounting-and-qgroups
name: btrfs-space-accounting-and-qgroups
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, btrfs, btrfs-filesystem-usage, btrfs-qgroups, btrfs-balance, enospc, metadata-full]
level: advanced
status: docs-checked
description: "Understand Btrfs space: btrfs filesystem usage vs df, data/metadata chunk allocation, ENOSPC with free space, balance filters, and per-subvolume accounting with qgroups."
sources:
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-filesystem.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-balance.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-balance-filters.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-quota.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/btrfs-qgroup.rst
  - https://github.com/kdave/btrfs-progs/blob/master/Documentation/ch-quota-intro.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Btrfs space accounting

## See real usage
```bash
btrfs filesystem usage -T /
#             Data     Metadata  System
# Size        90.00GiB  3.00GiB  32MiB    <- allocated chunks
# Used        60.10GiB  2.95GiB  ...      <- metadata nearly full!
# Device unallocated: 0.00B               <- no room to allocate new chunks
btrfs filesystem df /
```
Plain `df` cannot show block-group allocation; `btrfs filesystem usage` reports allocated and unallocated space, while `btrfs filesystem df` is a terse debugging summary.

## "No space left" with free space
Cause: all raw space is allocated to chunks, and the type you need (usually metadata) is full while data chunks are half empty.
```bash
btrfs balance start -dusage=10 /      # repack data chunks <10% used, freeing unallocated space
btrfs balance start -dusage=50 /      # escalate gradually
btrfs balance start -musage=50 /      # metadata, sparingly
btrfs balance status /
```
Balance needs free work space at block-group level (size minus used per device in `btrfs filesystem show`). If it fails with ENOSPC, start with `-dusage=0`, which needs no work space.

## Per-subvolume usage (qgroups)
```bash
btrfs quota enable /                  # or 'btrfs quota enable --simple' (simple quotas, squota)
btrfs qgroup show -reF /              # referenced/exclusive per qgroup; -r/-e add limits, -F = qgroups impacting the path
btrfs qgroup limit 50G /srv/projects/alpha    # limit a subvolume
```
Exclusive is data whose references are all inside that qgroup. Full qgroup accounting can slow transaction commits where snapshots scale up; simple quotas (squotas) are the documented alternative.

## Verify
- [ ] `Device unallocated` has headroom; qgroup report explains where the space is.

## Checked
Checked 2026-10-26 against btrfs-progs Documentation (master, pushed 2026-10-23): btrfs-filesystem, btrfs-balance and balance filters, btrfs-quota, btrfs-qgroup, ch-quota-intro.
Confirmed: `filesystem usage -T`, `Device unallocated`, balance `-dusage`/`-musage` filters and `usage=0` needing no work space, `btrfs quota enable --simple`, `qgroup show -r -e -F` and `qgroup limit`, definitions of referenced and exclusive.
Wrong in the draft: `-r -e` on qgroup show print limits rather than referenced/exclusive columns; the loop-device and global-reserve ENOSPC advice is not in the docs.
Removed as unconfirmed: the kernel 6.7 squota claim and the btdu mention.
Method: documentation only; no commands were run.
