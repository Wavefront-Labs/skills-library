---
id: computing-software.networking-hardware-and-wireless.arista-eos.lldp
name: lldp
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, lldp, neighbor-discovery, lldp-neighbors]
level: practitioner
status: draft
description: "Use EOS LLDP to discover neighbors, tune transmit timers and verify cabling."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LLDP
Goal: confirm physical topology.

```
lldp run
lldp timer 30
lldp management-address Management1
interface Ethernet1
   lldp transmit
   lldp receive
```

```
show lldp neighbors
show lldp neighbors detail
show lldp local-info
```

- LLDP is on by default on EOS.
- Compare discovered neighbors against the intended design (AVD ‘connected endpoints’ or a cabling plan).
- CloudVision uses LLDP for topology.

Gotcha: some servers' NICs absorb LLDP in firmware, so a missing neighbor does not always mean a cabling problem.

Operational tip: compare LLDP neighbors against the design on a schedule via eAPI or telemetry; cabling drift is a frequent cause of mysterious path changes and MLAG inconsistencies. Disable LLDP transmit toward untrusted edge ports if the management address and system description should not be advertised to hosts. Cabling documentation should include the LLDP-reported remote port so a re-patch is caught by the next scheduled check.

## Verify
- `show lldp neighbors` lists the peer port as documented.
