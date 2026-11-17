---
id: computing-software.cloud-infrastructure-engineering.netdata.lightweight-child-config
name: lightweight-child-config
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, ram-mode, lightweight-child, iot]
level: practitioner
status: docs-checked
description: "Configure a lightweight Netdata Child that keeps metrics in RAM, runs no ML or alerts, binds to localhost and streams everything to a Parent."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/deployment-guides/deployment-strategies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `netdata.conf` (open it with `edit-config`):

```
[db]
    db = ram
    retention = 1200
    update every = 1
[ml]
    enabled = no
[health]
    enabled = no
[web]
    bind to = localhost
```

- `db = ram` keeps metrics in RAM; metadata and logs can still write to disk.
- `retention = 1200` rounds to 2048 entries on 4 KiB-page devices (about 34 minutes at 1 s). Retained time depends on each chart's interval.
- Raise `update every` to lower CPU use.
- The Parent handles ML and alerting.
- Optionally uncomment `enable running new plugins = no` for extreme IoT cases.

In `stream.conf`:

```
[stream]
    enabled = yes
    destination = PARENT:19999
    api key = <uuidgen output>
```

Gotchas:
- The docs do not recommend connecting Children to Cloud directly.
- Lowering retention or changing cadence changes retained time; review the fleet guide first.

## Checked

2026-11-04. Confirmed against the Netdata Configuration Examples page, Lightweight Child Configuration: the netdata.conf and stream.conf settings, RAM mode behaviour, the 1200 to 2048 entries and about 34 minutes figure, the ML and health notes, the optional enable running new plugins line, and the no-direct-Cloud recommendation. Removed the closing restart-and-confirm step and the claim-the-Parent advice, which the page does not state.

Method: documentation only; no commands were run.
