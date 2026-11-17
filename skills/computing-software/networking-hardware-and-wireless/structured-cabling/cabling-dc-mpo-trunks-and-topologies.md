---
id: computing-software.networking-hardware-and-wireless.structured-cabling.cabling-dc-mpo-trunks-and-topologies
name: cabling-dc-mpo-trunks-and-topologies
category: computing-software
field: networking-hardware-and-wireless
product: structured-cabling
tags: [dc-mpo-trunk, tor-vs-eor, cabling-tia-942, cabling-data-centre]
level: advanced
status: draft
description: "Design data-centre cabling with MPO trunks, breakout cassettes, top-of-rack versus end-of-row topology and clear polarity."
sources:
  - https://tiaonline.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data-centre cabling

- ToR: a switch per rack, short intra-rack DAC/AOC, few uplinks leaving the rack. EoR/MoR: longer cabling to a row-end switch with structured copper/fibre to servers. Pick by port density, growth and cabling cost.
- MPO/MTP trunks (12/24 fibres) link patch panels or cassettes; breakout (40G to 4x10G, 100G to 4x25G) uses breakout cassettes or cables. Keep one polarity method end to end (TIA-568.3-D methods A/B/C).
- TIA-942 defines data-centre spaces (entrance room, main distribution area, horizontal distribution area, equipment distribution area) and topology.
- Document every patch and keep labels consistent with the rack elevation records.
- Cable management: vertical/horizontal managers, no blocking of airflow.

## Verify
- [ ] A polarity test/OLTS confirms transmit-to-receive on every channel before turn-up.
