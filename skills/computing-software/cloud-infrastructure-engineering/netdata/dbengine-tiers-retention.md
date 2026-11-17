---
id: computing-software.cloud-infrastructure-engineering.netdata.dbengine-tiers-retention
name: dbengine-tiers-retention
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, dbengine, retention, db-tiers]
level: practitioner
status: docs-checked
description: "Understand default dbengine tiers, per-tier size and time limits, disk footprint and how retention is shared on a Parent; ram mode for Children."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/sizing-netdata-agents/disk-requirements-and-retention.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Modes: `dbengine` (default; multi-tier compressed on disk) and `ram` (in memory only; suits Children streaming to a Parent).

Defaults, 3 tiers (up to 5 allowed):

| Tier | Resolution | Size limit | Time limit |
|---|---|---|---|
| tier0 | per-second | 1 GiB | 14 days |
| tier1 | per-minute | 1 GiB | 3 months |
| tier2 | per-hour | 1 GiB | 2 years |

Data is deleted when the size or time limit is reached, whichever is first. The size limit is soft. Expect about 4 GiB total with SQLite databases, alert transitions and metadata. Typical on-disk bytes per sample: tier0 0.6, tier1 6, tier2 18.

Set explicitly in `netdata.conf`:

```
[db]
    db = dbengine
```

Parents: retention is enforced per tier across all metrics; Children share the quota, no per-Child limit. Size for total cardinality plus `.ndf`, `.njf`, `.njfv2` overhead. Child and Parent storage are independent.

ram mode: `[db] db = ram`, 4 bytes per sample, history lost on restart; set `[db] retention` to samples per dimension.

Gotchas: changing `[db] update every` shifts tier resolution. Churning short-lived instances can grow `netdata-meta.db` past defaults.

## Checked

2026-11-04. Confirmed against the Netdata Disk Requirements and Retention page: the two modes, up to five tiers, default tier table and limits, soft size limit, about 4 GiB footprint, bytes per sample, per-tier Parent enforcement, the .ndf/.njf/.njfv2 overhead, ram mode at 4 bytes per sample, the `[db].retention` setting, the update every note and the netdata-meta.db growth note. Nothing removed.

Method: documentation only; no commands were run.
