---
id: computing-software.database-administration.scylladb.kb-snapshot-disk-utilization
name: kb-snapshot-disk-utilization
category: computing-software
field: database-administration
product: scylladb
tags: [snapshot, disk-space, listsnapshots, hardlinks, compaction]
level: practitioner
status: docs-checked
description: "How ScyllaDB snapshot disk usage grows: hard links, True size vs Size on disk in nodetool listsnapshots, effect of background and major compaction."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/disk-utilization.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Snapshots and disk utilization

`nodetool snapshot` does not copy SSTables; it hard-links them into the snapshot directory. Consequences:
- Snapshot space starts at zero and grows to equal the data set size at the time the snapshot was taken.
- Background compactions delete replaced SSTables as usual, but any SSTable that is also linked from a snapshot is kept, so the disk space is retained.
- A major compaction makes the true snapshot size jump to the data size immediately, as the old SSTables are being deleted.

See it with `nodetool listsnapshots`:

```
Snapshot name  Keyspace name  Column family name  True size  Size on disk
1574708464997  ks3            standard1           0 bytes    2.23 GiB
Total TrueDiskSpaceUsed: 0 bytes
```
After `nodetool compact ks3` the same snapshot shows True size 2.23 GiB. `Size on disk` is the total size of the snapshot; `True size` is zero for an SSTable that also still exists in the table directory (per the `listsnapshots` page, a 1TB file present in both places shows 1TB on disk and 0 true size).

Clear old snapshots with `nodetool clearsnapshot` once the data is copied off the node.

## Checked

2026-11-04. Confirmed against kb/disk-utilization.rst and listsnapshots.rst: hard links, zero-growing true size, background compaction behaviour, example output, major compaction note. Removed the operational-implications claims (days later, one extra copy) the page does not state.

Method: documentation only; no commands were run.
