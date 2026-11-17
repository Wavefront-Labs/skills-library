---
id: computing-software.cybersecurity-defensive.security-architecture.data-diodes-and-air-gaps
name: data-diodes-and-air-gaps
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [network-segmentation, data-diode, air-gap, unidirectional-gateway, ot-security, cross-domain-solution, removable-media-kiosk]
level: advanced
status: draft
description: "Design air-gapped and one-way networks: unidirectional gateways for OT data, what a real air gap requires, media transfer kiosks, and patching isolated systems."
sources: ["https://www.cisa.gov/sites/default/files/2023-01/ics-cert_defense_in_depth_2016_s508c.pdf", "https://csrc.nist.gov/pubs/sp/800/82/r3/final", "https://www.ncsc.gov.uk/collection/cross-domain-solutions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data diodes and air gaps

## Data diode (unidirectional gateway)
Hardware that physically allows traffic in one direction only (e.g. fibre transmitter with no
receiver on the return path). Protocols that need acknowledgements (TCP) are handled by proxy
servers on each side that terminate and re-create sessions.
Typical uses:
- OT -> IT: replicate historian data, syslog, SNMP traps, file transfers, AV signature status out of
  the control network; nothing can be sent in.
- High -> low or low -> high classification domains (cross-domain solutions add content inspection).
Vendors: Owl, Waterfall, Hirschmann/Belden, Advenica, and software-based options with hardware diodes.

## Design points
- Decide what must flow out and how often; every protocol needs proxy support (OPC, Modbus replication,
  historian-specific replication, file transfer, syslog).
- Nothing comes back: no remote support, no patches, no acknowledgements at application level.
  Plan separate, controlled inbound paths for patching (below).
- Monitoring of the diode itself: proxies' health on both sides.

## Real air gaps
An air gap means no network path at all, including:
- No dual-homed engineering laptops, no cellular modems in PLC cabinets, no vendor remote access boxes,
  no wireless (check for Wi-Fi/Bluetooth chips in devices).
- Audit periodically: physical inspection and RF surveys; most "air-gapped" networks have bridges.

## Inbound transfers (patches, signatures, project files)
- Dedicated media transfer kiosk (multi-AV scanning, CDR content disarm, logging) outside the gap.
- Controlled, registered USB media used only for the transfer, scanned again inside.
- Hash verification against vendor-published hashes; signed packages only.
- Offline update infrastructure inside (WSUS offline sync, internal package mirrors, offline AV
  definition updates).

## Gotchas
- Stuxnet crossed an air gap on USB; removable media control is part of the design, not an afterthought.
- Time sync: isolated networks need their own GPS/PTP time source for log correlation.
- Diodes break applications that silently expected two-way traffic; test each data flow.

## Verify
Attempt a connection from the low side to the high side (must fail physically), confirm each
outbound data flow arrives, and audit the kiosk logs against a sample of transfers.
