---
id: computing-software.cloud-infrastructure-engineering.cortex.scale-ingesters-up-and-down
name: scale-ingesters-up-and-down
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [ingester, scaling, readonly-mode, shutdown-endpoint, query-store-after]
level: advanced
status: docs-checked
description: "Scale Cortex ingesters safely, including the gap risk when scaling up, the shutdown endpoint, and the READONLY mode added in 1.19.0."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/ingesters-scaling-up-and-down.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scaling up is safe: a new ingester registers in the ring and distributors reshard. Ingesters that used to receive the moved series see them go idle. With `-distributor.shard-by-all-labels=false` (the default), wait before adding a second ingester until idle series have been flushed to the back-end store, or queries show gaps. That happens after the next head compaction, typically every 2 hours; if you set `-querier.query-store-after` it is also a minimum wait. With `-distributor.shard-by-all-labels=true` no special care is needed.

Scaling down must not discard in-memory data. Ingesters do not flush at shutdown by default, but the `/shutdown` endpoint flushes series to blocks and uploads them first. Even then, queriers and store-gateways take time to discover new blocks because they scan the bucket periodically, so do not remove several ingesters in quick succession.

Recommended since Cortex 1.19.0: the READONLY state. A READONLY ingester rejects pushes (redistributed to others) but keeps serving queries. Set it per ingester with `POST /ingester/mode` using `mode=READONLY`, optionally watch `/ingester/all_user_stats`, then remove it. It is safe once queries no longer need its data: after `querier.query-ingesters-within` (for example 5h) at the earliest, or after the full retention period for complete ageing out.

Older versions need the legacy approach: `-querier.query-store-after=0s`, 5m bucket sync and cleanup intervals, and 1m metadata cache TTLs.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Ingesters scaling up and down (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
