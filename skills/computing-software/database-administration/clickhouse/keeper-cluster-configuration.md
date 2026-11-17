---
id: computing-software.database-administration.clickhouse.keeper-cluster-configuration
name: keeper-cluster-configuration
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, keeper, raft, server-id, coordination, four-letter-words]
level: practitioner
status: docs-checked
description: "Configure a 3-node ClickHouse Keeper ensemble with raft_configuration, storage paths and 4lw health checks."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/sre/keeper/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# keeper cluster configuration
ClickHouse Keeper replaces ZooKeeper for replication coordination. Each node gets a `keeper_server` block:
```xml
<keeper_server>
  <tcp_port>9181</tcp_port>
  <server_id>1</server_id>
  <log_storage_path>/var/lib/clickhouse/coordination/log</log_storage_path>
  <snapshot_storage_path>/var/lib/clickhouse/coordination/snapshots</snapshot_storage_path>
  <coordination_settings>
    <operation_timeout_ms>10000</operation_timeout_ms>
    <session_timeout_ms>30000</session_timeout_ms>
    <raft_logs_level>warning</raft_logs_level>
  </coordination_settings>
  <raft_configuration>
    <server><id>1</id><hostname>keeper1</hostname><port>9234</port></server>
    <server><id>2</id><hostname>keeper2</hostname><port>9234</port></server>
    <server><id>3</id><hostname>keeper3</hostname><port>9234</port></server>
  </raft_configuration>
</keeper_server>
```
Keeper is bundled in the ClickHouse server package; to run it standalone use `clickhouse-keeper --config <file>` (or `clickhouse keeper --config ...`). The `tcp_port` default is 2181 in the parameter table and the example config uses 9181. Set `server_id` per node (1, 2, 3) in the same `keeper_server` block.

Verify with four-letter words, for example `echo mntr | nc localhost 9181` (`zk_server_state` shows leader or follower). Allowed commands are governed by `four_letter_word_white_list`.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "ClickHouse Keeper": the `keeper_server` block, coordination settings (operation_timeout_ms, session_timeout_ms, raft_logs_level), raft_configuration, standalone start commands, port 9181 in the example and 2181 as the table default, 4lw usage. Removed: the odd-node-count advice, the server_id corruption claim and the `secure` TLS advice, which the page does not state in that form.
Method: documentation only; no commands were run.
