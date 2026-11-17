---
id: computing-software.cloud-infrastructure-engineering.azure.load-balancer-distribution-mode-and-source-ip-affinity
name: load-balancer-distribution-mode-and-source-ip-affinity
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, load-balancer, source-ip-affinity, distribution-mode, session-persistence, tcp-reset, idle-timeout]
level: practitioner
status: docs-checked
description: "Choose Azure Load Balancer distribution: 5-tuple hash vs SourceIP and SourceIPProtocol affinity, NAT'd-client hot spots, idle timeout and TCP reset settings."
sources: ["https://learn.microsoft.com/azure/load-balancer/distribution-mode-concepts", "https://learn.microsoft.com/azure/load-balancer/load-balancer-distribution-mode", "https://learn.microsoft.com/azure/load-balancer/load-balancer-tcp-reset"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distribution mode and session persistence

**Goal:** stateful legacy apps keep clients on one backend without creating a single hot node.

## Modes (per load-balancing rule)
| `loadDistribution` | Hash of | Behaviour |
|---|---|---|
| Default | Source IP, source port, dest IP, dest port, protocol (5-tuple) | Each new connection can hit any backend |
| SourceIPProtocol | Source IP + dest IP + protocol (3-tuple) | Same client + protocol -> same backend |
| SourceIP | Source IP + dest IP (2-tuple) | Same client -> same backend across protocols |
```bash
az network lb rule update -g rg --lb-name lb-app -n rule-https --load-distribution SourceIP
```

## Trade-offs
- Clients behind a corporate NAT/proxy share one source IP - they all land on one backend (hot spot).
- When backend pool members are added or removed, distribution is recomputed, so new connections from existing clients may land elsewhere - apps must tolerate it.
- For HTTP apps prefer a stateless design over relying on source IP affinity.
- Documented use cases: Remote Desktop Gateway (client IP and protocol, 3-tuple) and media upload where a client's UDP data session must reach the same backend as its TCP control session.

## Idle timeout and TCP reset
```bash
az network lb rule update -g rg --lb-name lb-app -n rule-https --idle-timeout 15 --enable-tcp-reset true
```
- Standard LB idle timeout is 4 to 100 minutes for load-balancing and inbound NAT rules (4 to 120 for outbound rules), default 4; idle flows are dropped silently unless **TCP reset** is enabled, which sends RST to both ends so apps fail fast instead of hanging. Idle timeout isn't supported on UDP rules, and TCP reset isn't supported on internal HA ports rules with an NVA in the path.
- Prefer application/OS keepalives shorter than the timeout for long-lived idle connections.

## Gotchas
- Switching distribution mode causes no downtime.
- For inbound rules, if the frontend IP's idle timeout differs from the rule's, the frontend IP's value takes precedence.

## Verify
- [ ] Repeated connections from one test client hit the same backend (log hostnames); load spread across backends from many clients remains acceptable.

## Checked

2026-10-31. Confirmed against the Learn Load Balancer distribution mode concepts page (5-, 3- and 2-tuple modes, loadDistribution values, proxy and NAT hot spots, recomputation when pool members change, RD Gateway and media upload cases, no downtime on switching) and the TCP reset and idle timeout page (4 to 100 and 4 to 120 minute ranges, default 4, silent drop without TCP reset, frontend IP precedence, limitations); corrected the idle timeout range. Removed: the probe-failure affinity claim, the Layer 7 product names and the Gateway LB hashing note (not in the docs). Commands were checked with check_commands.py.

Method: documentation only; no commands were run.
