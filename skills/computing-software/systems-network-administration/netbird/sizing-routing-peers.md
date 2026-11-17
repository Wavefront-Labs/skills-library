---
id: computing-software.systems-network-administration.netbird.sizing-routing-peers
name: sizing-routing-peers
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, capacity-planning, routing-peer-sizing, throughput, jumbo-frames]
level: advanced
status: docs-checked
description: "Size NetBird routing peers by sustained throughput: four-step method, per-vCPU capacity table, tuning levers (kernel WireGuard, MTU) and validation with iperf3."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/networks/sizing-routing-peers.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Size against sustained traffic in the direction users use, not enrolled user count. Each tunnel is handled mostly by one core, so capacity comes from many tunnels across cores.

Method:
1. Peak throughput = peak simultaneously active users x per-user rate.
2. Read per-peer capacity from the table or measure.
3. Active peers = ceil(peak / per-peer capacity).
4. A single Network does not split traffic across its peers: build one identical Network per share of traffic, each with 2+ routing peers for failover, and assign client groups by policy.

Approximate capacity (kernel WireGuard, 1280 MTU, TCP, ~20% variation), download / upload Gbps:
- 1 vCPU ~2/~2; 2 vCPU ~3/~3; 4 vCPU ~7/~4; 8 vCPU ~13/~11
- 16 vCPU ~20/~15; 32 vCPU ~25/~15; 64 vCPU ~31/~15

Downloads (peer encrypts) run about twice as fast as uploads. Upload flattens near 16 cores, so 16 to 32 vCPUs is the sweet spot. Small packets run at about half.

Levers: kernel WireGuard (userspace plateaus near 6.8 Gbps download); a NIC that is not the bottleneck; jumbo frames (8920-byte tunnel MTU lifted 64-vCPU download from ~31 to ~95 Gbps in testing) only where the whole path supports it; cores up to ~16, then add peers.

Cloud notes: single flows may be capped (about 5 Gbps on AWS); use network-optimized instances; routing peers need no inbound ports.

Validate with iperf3 3.16+, read the WireGuard interface byte counters, watch CPU with mpstat.

## Checked

2026-11-04. Confirmed against the NetBird sizing routing peers page. Nothing removed.
Method: documentation only; no commands were run.
