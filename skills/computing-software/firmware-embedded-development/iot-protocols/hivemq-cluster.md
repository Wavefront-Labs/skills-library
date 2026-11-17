---
id: computing-software.firmware-embedded-development.iot-protocols.hivemq-cluster
name: hivemq-cluster
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [hivemq-cluster, hivemq-broker, hivemq, cluster, discovery, iot-protocols]
level: practitioner
status: docs-checked
description: "HiveMQ clustering: Configure transport and discovery for a HiveMQ cluster."
sources:
  - https://docs.hivemq.com/hivemq/latest/user-guide/cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HiveMQ clustering and operations

**Goal:** Configure a HiveMQ cluster for production.

## Steps
1. Enable clustering in config.xml: a `<cluster>` element with `<enabled>true</enabled>`, a `<transport>` (TCP with bind-address and bind-port, or UDP) and a `<discovery>` mechanism
2. Discovery mechanisms are static (fixed node list with TCP host and port), multicast, broadcast, and extension (a HiveMQ extension supplies the node list); not every discovery mechanism is compatible with every transport, and multicast is the only discovery method usable with UDP transport
3. If transport and discovery are not set, HiveMQ uses UDP transport with multicast discovery; the page recommends that minimal configuration only for local test networks and says UDP transport is not suitable for production
4. For a fixed-size, highly available deployment static discovery with TCP transport is the usual choice
5. Clients can connect to any node of the cluster, which acts as one logical broker

## Gotcha
Most cloud providers (including AWS) do not permit IP multicast and most do not allow broadcasting, so multicast and broadcast discovery fail there; use static discovery or an extension. Broadcast discovery also needs all nodes in the same IP subnet. Transport certificates are read only at startup, so rotating them needs a rolling restart.

## Verify
- [ ] Every node reports the expected cluster size in its log or in monitoring
- [ ] Stopping one node leaves clients able to reconnect to the others

## Checked

2026-11-03. Confirmed in the HiveMQ MQTT Broker Clusters page: config.xml cluster, enabled, transport and discovery elements, discovery mechanism table, defaults, multicast and broadcast cloud limits, same-subnet rule for broadcast, certificate-read-at-startup note. Removed: DNS and Kubernetes discovery names, replication factor, load balancer health checks, Control Center and Prometheus monitoring, and rolling-upgrade rules (not on the reachable pages).
Method: documentation only; no commands were run.
