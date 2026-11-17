---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimir-hash-ring-and-memberlist
name: mimir-hash-ring-and-memberlist
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [hash-ring, mimir, memberlist, ingester-ring, kvstore, ring-status, unhealthy-instances]
level: practitioner
status: docs-checked
description: "Configure and troubleshoot Mimir hash rings: memberlist KV store, cluster label verification, ring status pages and forgetting unhealthy instances."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-hash-rings/", "https://grafana.com/docs/mimir/latest/references/http-api/", "https://grafana.com/docs/mimir/latest/configure/configure-zone-aware-replication/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: healthy rings so writes and reads route correctly.

Each component builds its own ring, configured with a flag prefix: ingesters `-ingester.ring.*`, distributors `-distributor.ring.*`, compactors `-compactor.ring.*`, store-gateways `-store-gateway.sharding-ring.*`, and optionally query-schedulers, rulers, alertmanagers (`-alertmanager.sharding-ring.*`) and overrides-exporters. KV store per ring: `<prefix>.store` with `memberlist` (default), `consul`, `etcd` or `multi` (only for migrating between backends).

Memberlist is configured globally, not per component. Instances join via `-memberlist.join` (`<ip>:<port>`, `<hostname>:<port>` or DNS service discovery format; default port `7946`). On Kubernetes use a headless Service and `dnssrv+<service name>.<namespace>.svc.cluster.local:<port>`.
```yaml
memberlist:
  join_members:
    - dnssrv+mimir-gossip-ring.mimir.svc.cluster.local:7946
ingester:
  ring:
    kvstore:
      store: memberlist
```
Bind/advertise: `-memberlist.bind-addr`, `-memberlist.bind-port`, `-memberlist.advertise-addr`, `-memberlist.advertise-port`.

Cluster label verification stops two Mimir clusters (or other memberlist users) found by DNS from merging. Set a unique `-memberlist.cluster-label` on every instance of a cluster. To migrate a live cluster: set `-memberlist.cluster-label-verification-disabled=true` everywhere and wait for rollout; set the label and wait; remove the disabled flag and wait.

Zone awareness: set `-ingester.ring.instance-availability-zone` per replica and `-ingester.ring.zone-awareness-enabled=true` (distributors, ingesters, queriers). `-ingester.ring.replication-factor` is not used in the ingest storage architecture.

Ring status pages (GET): `/ingester/ring`, `/distributor/ring`, `/store-gateway/ring`, `/compactor/ring`, `/ruler/ring`, `/query-scheduler/ring`, `/multitenant_alertmanager/ring`, `/overrides-exporter/ring`. They show state, health and last heartbeat of each instance. The runbooks say to use the **Forget** button on an `Unhealthy` entry, but forgetting an instance that is still running or owns data can lose data.

Gotchas
- An instance missing heartbeats for the configured period is unhealthy.
- With replication factor 3 a write needs a quorum of at least 2 ingesters.
- Slow propagation of ring changes: measure with `max(time() - (cortex_ring_oldest_member_timestamp{state="ACTIVE"} > 0))`; it should stay under the `<prefix>.heartbeat-period` plus a small delta (the docs suggest 15 s). Tune `-memberlist.gossip-interval` (down), `-memberlist.gossip-nodes` and `-memberlist.retransmit-factor` (up).

## Verify
The ring pages show every instance `ACTIVE` with a recent heartbeat.

## Checked
2026-11-03. Confirmed against the Mimir hash ring configuration page, HTTP API reference (ring status endpoints), zone-aware replication page, hash ring architecture page and the runbooks (Forget button and data-loss caution). Removed: the `curl -X POST ... forget=` command, the "TCP and UDP" port claim, `cortex_ring_members` metric, the "at least 2 live replicas required" error text, the JOINING/LEAVING state list for classic rings and the claim that changing the replication factor needs a planned rollout.
Method: documentation only; no commands were run.
