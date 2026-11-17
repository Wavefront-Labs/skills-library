---
id: computing-software.database-administration.scylladb.kb-system-limits-and-cpuset
name: kb-system-limits-and-cpuset
category: computing-software
field: database-administration
product: scylladb
tags: [system-limits, nofile, memlock, cpuset, perftune-yaml, irq]
level: advanced
status: docs-checked
description: "Required ScyllaDB OS limits (core, memlock, nofile 200000, as, nproc 8096 in limits.d scylla.conf) and customising CPUSET in cpuset.conf together with perftune.yaml irq_cpu_mask."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/system-limits.rst", "https://github.com/scylladb/scylladb/blob/master/docs/kb/customizing-cpuset.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# System limits and CPUSET

**Limits** (file `/etc/security/limits.d/scylla.conf`):
- `core`: unlimited (core dump size)
- `memlock`: unlimited (locked-in-memory address space)
- `nofile`: 200000 (open file descriptors)
- `as`: unlimited (address space)
- `nproc`: 8096 (processes)

**CPUSET**: `/etc/scylla.d/cpuset.conf` is set automatically by `scylla_setup` or `scylla_cpuset_setup`. To customise, change both `cpuset.conf` and `/etc/scylla.d/perftune.yaml`. The scylla-server service generates `/etc/scylla.d/perftune.yaml` only if the file does not exist.

Example 1 (16 CPUs, ScyllaDB on CPUs 3,4,5, IRQs handled on the same CPUs, other apps may benefit from XFS/RFS/RPS on `eth5`, as the page writes it, apparently a typo for XPS):

```
# cpuset.conf
CPUSET="--cpuset 3,4,5 "
# perftune.yaml
cpu_mask: '0xffff'
dir:
- /var/lib/scylla
irq_cpu_mask: '0x38'
nic:
- eth5
tune:
- net
- disks
```
Example 3 sends IRQs to other CPUs (6,7,8) while ScyllaDB stays on 3,4,5: same `CPUSET`, but `irq_cpu_mask: '0x1c0'`. Masks are bit positions of CPUs: CPUs 3,4,5 are `0x38`, CPUs 6,7,8 are `0x1c0`.

## Checked

2026-11-04. Confirmed against kb/system-limits.rst and kb/customizing-cpuset.rst: all five limit values and the limits.d file, cpuset.conf and perftune.yaml customisation, examples 1 and 3 with masks. Corrected the perftune.yaml sentence (it is generated only if absent) and removed the unsupported mixed-cluster advice. The page writes XFS/RFS/RPS, apparently a typo for XPS.

Method: documentation only; no commands were run.
