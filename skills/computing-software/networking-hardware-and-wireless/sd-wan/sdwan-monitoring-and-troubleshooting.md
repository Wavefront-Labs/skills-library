---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-monitoring-and-troubleshooting
name: sdwan-monitoring-and-troubleshooting
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-troubleshooting, tunnel-health-monitoring, sdwan-assurance, sdwan-operations]
level: practitioner
status: draft
description: "Monitor tunnel loss/latency/jitter and troubleshoot control connection, tunnel, policy and MTU issues step by step."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD-WAN troubleshooting

1. Control connections to orchestrator/controllers up? Certificate valid and time (NTP) correct - expired certs and wrong clocks are classic causes.
2. Underlay: circuit up, IP/gateway reachable, DNS, firewall allows required UDP ports.
3. Tunnels: state per transport, BFD/probe stats, NAT type.
4. Routing: overlay and LAN routes advertised; check policies for filters.
5. Policy: which SLA class a flow matched and the chosen path.
6. MTU/MSS: black-holed large packets look like "slow apps".
- Use the vendor's flow trace/packet capture on the edge; confirm exact commands in docs.
- Keep a "single pane" dashboard for tunnel health per site and set alerts on SLA violations.

## Verify
- [ ] Root cause is reproduced and a regression alert covers it.
