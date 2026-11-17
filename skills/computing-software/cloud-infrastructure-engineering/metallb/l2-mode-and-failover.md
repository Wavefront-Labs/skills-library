---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-mode-and-failover
name: l2-mode-and-failover
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, layer2, failover, memberlist, arp, ndp, gratuitous-packets, single-node-bottleneck]
level: practitioner
status: docs-checked
description: "MetalLB layer 2 mode behaviour: one leader node per IP, memberlist failure detection, gratuitous packets on failover, bandwidth limit and how to handle slow failover."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/layer2.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L2 mode and failover

One node answers ARP (IPv4) or NDP (IPv6) for the service IP; to the LAN it looks like that machine has extra addresses. It works on any Ethernet network.

- All traffic for the IP lands on that node, then `kube-proxy` spreads it across pods. This is failover, not load balancing.
- A failed node is detected with memberlist; other nodes then take over its IPs.
- On failover MetalLB sends gratuitous (really unsolicited) L2 packets so clients update the IP-to-MAC mapping.

Limits:
1. Ingress bandwidth for one service IP is capped at one node's bandwidth.
2. Failover relies on clients. All modern Windows, Mac and Linux handle it and recover within a few seconds. Old or unusual OSes may delay neighbor cache refresh.

Practice:
- For planned leadership changes, keep the old leader up for a couple of minutes so it can forward for clients with stale caches.
- On unplanned failover, buggy clients cannot reach the IP until their cache entry refreshes.
- If failover takes more than about 10s, the docs ask you to file a bug at github.com/metallb/metallb/issues/new.

Related: `computing-software.cloud-infrastructure-engineering.metallb.l2-periodic-gratuitous-arp`, `computing-software.cloud-infrastructure-engineering.metallb.l2-leader-election`.

## Checked
2026-11-04. Confirmed against the MetalLB "layer 2 mode" page: ARP and NDP, failover via memberlist, gratuitous packets, bandwidth limit, client cooperation, the couple-of-minutes advice, and the 10s bug-report threshold.
Method: documentation only; no commands were run.
