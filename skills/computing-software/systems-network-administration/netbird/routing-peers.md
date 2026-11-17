---
id: computing-software.systems-network-administration.netbird.routing-peers
name: routing-peers
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, routing-peers, ip-forwarding, ha-failover, input-chain-policy]
level: practitioner
status: docs-checked
description: "Run NetBird routing peers correctly: IP forwarding, container capabilities, HA selection order, forward versus input policies, DNS forwarder port and troubleshooting."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/networks/how-routing-peers-work.mdx
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/networks/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A routing peer forwards overlay traffic to resources that cannot run the client (LANs, VPCs, data centers, Kubernetes). Prefer Networks over legacy Routes; keep Routes for exit nodes.

Requirements:
- Linux is the common production choice; other platforms forward in userspace.
- Enable IP forwarding (`net.ipv4.ip_forward`, `net.ipv6.conf.all.forwarding`); the Linux client usually does it.
- Containers need `NET_ADMIN`.
- The peer needs direct reachability to the resources (subnets, security groups).
- `NB_ENABLE_LOCAL_FORWARDING` on userspace peers allows reaching the peer's own LAN IP; enable only if you accept that exposure.

HA: clients choose by connection status, then metric (lowest wins), then direct over relayed, then latency. Different metrics give primary/failover; equal metrics give nearest peer. Put HA peers in separate failure domains. HA is failover, not load balancing. Peers added as a group share one metric with no primary.

Policies: forward chain governs traffic through the peer; reaching the peer itself (SSH, Grafana) needs a separate peer-to-peer policy (input chain). Policies with a network resource destination are one-way.

Troubleshoot: `netbird status -d`, `netbird networks ls`, `netbird debug trace`; on the peer check forwarding, `ip route` and nftables/iptables. Frequent mistake: resource policy works but no input-chain policy exists.

Enable the Routing Peer Disconnected notification.

## Checked

2026-11-04. Confirmed against the NetBird How Routing Peers Work and Networks pages: OS support, IP forwarding sysctls, `NB_ENABLE_LOCAL_FORWARDING` conditions, container capabilities, reachability, HA selection order and metric behaviour, failure domains, forward versus input chain, one-way resource policies, troubleshooting commands, disconnected notification. Nothing removed.
Method: documentation only; no commands were run.
