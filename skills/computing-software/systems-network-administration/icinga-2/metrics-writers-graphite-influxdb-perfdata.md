---
id: computing-software.systems-network-administration.icinga-2.metrics-writers-graphite-influxdb-perfdata
name: metrics-writers-graphite-influxdb-perfdata
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, metrics, graphite, influxdb, perfdata-writer, enable-ha, time-series]
level: practitioner
status: docs-checked
description: Send Icinga 2 performance data to Graphite, InfluxDB v1 or v2, or perfdata spool files, including naming schema, default ports and enable_ha for clustered zones.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/14-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics writers
Writers parse performance data from executed or API-submitted check results and forward it to a time series backend. Documented writers: OpenTelemetry (OTLPMetrics), Graphite, InfluxDB, OpenTSDB, plus Elastic Stack and Graylog integrations.

**Graphite:** `icinga2 feature enable graphite`. Writes to Carbon Cache, default `127.0.0.1` port `2003`. Default prefixes use macros: `icinga2.$host.name$.host.$host.check_command$` and `icinga2.$host.name$.services.$service.name$.$service.check_command$`; change with `host_name_template` and `service_name_template`. Whitespace, `.`, `\` and `/` in prefix labels become `_`. Values go to `<prefix>.perfdata.<label>.value`.

**InfluxDB:** `feature enable influxdb` (v1) or `influxdb2`. Default `127.0.0.1` port `8086`. A `metric` tag with the perfdata label is added automatically; fields are value, warn, crit, min, max, unit. The database or bucket must already exist. With SELinux set the boolean `icinga2_can_connect_all`.

**Perfdata files:** `feature enable perfdata` writes `host-perfdata.<timestamp>` and `service-perfdata.<timestamp>` to `/var/spool/icinga2/perfdata/`, rotated every 15 seconds, for collectors like PNP or Graphios; collectors must delete processed files.

**HA zones:** by default every endpoint writes. Set `enable_ha = true` in the feature config on all endpoints so only one writes and others take over if the cluster connection breaks.

## Checked

2026-11-04. Confirmed against the Icinga 2 features chapter: documented writers, Graphite default 127.0.0.1:2003 and prefix macros and character replacement table, InfluxDB default port 8086, metric tag and fields, SELinux boolean, perfdata file 15 second rotation and spool path, enable_ha.

Method: documentation only; no commands were run.
