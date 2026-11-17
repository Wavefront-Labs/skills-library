---
id: computing-software.cloud-infrastructure-engineering.calico.data-path-routes-arp-and-no-overlay
name: data-path-routes-arp-and-no-overlay
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [architecture, data-path, routing, felix, bgp, arp, iptables, ebpf]
level: intro
status: docs-checked
description: "How Calico forwards pod traffic by plain IP routing: host MAC answers ARP, per-workload routes, and who installs them (Felix or BGP)."
sources:
  - https://docs.tigera.io/calico/latest/reference/architecture/data-path
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico's basic data path adds no encapsulation: packets to and from a workload are routed and firewalled by the Linux routing table plus iptables or eBPF on the workload's host.

**Sending side.** Calico ensures the host's MAC is always the next-hop MAC the workload sees, whatever routing the workload configures itself. **Receiving side.** The last IP hop is from the destination workload's host to the workload.

The page's example uses workloads in 10.65/16 on hosts in 172.18.203/24. `route -n` on a host shows:

| Route | Meaning |
|---|---|
| `10.65.0.24` via interface `tapa429fb36-04`, flags UH | Local workload, direct route on its tap or veth |
| `10.65.0.21` via gateway `172.18.203.126`, flags UGH | Workload on another host, routed via that host |
| `10.65.0.22` and `.23` via `172.18.203.129` | Two workloads on a second host |

Who creates which route:

- Direct (local) routes are set up by Felix when asked to provision connectivity for a workload.
- Indirect routes to other hosts appear because a BGP client such as BIRD notices Felix's routes and distributes them, perhaps through a route reflector, to BGP clients on other hosts.
- Alternatively, Felix can program the indirect (cluster) routes itself for VXLAN, IP-in-IP or unencapsulated IP pools, if Felix is configured to program cluster routes.

The page states that the static data path is only ARP answers with the host MAC, IP routing and iptables or eBPF; the complexity is in managing routing and security information and dynamic events such as workload migration.

## Checked

Read in full on 2026-11-08: the Calico data path page. The route table example, route origins and Felix-programmed cluster routes match it.

Method: documentation only; no commands were run.
