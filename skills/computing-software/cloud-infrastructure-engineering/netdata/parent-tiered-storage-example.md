---
id: computing-software.cloud-infrastructure-engineering.netdata.parent-tiered-storage-example
name: parent-tiered-storage-example
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, tiered-storage, backfill, page-cache]
level: advanced
status: docs-checked
description: "Reference tiered-storage Parent for 10 Children of about 2k metrics each: three tiers with time and size limits, backfill and page cache settings."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/deployment-guides/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs size this Parent for 10 Children with about 2k metrics each:

| Tier | Resolution | Time | Size |
|---|---|---|---|
| 0 | 1 s | 7 days | 12GiB |
| 1 | 1 minute (`update every iterations = 60`) | 1 month | 4GiB |
| 2 | 1 hour (`update every iterations = 60`) | 1 year | 2GiB |

Settings in `[db]`:

```
db = dbengine
dbengine tier backfill = new
storage tiers = 3
dbengine page cache size = 1.4GiB
```

Each tier is limited by both time and size; whichever hits first applies. Expected resources: about 25GB disk, 3.5GB RAM typical, 2.5GB under memory pressure.

Accept Children in `stream.conf` with a `[API_KEY]` section containing `enabled = yes` (key from `uuidgen`).

Edit `netdata.conf` and `stream.conf` on the Parent with the `edit-config` script.

Gotcha: the example numbers are for that workload only; for your size use the sizing and retention-planning skills.

## Checked

2026-11-04. Confirmed against the Netdata Deployment Strategies page, Parent with Tiered Storage section: 10 Children of about 2k metrics, the three resolutions and periods, 25GB disk, 3.5GB typical and 2.5GB under pressure RAM, the [db] settings, tier sizes, update every iterations = 60, and the stream.conf API key with enabled = yes. Removed the invented restart-then-check-resources step and the sudo ./edit-config form.

Method: documentation only; no commands were run.
