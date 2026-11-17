---
id: computing-software.networking-hardware-and-wireless.check-point.clusterxl-modes-and-setup
name: clusterxl-modes-and-setup
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, clusterxl, high-availability, load-sharing]
level: practitioner
status: draft
description: "Build a ClusterXL cluster: VIPs, sync network, HA New mode versus Load Sharing, and member priority."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ClusterXL_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ClusterXL High Availability and Load Sharing setup

- In SmartConsole create a **Gateway Cluster** (wizard or classic): add members (SIC to each), then **Cluster Members**, **ClusterXL and VRRP** > choose **High Availability** (Active/Standby, "New" mode) or **Load Sharing** (Multicast or Unicast Pivot). Topology: each data interface has a **Cluster VIP** (e.g. 10.1.10.1) plus a member IP (10.1.10.2 / .3); the **Sync** interface has a dedicated network with no VIP.
```
cphaprob stat
cphaprob -a if
cphaprob roles                      # (confirm; R81+)
clusterXL_admin down -p             # persistent admin-down of this member
clusterXL_admin up -p
cphaconf set_ccp broadcast          # CCP mode: multicast or broadcast
```
- HA New mode: one Active, others Standby; the Active member's MAC answers for the VIP, and the VIP's MAC is the same MAC after failover (VMAC mode helps switches/Layer 2). Load Sharing needs a switch that accepts a multicast MAC for the VIP or uses Unicast Pivot.
- Priority/recovery: "Maintain current active Cluster Member" (default) avoids flapping back; "Switch to higher priority" fails back automatically.
- Use a dedicated sync interface, ideally a cable or bond between members, and not the production VLAN.
- Members must run the same version, Jumbo take and policy; mismatch shows as `Unable to verify` states.
- Gotcha: with HA and ARP caches on old routers, enable "Use Virtual MAC (VMAC)" under cluster > ClusterXL (confirm).

Verify: `cphaprob stat` shows one `Active` and one `Standby` with `Ready` state; `cphaprob -a if` lists each interface as `UP` with `Sync`, `Cluster` roles.
