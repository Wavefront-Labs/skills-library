---
id: computing-software.messaging-and-integration.redpanda.rolling-restart-with-maintenance-mode
name: rolling-restart-with-maintenance-mode
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rolling-restart, maintenance-mode, rpk-cluster-maintenance, pre-restart-probe, health, metrics]
level: practitioner
status: docs-checked
description: "Restart Redpanda brokers one at a time: check health, run the pre_restart_probe, enable maintenance mode with --wait, watch listed metrics, restart, then disable maintenance mode."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/rolling-restart/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Maintenance mode makes a broker drain partition leadership to other brokers for topics with replication factor above one. Topics with `replication.factor=1` become unavailable during the restart, so if disk allows, raise their factor beforehand and let data replicate.

**Per broker**
1. Confirm membership: `rpk cluster info -b --detailed` should show MEMBERSHIP `active` and IS-ALIVE `true` everywhere.
2. `rpk cluster health` must be healthy.
3. Optional risk check on the Admin API (port 9644): `curl -X GET "http://<broker-address>:<admin-api-port>/v1/broker/pre_restart_probe"` returns `risks` such as `rf1_offline`, `full_acks_produce_unavailable`, `unavailable` and `acks1_data_loss`.
4. `rpk cluster maintenance enable <node-id> --wait` waits for draining. Verify with `rpk cluster maintenance status`: `FINISHED` should be true for that node.
5. `rpk cluster health --watch --exit-when-healthy` blocks until healthy. If there are problems, run `rpk cluster maintenance disable <node-id>` before retrying.
6. Check metrics before continuing: `redpanda_kafka_under_replicated_replicas` (pause if non-zero), `redpanda_cluster_unavailable_partitions` (must be zero), and recovery of produce and consume rates (`redpanda_rpc_received_bytes`, `redpanda_rpc_sent_bytes`) and p99 of `redpanda_kafka_request_latency_seconds` and `redpanda_rpc_request_latency_seconds`.
7. `sudo systemctl restart redpanda`
8. `rpk cluster maintenance disable <node-id>`, then confirm with status.
9. `rpk cluster health`; `post_restart_probe` reports `load_reclaimed_pc`.

**Expected impact:** client latency (clients get `NOT_LEADER_FOR_PARTITION` and refresh metadata), CPU spikes while replicas rebalance, and under-replicated partition alerts until replicas catch up.

## Checked

2026-11-04. The steps, commands, probe responses, metric guidance and impact notes were confirmed on the Rolling Restart page.

Method: documentation only; no commands were run.
