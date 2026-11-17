---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.replication-placement-string
name: replication-placement-string
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [000, 001, durability, replication, placement, xyz]
level: practitioner
status: docs-checked
description: "Read and set the 3-digit SeaweedFS replication string (data center, rack, server copies); defaults at master/filer, no auto-repair, and costs."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Replication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# replication placement string

The string is `XYZ`: extra copies on other data centers (X), other racks in the same DC (Y), other servers in the same rack (Z). Total copies = 1 + X + Y + Z.

Examples: `000` one copy; `001` one extra copy on the same rack; `010` one on a different rack; `100` one in another data center; `200` two other data centers; `110` one other rack plus one other data center.

Set a default on the master (`weed master -defaultReplication=001`) or the filer; it is propagated to volumes. The page also shows `weed volume` setting replication directly (less useful), `weed mount -replication` overriding filer and master, and the `dataCenter` parameter on `/dir/assign` to restrict the data center.

Gotchas:
- Replication is per volume. Writes complete only once all replicas confirm (W = N, R = 1); if one replica fails the whole write fails.
- SeaweedFS does not rebalance or auto-repair a missing replica in normal operation (to avoid over-replication from transient failures). The volume becomes read-only and new writes go to another volume; repair with `volume.fix.replication` in `weed shell`, typically scripted periodically. `-doDelete=false` repairs without deleting.
- Changing a volume's setting with `volume.configure.replication` makes it read-only until `volume.fix.replication` creates the missing replicas.
- Data stays readable while at least one replica is accessible, but writes are permitted only if the replica count is achievable. The maximum string value is 255.
- High factors multiply disk use (205 means 8 copies); erasure coding gives resilience at lower storage cost.

## Checked

2026-11-08. Confirmed against the Replication wiki page. Removed the unsupported `/dir/assign?replication=` and `fs.configure -replication` overrides and the "same host counts as separate servers" note (that is on the Production Setup page, not this one); added quorum, repair and change-replication details.

Method: documentation only; no commands were run.
