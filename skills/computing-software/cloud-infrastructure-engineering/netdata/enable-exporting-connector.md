---
id: computing-software.cloud-infrastructure-engineering.netdata.enable-exporting-connector
name: enable-exporting-connector
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, exporting-conf, graphite, opentsdb]
level: practitioner
status: docs-checked
description: "Export Netdata metrics to external databases by enabling the exporting engine in exporting.conf and adding one connector section per destination."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/exporting-metrics/enable-an-exporting-connector.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
cd /etc/netdata 2>/dev/null || cd /opt/netdata/etc/netdata
sudo ./edit-config exporting.conf
```

Enable the engine:

```
[exporting:global]
    enabled = yes
```

Add a section per destination; the header is connector type plus an instance name you choose:

```
[graphite:my_graphite_instance]
    enabled = yes
    destination = localhost:2003

[opentsdb:http:my_opentsdb_http_instance]
    enabled = yes
    destination = localhost:4242
```

Replace instance names and `destination` (database IP or hostname) with your own. Restart the Agent; data should appear in the database within seconds.

Notes:
- Types can be mixed. Each section with `enabled = yes` exports independently, and by default all get the same metrics. Each section can override `destination`, export interval and metric filters.
- Gotcha: no historical backfill; exporting starts from the Agent restart time.
- Gotcha: changes apply only after a restart.
- Further per-connector options are in the connector docs and exporting engine reference.

## Checked

2026-11-04: edit-config usage, the `[exporting:global]` setting, the Graphite and OpenTSDB section examples, instance naming, restart, data appearing within seconds, export from restart time only, independent sections and per-section overrides confirmed against the Netdata Enable an Exporting Connector page.

Method: documentation only; no commands were run.
