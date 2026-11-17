---
id: computing-software.cloud-infrastructure-engineering.rook.rook-supported-platforms-and-devices
name: rook-supported-platforms-and-devices
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [prerequisites, kubernetes-version, raw-devices, lsblk, devicefilter]
level: intro
status: docs-checked
description: "Check Kubernetes version support, CPU architecture and which local devices Rook can turn into OSDs, using lsblk to spot formatted disks."
sources:
  - https://rook.io/docs/rook/latest-release/Getting-Started/Prerequisites/prerequisites/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rook runs on any Kubernetes cluster that meets the minimum version and grants Rook its required privileges. The prerequisites page lists Kubernetes v1.32 through v1.37 and the amd64 and arm64 architectures.

At least one of these storage types must exist for the Ceph cluster:
- raw devices with no partitions or filesystem
- raw partitions with no filesystem
- LVM logical volumes with no filesystem
- Persistent Volumes from a storage class in block mode

The quickstart also lists encrypted and multipath devices without a filesystem.

When selecting devices on a node (`useAllDevices`, `deviceFilter`, `devicePathFilter` or `devices`), Rook skips rbd, nbd, drbd and zram devices. OSDs on PVCs are unaffected by this rule.

Check for filesystems with:
```
lsblk -f
```
If the `FSTYPE` column is not empty for a device, a filesystem sits on it and Rook will not use it. In the docs example, `vdb` is free while `vda` and its partitions hold a filesystem.

Self-check: every node you expect to host OSDs shows at least one device with an empty `FSTYPE`, and its name is not matched by the skip list above.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (prerequisites) against this skill: 9 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
