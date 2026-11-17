---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-cluster-flags-run
name: grafana-alloy-cluster-flags-run
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [clusterenabled, clusterjoin-addresses, clusterdiscover-peers, clusteradvertise-address, clusterwait-for-size, clusterenable-tls, dnssrv]
level: advanced
status: docs-checked
description: "Clustering flags of alloy run: join address DNS prefixes, discover-peers, advertise interfaces, TLS, wait-for-size and viewer, participant, terminating states."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/cli/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Clustering flags for alloy run

`--cluster.enabled` (default `false`) starts clustered mode. Related flags:
- `--cluster.node-name` (default hostname) and `--cluster.name` (nodes without the same name cannot join).
- `--cluster.join-addresses`: comma-separated IPs or DNS names, optional `:port` (default: the HTTP listener port, so all instances must share it). Mutually exclusive with `--cluster.discover-peers`.
- `--cluster.discover-peers`: tuples such as `provider=XXX key=val`; quote values containing spaces, backslashes or quotes.
- `--cluster.rejoin-interval` (default `60s`), `--cluster.max-join-peers` (default `5`).
- `--cluster.advertise-address` and `--cluster.advertise-interfaces` (default `eth0,en0`; `all` uses every interface).
- `--cluster.wait-for-size` (default `0`, disabled) and `--cluster.wait-timeout` (default `0`, wait forever): hold clustered components until enough nodes exist.
- TLS: `--cluster.enable-tls`, `--cluster.tls-ca-path`, `--cluster.tls-cert-path`, `--cluster.tls-key-path`, `--cluster.tls-server-name`.
- `--cluster.use-discovery-v1` is deprecated and does nothing.

## DNS prefixes for join addresses
- `dns+host:port`: A/AAAA lookup.
- `dnssrv+_alloy._tcp.alloy.namespace.svc.cluster.local`: SRV lookup, then A/AAAA per record.
- `dnssrvnoa+...`: SRV only.
- No prefix: tries both A/AAAA and SRV.

## States
A node joins as **viewer** (read-only), becomes **participant** once startup completes and shares work for components with clustering enabled, and moves to **terminating** on shutdown. The state shows on the clustering page of the UI.

## Checked

2026-11-04. Confirmed against the run CLI reference (reference/cli/run.md): cluster flags and defaults, DNS prefixes, discover-peers quoting, deprecated discovery-v1 flag, viewer/participant/terminating states. No claims changed.

Method: documentation only; no commands were run.
