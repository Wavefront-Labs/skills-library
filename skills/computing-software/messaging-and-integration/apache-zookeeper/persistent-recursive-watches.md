---
id: computing-software.messaging-and-integration.apache-zookeeper.persistent-recursive-watches
name: persistent-recursive-watches
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, persistent-watches, recursive-watches, addwatch, removewatches]
level: advanced
status: docs-checked
description: "Persistent and recursive watches added in 3.6.0: addWatch, events they fire, no child-changed events, and removal with removeWatches and WatcherType.Any."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persistent recursive watches (3.6.0)

- New in 3.6.0: a watch that is not removed when triggered. Set with `addWatch()`.
- They trigger NodeCreated, NodeDeleted and NodeDataChanged and, optionally, recursively for all znodes starting at the znode the watch is registered on.
- NodeChildrenChanged is never triggered for persistent recursive watches, as it would be redundant.
- Triggering semantics and guarantees, other than one-time triggering, are the same as standard watches.
- Remove with `removeWatches()` using watcher type `WatcherType.Any`. A removal triggers a Persistent Remove event for watchers added as persistent watches.
- Standard watches stay one-time, so re-arming them can miss changes between event and re-registration; persistent watches avoid the re-arm step.
- The zkCli reference documents no addWatch command.

## Checked
Confirmed against the Programmers Guide watches sections and the zkCli reference, 2026-11-08. Removed: the zkCli removewatches flag meanings and the verification line, which the pages do not give.
Method: docs-only read of cited pages, 2026-11-08
