---
id: computing-software.messaging-and-integration.redpanda.bootstrap-brokers-seed-servers-and-listeners
name: bootstrap-brokers-seed-servers-and-listeners
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [bootstrap, seed-servers, rpk, listeners, redpanda-yaml, empty-seed-starts-cluster, node-id]
level: practitioner
status: docs-checked
description: "Bootstrap Redpanda brokers with rpk redpanda config bootstrap, set seed servers identically with empty_seed_starts_cluster false, and never set node_id by hand."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/production/production-deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bootstrapping sets listeners, seed servers and advertised listeners:

```bash
sudo rpk redpanda config bootstrap --self <listener-address> --advertised-kafka <advertised-kafka-address> --ips <seed-server1-ip>,<seed-server2-ip>,<seed-server3-ip> && \
sudo rpk redpanda config set redpanda.empty_seed_starts_cluster false
```

- `--self`: interfaces to bind for the Kafka, RPC and Admin APIs. `0.0.0.0` binds all interfaces; a specific IP restricts to that interface.
- `--advertised-kafka`: a different advertised Kafka address when the reachable address differs from the bind address. Advertised addresses must not be `0.0.0.0`, or startup validation errors occur.
- `--ips`: all seed servers including this one, set identically and in the same order on every node.

The command edits `/etc/redpanda/redpanda.yaml`: `seed_servers` (port 33145), `rpc_server`, `kafka_api` (9092), `admin` (9644), `advertised_rpc_api` and `advertised_kafka_api`.

**Seed server rules**
- Use at least three; put one or more in each fault domain (rack or AZ).
- With `empty_seed_starts_cluster: false` (recommended since 22.3), a seed server waits for all other seed servers, then forms the cluster; a non-seed broker asks the seed servers to join.
- The default `true` is for backward compatibility: a broker with an empty `seed_servers` list creates a one-broker cluster, so never have more than one such broker.
- You can add a seed server later by editing `seed_servers` and restarting broker by broker.
- Keep at least one seed server available so brokers can discover the cluster.

**Do not set `node_id`.** Redpanda assigns unique IDs automatically; setting or reusing them, even for decommissioned brokers, can cause inconsistencies.

Start with `sudo systemctl start redpanda-tuner redpanda`, then verify with `rpk cluster info`.

## Checked

The bootstrap command, flags, resulting YAML keys, seed server guidance, start command and node_id warning were confirmed on the Deploy for Production: Manual page.

Method: docs-checked 2026-11-09 against the Deploy for Production: Manual page, read in full; no commands were run.
