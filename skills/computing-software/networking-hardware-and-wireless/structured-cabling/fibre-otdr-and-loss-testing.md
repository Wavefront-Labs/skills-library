---
id: computing-software.networking-hardware-and-wireless.structured-cabling.fibre-otdr-and-loss-testing
name: fibre-otdr-and-loss-testing
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [fibre-otdr, fibre-loss-budget, tier-1-tier-2-testing]
level: advanced
status: draft
description: "Test fibre with a light source and power meter for loss budget (Tier 1) and an OTDR trace for events and length (Tier 2)."
sources:
  - https://tiaonline.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fibre testing

- Tier 1 (OLTS): measure total loss with a source and power meter at the correct wavelengths with correct reference method; compare to the budget (fibre attenuation x length + connector and splice loss).
- Tier 2 (OTDR): trace events (connectors, splices, bends) and fibre length; use launch and tail cords so the first and last connectors are characterised.
- Typical budget components: connector pair loss commonly 0.75 dB maximum, splice loss around 0.3 dB (fusion usually lower); use your contract's numbers.
- Test multimode at 850 and 1300 nm, singlemode at 1310 and 1550 nm.
- Always clean and inspect before testing; dirty connectors skew results.

## Verify
- [ ] Measured loss is within the budget with margin and the report is saved per link.
