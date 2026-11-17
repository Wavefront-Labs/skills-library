---
id: computing-software.networking-hardware-and-wireless.strongswan.per-cpu-sas
name: per-cpu-sas
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, per-cpu-sas, rfc-9611, rss, performance]
level: advanced
status: docs-checked
description: "Scale strongSwan throughput with per-CPU child SAs (RFC 9611): trap start_action with per_cpu_sas, fallback SA behaviour, and RSS setup with ethtool or UDP encapsulation."
sources:
  - https://docs.strongswan.org/docs/latest/features/per-cpu-sas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# per cpu sas
RFC 9611 lets IKEv2 create duplicate Child SAs for specific resources such as CPUs or NIC queues, so each has exclusive use of an SA and does not synchronise crypto state, sequence numbers and anti-replay windows. Linux supports it from 6.13 and strongSwan from 6.0.2, per the page.

**How it works.** Trap policies trigger separate acquires for packets from different CPUs, and a Child SA is negotiated per CPU; the CPU ID is assigned to the SA at install time. Meanwhile a fallback SA with no CPU ID carries traffic. As responder strongSwan first ensures a fallback SA exists, then assigns each new SA a CPU ID without an SA yet. CPU IDs are not negotiated (a received ID is for debugging only), so CPU counts can differ and more SAs than needed may exist.

**Configure.** Both are required: `start_action = trap` on the child and `per_cpu_sas` enabled (`encap` selects the UDP encapsulation variant). Enabling alone is not enough; the system needs careful tuning.

**Inbound.** Use Receive Side Scaling on the NIC to spread flows. For NICs with ESP support:

```
ethtool -N <nic> rx-flow-hash esp4
ethtool -N <nic> flow-type esp4 src-ip <ip> dst-ip <ip> spi 0x<spi> action <queue>
```

Without NIC ESP support use UDP encapsulation with a random source port per SA, or software options such as XDP cpumap redirect.

**Outbound.** Pin processes or threads to CPU cores if not all CPUs can be used efficiently with the NIC.

## Checked
2026-11-04. Confirmed against the strongSwan Per-CPU SAs page: Linux 6.13 and strongSwan 6.0.2, trap plus per_cpu_sas, fallback SA, CPU IDs not negotiated, RSS ethtool commands, UDP encapsulation variant. Nothing removed.

Method: documentation only; no commands were run.
