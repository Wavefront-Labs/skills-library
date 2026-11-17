---
id: computing-software.systems-network-administration.proxmox-ve.external-metric-server
name: external-metric-server
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [metrics, influxdb, graphite, opentelemetry, status-cfg]
level: practitioner
status: docs-checked
description: "Send host, guest and storage statistics to Graphite, InfluxDB or OpenTelemetry from Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
External metric servers periodically receive stats about hosts, guests and storages. Supported targets are Graphite, InfluxDB and OpenTelemetry. Definitions are stored in `/etc/pve/status.cfg` and are editable in the web interface.

Graphite: default port 2003, default path `proxmox`. Data goes over UDP by default, so the Graphite server must accept UDP; the MTU can be configured for non-1500 networks. TCP is possible, and a timeout is required so that a network fault does not block the `pvestatd` statistics daemon.

InfluxDB: data is sent over UDP by default, with a configurable MTU. A matching InfluxDB 1.x listener looks like:

```
[[udp]]
   enabled = true
   bind-address = "0.0.0.0:8089"
   database = "proxmox"
   batch-size = 1000
   batch-timeout = "1s"
```

Alternatively use the HTTP(S) v2 API by setting `influxdbproto` to `http` or `https`. The defaults are organization `proxmox` and bucket `proxmox` (settings `organization` and `bucket`). The v2 API needs a token that can write to the bucket; on InfluxDB 1.8.x, which has a compatible endpoint, `user:password` can serve as token and the organization is ignored. HTTP timeout defaults to 1s (`timeout`) and the maximum batch size to 25000000 bytes (`max-body-size`).

Because transmission is UDP by default, missing data usually means the receiver is not listening on the expected port or the MTU is wrong.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-sysadmin.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
