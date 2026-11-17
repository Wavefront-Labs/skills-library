---
id: computing-software.database-administration.vitess.reshard-workflow
name: reshard-workflow
category: computing-software
field: database-administration
product: vitess
tags: [reshard, resharding, vreplication, switchtraffic, split-shards, vdiff, new-shards]
level: practitioner
status: docs-checked
description: "Reshard a keyspace online: choose primary vindexes, apply a sharded VSchema, create target shards, run Reshard create, VDiff, switch replica/rdonly then primary traffic, complete."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/reshard/
  - https://vitess.io/docs/25.0/user-guides/configuration-advanced/resharding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Reshard` creates and manages workflows that horizontally shard an existing keyspace; the source can be unsharded or sharded. The lifecycle is `create --source-shards <shards> --target-shards <shards>`, `show`/`status`, VDiff, `switchtraffic`, then `complete` to clean up artifacts and source shards. Warning: workflows load source tablets, especially primaries; the `--vreplication-copy-phase-max-*` flags limit it.

Preparation (user guide example):
- Replace auto_increment with sequences in an unsharded keyspace.
- Pick the primary vindex from the highest-QPS WHERE clauses, high cardinality, join locality and transaction locality. In the example `customer_id` is the primary vindex for both customer and corder so joins stay in-shard. Use `xxhash` for BIGINT or VARBINARY and `unicode_loose_xxhash` for VARCHAR. Sharding by a tenant ID can unbalance shards.
- Apply the new VSchema with `vtctldclient ApplyVSchema --vschema-file <file> <keyspace>`, validating queries first; you can restore the old VSchema if queries fail.
- Create the new empty shards, then start.

Commands from the guide:

```
vtctldclient Reshard --target-keyspace customer --workflow cust2cust create --source-shards '0' --target-shards '-80,80-'
vtctldclient VDiff --target-keyspace customer --workflow cust2cust create
vtctldclient Reshard --target-keyspace customer --workflow cust2cust SwitchTraffic --tablet-types=rdonly,replica
vtctldclient Reshard --target-keyspace customer --workflow cust2cust SwitchTraffic
vtctldclient Reshard --target-keyspace customer --workflow cust2cust complete
```

Switching REPLICA and RDONLY reads first confirms the new shards' tablets are healthy. Omitting `--tablet-types` switches everything. After complete, remove the old shard (`vtctldclient DeleteShards --recursive customer/0`). The page notes you can always reshard again.

## Checked

2026-11-04. Lifecycle and warning on the Reshard reference page; preparation guidance, commands and cleanup on the Resharding user guide.

Method: documentation only; no commands were run.
