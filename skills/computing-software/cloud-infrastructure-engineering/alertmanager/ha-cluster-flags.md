---
id: computing-software.cloud-infrastructure-engineering.alertmanager.ha-cluster-flags
name: ha-cluster-flags
category: computing-software
field: cloud-infrastructure-engineering
product: alertmanager
tags: [alertmanager, high-availability, cluster-flags, gossip]
level: advanced
status: docs-checked
description: "Alertmanager --cluster.* flags with defaults: listen-address 9094, peer, peer-timeout, gossip-interval, pushpull-interval, label and UDP plus TCP requirement."
sources: ["https://raw.githubusercontent.com/prometheus/alertmanager/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# High availability cluster flags

Alertmanager high availability is enabled by default. Instances communicate with each other through the `--cluster.*` flags.

Important: since 0.15 both UDP and TCP are needed for the cluster. Whitelist the clustering port for both protocols in firewalls, and expose it for both in containers.

Flags and defaults:
- `--cluster.listen-address`: default `0.0.0.0:9094`; an empty string disables HA mode.
- `--cluster.advertise-address`: advertised address.
- `--cluster.peer`: initial peers; repeat the flag for each.
- `--cluster.peer-timeout`: `15s`.
- `--cluster.peers-resolve-timeout`: `15s`.
- `--cluster.gossip-interval`: `200ms`, message propagation speed.
- `--cluster.pushpull-interval`: `1m0s`; lower values speed convergence at the expense of bandwidth.
- `--cluster.settle-timeout`: maximum wait for cluster connections to settle before evaluating notifications.
- `--cluster.tcp-timeout`: `10s`.
- `--cluster.probe-timeout`: `500ms`, wait for ack before marking a node unhealthy.
- `--cluster.probe-interval`: `1s`.
- `--cluster.reconnect-interval`: `10s`.
- `--cluster.reconnect-timeout`: `6h0m0s`.
- `--cluster.label`: optional string included on each packet and stream; uniquely identifies the cluster and prevents cross-communication.

The port in `cluster.listen-address` is the one to give other peers in `cluster.peer`. `cluster.advertise-address` is required if the instance has no IP from RFC 6890 with a default route.

## Checked

2026-11-03. Confirmed against the Alertmanager README: all --cluster.* flags, defaults, UDP plus TCP note, RFC 6890 advertise-address note.

Method: documentation only; no commands were run.
