---
id: computing-software.cloud-infrastructure-engineering.cortex.migrate-kv-store-to-memberlist
name: migrate-kv-store-to-memberlist
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [memberlist, consul, migration, multi-kv, mirror]
level: advanced
status: docs-checked
description: "Live-migrate the Cortex ring from Consul or Etcd to memberlist using the multi KV store with mirroring."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/migration-kv-store-to-memberlist.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The multi KV store allows a live migration. Phase one: keep the existing store (for example Consul) as primary and add memberlist as secondary, with mirroring so everything written to the primary is replicated into the secondary:

```yaml
ring:
  store: memberlist
memberlist:
  abort_if_cluster_join_fails: false
  bind_port: <gossip-ring-port>
  join_members:
    - gossip-ring.<namespace>.svc.cluster.local:<gossip-ring-port>
ingester:
  lifecycler:
    join_after: 60s
    heartbeat_period: 5s
    ring:
      kvstore:
        store: multi
        multi:
          mirror_enabled: true
          primary: consul
          secondary: memberlist
        consul:
          host: <consul-host>:<consul-port>
```

Apply the same multi KV config to every component that uses the ring (distributors, store-gateways and so on), not just ingesters. `join_after: 60s` gives gossip time to sync the existing ring before the ingester joins.

Verify mirroring with metrics: `cortex_multikv_mirror_enabled` should be 1, `rate(cortex_multikv_mirror_writes_total[5m])` should be stable, and `cortex_multikv_mirror_write_errors_total` should not increase.

Phase two, once stable: set `kvstore.store: memberlist` (dropping the multi block) on every component, deploy, and then remove Consul.

If several Cortex, Mimir or Loki clusters can reach the same gossip seeds, set a shared `memberlist.cluster_label`: deploy with `cluster_label_verification_disabled: true`, then set it to false once every process has the label. This isolates memberlist traffic only, not Consul or Etcd prefixes.

Use `multi` only for migration, as the HA tracker docs also say.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Migration KV Store to Memberlist (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
