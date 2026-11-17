---
id: computing-software.messaging-and-integration.nats.jetstream-backup-restore
name: jetstream-backup-restore
category: computing-software
field: messaging-and-integration
product: nats
tags: [disaster-recovery, backup, restore, snapshot, account-backup, quorum]
level: practitioner
status: docs-checked
description: "Recover JetStream: automatic replacement of R3+ replicas, nats stream backup/restore, nats account backup/restore, and limits."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/nats_admin/jetstream_admin/disaster_recovery.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restore JetStream data after node loss, using automatic recovery where possible and snapshots otherwise.

Automatic recovery creates replacement replicas only if: the stream is R3 or higher; the surviving replicas still meet quorum floor(R/2)+1; there is an available node in the stream cluster; and the failed node(s) were removed from the Meta group (for example `nats server cluster peer-remove`). R1 streams live on one node, so backup is the only recovery path.

Manual recovery uses snapshots:
- `nats stream backup ORDERS '/data/js-backup/backup1'` snapshots stream config and state, durable consumer config and state, and all payload data including timestamps and headers. While it runs the stream config cannot change and retention does not evict data.
- `nats stream restore '/data/js-backup/backup1'` restores one stream to the same or a new server or cluster.
- `nats account backup /data/js-backup` and `nats account restore` handle every stream in the account at once. The docs prefer configuration management as the desired-state source, but these commands suit interactively configured servers.
- `--no-progress` replaces the progress bar with log lines.

Gotcha: memory-storage streams do not support snapshots; only file-based streams can be backed up.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
