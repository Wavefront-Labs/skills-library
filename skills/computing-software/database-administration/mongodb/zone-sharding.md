---
id: computing-software.database-administration.mongodb.zone-sharding
name: zone-sharding
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, zone-ranges, zone-sharding, mongodb-sharding, data-locality]
level: practitioner
status: docs-checked
description: "Pin ranges of MongoDB sharded data to specific shards with zones (geo locality, tiered storage, tenant isolation), including shard key prefix rules and balancer behaviour."
sources:
  - https://www.mongodb.com/docs/manual/core/zone-sharding/
  - https://www.mongodb.com/docs/manual/tutorial/manage-shard-zone/
  - https://www.mongodb.com/docs/manual/reference/method/sh.updateZoneKeyRange/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zone sharding

**Goal:** keep EU customers' data on EU shards, put recent data on fast hardware, or isolate a large tenant.

## Requirements
The zone range is defined on the shard key (or its prefix). Shard key `{ region: 1, customerId: 1 }` allows zones on `region`.

## Configure
```javascript
sh.addShardToZone("shard-eu-1", "EU")
sh.addShardToZone("shard-eu-2", "EU")
sh.addShardToZone("shard-us-1", "US")
sh.updateZoneKeyRange("crm.customers",
  { region: "EU", customerId: MinKey }, { region: "EU", customerId: MaxKey }, "EU")
sh.updateZoneKeyRange("crm.customers",
  { region: "US", customerId: MinKey }, { region: "US", customerId: MaxKey }, "US")
```
Each zone range is inclusive of its lower boundary and exclusive of its upper boundary; ranges cannot overlap. Use `MinKey`/`MaxKey` for the suffix fields to cover the whole region. With a compound shard key, the range must include the shard key prefix.

## What happens
The balancer migrates chunks to the shards of the matching zone in the background. Move a range boundary with `sh.removeRangeFromZone` and `sh.updateZoneKeyRange`.

## Gotchas
- Zones constrain, they do not shard: a zone with one shard means all of that range sits on one shard.
- Remove a zone from a shard with `sh.removeShardFromZone()`.
- For an empty collection with a hashed shard key, `sh.shardCollection()` with `presplitHashedZones: true` creates the initial chunks according to the zones.

## Verify
```javascript
sh.status()                          // shows zones per range
db.getSiblingDB("config").tags.find({ ns: "crm.customers" })
```

## Checked

2026-10-28. Confirmed against MongoDB manual zone sharding, Manage Shard Zones and sh.updateZoneKeyRange pages: ranges inclusive of lower boundary and exclusive of upper, no overlapping ranges, compound shard key ranges must include the prefix, MinKey/MaxKey bounds, sh.removeRangeFromZone, sh.removeShardFromZone, presplitHashedZones, config.tags. Removed unconfirmed: balancing window remark, immediate routing claim, tiered NVMe storage pattern, balancer warning on orphaned zone, getShardDistribution.

Method: documentation only; no commands were run.
