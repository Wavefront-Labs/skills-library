---
id: computing-software.networking-hardware-and-wireless.check-point.clusterxl-state-sync-and-delayed
name: clusterxl-state-sync-and-delayed
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, state-synchronization, delayed-sync, fw-ctl-sync]
level: practitioner
status: draft
description: "Tune ClusterXL state sync: what is synchronized, delayed synchronization for short-lived services and sync-network sizing."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ClusterXL_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_PerformanceTuning_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# State synchronization and delayed sync

```
cphaprob syncstat                   # sync statistics, lost updates
fw ctl pstat                        # sync section: total/lost updates
fw tab -t connections -s            # connection table size on this member
fw ctl set int fw_sync_delay_ms 3000 # (confirm) not recommended on production without guidance
```
- Connections are synchronized member-to-member over the sync network so that a failover keeps established sessions. Most traffic is synchronized; to reduce load, **Delayed synchronization** (per service in the object: Advanced > Synchronize connections on cluster / "Start synchronizing X seconds after connection initiation", default 3 s for HTTP, SMTP and similar short-lived services) skips short connections.
- Non-synchronized services: you can untick "Synchronize connections on cluster" on specific services (e.g. DNS, ICMP) in SmartConsole, then they will drop on failover.
- Sync network sizing: 1 Gb is enough for most; use 10 Gb for high connection-rate sites. A `cphaprob syncstat` with `Lost updates` or `Sync retransmits` rising means the link or members are too busy.
- In Load Sharing cluster, sync is mandatory for correct stateful processing.
- Gotcha: VPN, NAT and Identity Awareness each add state; verifying them across failover is a separate test (try a ping/ssh before failing over).

Verify: during a manual failover (`clusterXL_admin down -p`), an SSH session across the cluster must survive; `cphaprob syncstat` shows `Sync status OK` and low `Lost updates`.
