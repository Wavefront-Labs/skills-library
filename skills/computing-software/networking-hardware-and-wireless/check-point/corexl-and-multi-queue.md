---
id: computing-software.networking-hardware-and-wireless.check-point.corexl-and-multi-queue
name: corexl-and-multi-queue
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, corexl, multi-queue, cpu-affinity]
level: practitioner
status: draft
description: "Tune CoreXL firewall instances, CPU affinity and Multi-Queue on Check Point gateways and read the split between SND and instances."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_PerformanceTuning_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CoreXL instances, affinity and Multi-Queue

```
fw ctl multik stat                 # per-instance connections and CPU
fw ctl affinity -l -r              # listing of CPU affinities (SND, fwk, daemons)
fw ctl affinity -s -i eth1 2       # (legacy) bind an interface to CPU 2
cpmq get -a                         # Multi-Queue status per interface
cpmq set                            # interactive: enable Multi-Queue
cpconfig                            # "Check Point CoreXL" - change the number of instances (reboot)
```
- CoreXL runs multiple firewall kernel **instances** (fwk) in parallel on separate cores; **SND** (Secure Network Distributor) cores handle NIC interrupts and SecureXL. The default split depends on core count (e.g. 4 cores: 1 SND + 3 FWK).
- Imbalance (one instance at 100% while others idle) usually means a few **elephant flows**; relief through SecureXL acceleration, Fast Acceleration, or the "Dynamic Balancing" feature (R81.20: `dynamic_balancing`, confirm).
- **Multi-Queue** lets several SND cores service one NIC's receive queues; without it, one NIC is bound to one SND core. Enable with `cpmq set` for the busiest 10G interfaces (drivers must support it; Intel `igb`/`ixgbe`, `i40e`).
- If SND cores are saturated and instances idle, add SND cores; if instances are saturated, reduce SND cores. Use `cpview` > Advanced > CoreXL to decide.
- Gotcha: changing instances needs a reboot, and on a cluster all members must have the same number of instances.

Verify: `fw ctl multik stat` shows a balanced connection spread; `top -H` shows load distribution; `cpmq get` lists "Active" for the interfaces you enabled.
