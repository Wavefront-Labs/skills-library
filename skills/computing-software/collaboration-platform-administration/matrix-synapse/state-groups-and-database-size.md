---
id: computing-software.collaboration-platform-administration.matrix-synapse.state-groups-and-database-size
name: state-groups-and-database-size
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, state-groups, state-groups-state, synapse-compress-state, database-size, maintenance, postgresql]
level: sme
status: docs-checked
description: "Why state_groups_state grows: how Synapse stores room state as state groups and deltas, the known bug that creates extra groups, and synapse-compress-state and other tools."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/state_groups.html
  - https://element-hq.github.io/synapse/latest/usage/administration/database_maintenance_tools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse must be able to work out a room's state at any event in its history quickly. It does so with state groups.

A run of events sharing the same state is grouped into a `state_group`, and the mapping is recorded in `event_to_state_groups`. The `state_groups` table records, per group, the room ID and the first event in that group. Storing the full state for every group would be huge, so for most groups Synapse stores only the difference from a previous group. The `state_group_edges` table links a group to its predecessor, and `state_groups_state` holds the differences in state since that predecessor. Only occasionally is a group a full one, which records the event ID for every piece of state in the room at that point.

The page explains why `state_groups_state` gets so big. The docs also note known bugs that can make Synapse create many more state groups than necessary; they point to issue 3364 in the Synapse repository for the details.

**Compression tool.** `rust-synapse-compress-state` (an external tool from the matrix-org organisation) compresses `state_groups_state` on a room-by-room basis. It essentially reduces the number of full state groups and can shrink the table dramatically. The docs link two community blog posts on using it.

Other maintenance tools the docs list for database size:

- the purge remote media API, for cached remote media;
- the delete local media API, for local media on disk;
- the purge history API, which deletes historic events;
- `synapse-compress-state`, which deduplicates `state_groups_state`;
- a page of useful SQL for analysing Postgres stats.

The Admin FAQ shows a query for the biggest rooms, and the List Room API can be ordered by `state_events`.

## Checked

2026-11-04. Confirmed against the Synapse State Groups page and the database maintenance tools page: tables, delta storage, known-bugs issue, compression tool, tool list. Removed an unsourced order-of-attack paragraph and VACUUM FULL advice.
Method: documentation only; no commands were run.
