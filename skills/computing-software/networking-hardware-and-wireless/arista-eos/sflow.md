---
id: computing-software.networking-hardware-and-wireless.arista-eos.sflow
name: sflow
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, sflow, flow-monitoring, sflow-collector, sample-rate]
level: practitioner
status: draft
description: "Enable EOS sFlow with a collector, sample rate and per-interface enablement."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sFlow
Goal: sampled traffic visibility.

```
sflow source-interface Management1
sflow vrf MGMT destination 192.0.2.80
sflow sample 16384
sflow polling-interval 30
sflow run
interface Ethernet1
   sflow enable
```

```
show sflow
show sflow interfaces
```

- Sample rate is 1 in N; higher N means lighter load but less detail.
- Hardware sFlow on many platforms; `sflow hardware acceleration` options (confirm).
- Collectors: sFlow-RT, ntopng, pmacct.

Gotcha: forgetting `sflow run` or the VRF on the destination yields no flow records; interface-level `sflow enable` is also needed.

Operational tip: enable sFlow on all fabric ports but choose a sample rate scaled to link speed (for example 1 in 32768 on 100G). Verify the collector's clock and NAT path if datagrams seem missing. Remember sFlow samples packets at ingress and egress separately on some platforms, so be consistent when comparing numbers with SNMP counters.

## Verify
- `show sflow` shows `Running` and the collector's `Datagrams sent` counter increases.
