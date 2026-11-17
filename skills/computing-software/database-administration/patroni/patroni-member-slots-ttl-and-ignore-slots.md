---
id: computing-software.database-administration.patroni.patroni-member-slots-ttl-and-ignore-slots
name: patroni-member-slots-ttl-and-ignore-slots
category: computing-software
field: database-administration
product: patroni
tags: [patroni, replication-slots, member-slots-ttl, ignore-slots, wal-retention]
level: advanced
status: docs-checked
description: "Keep replica slots through downtime with member_slots_ttl or member-named permanent slots, and exclude foreign slots."
sources:
  - https://patroni.readthedocs.io/en/latest/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop slot drops from forcing replica rebuilds.

Problem: with `use_slots` on, when a member goes offline its slot on the upstream is dropped once the member key expires from the DCS.

Options:
1. `member_slots_ttl`: default 30 minutes (available from Patroni 4.0.0, PostgreSQL 11+). Slots for absent members are kept while downtime is shorter than the value. Set 0 for the old behaviour, immediate removal.
2. Permanent physical slots named like members, for a static topology:

```
slots:
  node_name1:
    type: physical
  node_name2:
    type: physical
```

Since Patroni 3.2.0 these are created on all nodes and advanced there. When removing a member, you must remove its slot entry or Patroni keeps it forever. Before 3.2.0 they were managed only on the current leader. A small race remains where a fresh replica slot is ahead of the leader's; configure continuous archiving so required WAL can be restored or PITR performed.

Names matching a Patroni member are not removed even if the member is unresponsive; avoid leaving such entries in DCS after they stop being needed.

`ignore_slots` (an array, unlike the `slots` hashmap) lists slot property sets Patroni ignores because they are managed outside it:

```
ignore_slots:
  - name: ignored_logical_slot_name
    type: logical
    database: my_db
    plugin: test_decoding
```

Any matching subset of properties causes the slot to be ignored. Release 4.1.4 drops Patroni-managed slots with `wal_status=lost`.

## Checked

2026-11-03. Confirmed against Dynamic Configuration (member_slots_ttl default 30min and PostgreSQL 11 requirement, permanent slots, ignore_slots) and the FAQ; 3.2.0 and 4.1.4 notes against the release notes.

Method: documentation only; no commands were run.
