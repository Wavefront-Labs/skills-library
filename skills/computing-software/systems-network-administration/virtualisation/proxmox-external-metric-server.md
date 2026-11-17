---
id: computing-software.systems-network-administration.virtualisation.proxmox-external-metric-server
name: proxmox-external-metric-server
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-metric-server, influxdb, graphite, proxmox, monitoring]
level: practitioner
status: docs-checked
description: "Send Proxmox VE node, guest and storage metrics to InfluxDB (UDP or HTTP API v2) or Graphite, with status.cfg examples and Grafana tips."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#external_metric_server
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External metric server (InfluxDB or Graphite)

**Goal:** long-term metrics for nodes, VMs, containers and storage in your monitoring stack.

## Add a target
Datacenter -> **Metric Server** -> Add -> *InfluxDB* or *Graphite*. Every node pushes its own stats. The config is cluster-wide in `/etc/pve/status.cfg`:
```
influxdb: influx-prod
	server influx.example.com
	port 8086
	influxdbproto https
	organization infra
	bucket proxmox
	token <api-token>
	max-body-size 25000000

graphite: graphite1
	server 10.0.0.40
	port 2003
	proto tcp
	path proxmox
```

## InfluxDB choices
- **HTTP(S) API v2** with organization, bucket and token: reliable, works with InfluxDB 2.x and 1.8+ compatibility endpoints.
- **UDP** (the plugin default): the InfluxDB server needs a UDP listener, and the MTU can be configured for non-1500 networks.

## Grafana
Use a community Proxmox dashboard built for your InfluxDB flavour (Flux vs InfluxQL), and template on `host` and `vmid`.

## Gotchas
- Token needs write access to the bucket only.
- `disable 1` pauses a target without deleting it.
- Every node must reach the metric server; firewall rules on the server side by node IP.
- Metric cardinality grows with guests; set bucket retention.

## Verify
In InfluxDB Data Explorer, data from each node appears in the bucket.

## Checked
2026-11-01. Confirmed in the Proxmox VE admin guide (Metric Server): Graphite and InfluxDB targets, Graphite default port 2003 and path proxmox, UDP default with MTU option, InfluxDB v2 HTTP(S) mode with token, organization and bucket, 1.8 compatible endpoint, `max-body-size`. Removed: push interval, measurement names and tags.
Method: documentation only; no commands were run.
