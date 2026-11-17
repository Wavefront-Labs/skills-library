---
id: computing-software.cloud-infrastructure-engineering.netdata.alert-label-scoping
name: alert-label-scoping
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, host-labels, chart-labels, alert-scope]
level: advanced
status: docs-checked
description: "Scope Netdata alerts to hosts or charts with host labels and chart labels, including pattern matching, AND semantics and how to list chart labels."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/REFERENCE.md
  - https://raw.githubusercontent.com/netdata/netdata/master/src/health/overriding-stock-alerts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Define host labels in `netdata.conf`:

```
[host labels]
    installed = 20191211
    room = server
```

Use them in an alert file:

```
host labels: room = server
host labels: installed = 201*
chart labels: mount_point=!/mnt/disk1 *
chart labels: mount_point=/mnt/disk1 device=sda
```

Rules:
- Values accept simple patterns; space-separated items evaluate in order.
- Multiple chart labels are ANDed.
- A chart lacking the label does not match.
- Chart labels only match charts that exist (a `disk.space` chart exists only while its mount point is present).
- List chart labels at `http://localhost:19999/api/v1/charts?all`.

Use cases:
- Different thresholds per host: same alert name with `host labels` such as `environment=production` versus `environment=development`; they do not conflict because they match different hosts.
- Several instances without listing chart IDs: a template with a shared chart label.

If your override has `host labels: production` but the stock alert has no host label scope, the stock alert still creates alerts on the hosts your override does not match. Match at least the stock scope.

Apply: `sudo netdatacli reload-health` (host labels in `netdata.conf` are reloaded with `netdatacli reload-labels`).

## Checked

2026-11-04: host and chart label syntax, simple-pattern and AND behaviour, the chart-must-exist note, the charts API URL, per-environment overrides and `reload-labels` confirmed against the Netdata health REFERENCE, overriding-stock-alerts and start-stop-restart pages. Reworded the host-label gotcha to match the page.

Method: documentation only; no commands were run.
