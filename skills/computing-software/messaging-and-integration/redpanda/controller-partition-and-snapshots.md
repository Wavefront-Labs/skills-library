---
id: computing-software.messaging-and-integration.redpanda.controller-partition-and-snapshots
name: controller-partition-and-snapshots
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [controller, snapshots, metadata, raft, startup]
level: advanced
status: docs-checked
description: "What the controller partition stores, how controller snapshots speed broker startup, and where each broker keeps its snapshot file in the controller log directory."
sources:
  - https://docs.redpanda.com/streaming/current/get-started/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Redpanda stores cluster metadata update commands, such as creating or deleting topics or users, in a system partition called the controller partition. It is replicated by one Raft group that includes every broker in the cluster.

**Snapshots.** A new snapshot is created after each controller command is added or, when updates arrive rapidly, after a set period of time (default 60 seconds). A snapshot saves the current metadata state to disk so startup is fast: for a partition that has moved several times, the snapshot restores the latest state without replaying every move command. The controller snapshot is the Raft snapshot for the controller group.

**Where it lives.** Each broker has its own snapshot file in the controller log directory. The page gives this example location:

```text
/var/lib/redpanda/data/redpanda/controller/0_0/snapshot
```

**When it is used.** Snapshots are hydrated when a broker joins the cluster or restarts. They are enabled by default for all clusters, both new and upgraded, so there is nothing to switch on after an upgrade.

## Checked

Controller partition contents, snapshot cadence, location example, default-on behavior and hydration were confirmed in the Controller partition and snapshots section of the How Redpanda Works page. Unconfirmed operator remarks were removed.

Method: docs-checked 2026-11-09 against the How Redpanda Works page, read in full; no commands were run.
