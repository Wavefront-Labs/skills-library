---
id: computing-software.messaging-and-integration.apache-zookeeper.reconfig-command-usage
name: reconfig-command-usage
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, reconfig, add-remove-servers, observer-to-participant, incremental, bulk]
level: advanced
status: docs-checked
description: "Run ZooKeeper reconfig: incremental -add/-remove, bulk -members or -file, conditional -v, role changes, removal behaviour and safe joiner startup."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reconfig usage

- Incremental: `reconfig -remove 3,4 -add server.5=...;...` (Majority quorum system only; otherwise BadArgumentsException).
- Bulk: `reconfig -members ...` or `reconfig -file newconfig.cfg` (Majority and Hierarchical); only bulk can change the quorum system.
- Conditional: add `-v <version>` so it applies only if the current version matches (else BadVersionException).
- CLI form: `reconfig [-s] [-v version] [-file path | -members ...] [-add ...]* [-remove ...]`.
- Removed servers are not shut down; they become non-voting followers, a temporary mode, so stop or re-add them.
- Observer to participant needs a connected, up-to-date majority of the new voters, else NewConfigNoQuorum; workaround: remove then re-add.
- Leader removal, change to observer or quorum-port change triggers a leader hand-off.
- Joiners: start with an initial list containing the current leader and the joiner; never list more than one joiner as participant (split-brain risk; multiple joiners as observers are fine).

Verify: `config` shows the new member list and the new version.

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Dynamic Reconfiguration guide (general, joiners, conditional, error conditions, additional comments) and the CLI guide (reconfig syntax).
