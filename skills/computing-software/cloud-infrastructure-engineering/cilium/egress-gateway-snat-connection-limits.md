---
id: computing-software.cloud-infrastructure-engineering.cilium.egress-gateway-snat-connection-limits
name: egress-gateway-snat-connection-limits
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, egress-gateway, snat, nat-stats, node-port-range, connection-limits]
level: advanced
status: docs-checked
description: "Diagnose SNAT port exhaustion on Cilium egress gateway nodes with cilium-dbg shell db/show nat-stats and the 65535 minus node-port-range limit."
sources:
  - https://docs.cilium.io/en/stable/network/egress-gateway/egress-gateway-troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Egress gateway SNAT limits

Problem: many clients connect through one egress node to the same tuple {egress IP, remote IP, remote port}. The SNAT map allows only (65535 minus the upper bound of `--node-port-range`) source ports per tuple; default range top 32767 gives 32768 connections. Beyond that old connections are evicted and SNAT fails to find source ports, breaking existing connections.

Inspect: `kubectl -n kube-system exec ds/cilium -- cilium-dbg shell -- db/show nat-stats`. Columns IPFamily, Proto, EgressIP, RemoteAddr, Count. The agent keeps the top 30 tuples, recalculated every 30 seconds by default (so stats lag). A Count approaching 32768 indicates overflow.

Fix: it is a hard limit, so reduce connections SNATed through the gateway (fewer new connections from clients, or spread connections over more remote addresses). Alert on the NAT endpoint max connection metric for source-port saturation.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/network/egress-gateway/egress-gateway-troubleshooting/. 

Method: documentation only; no commands were run.
