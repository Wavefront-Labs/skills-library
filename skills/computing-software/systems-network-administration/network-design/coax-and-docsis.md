---
id: computing-software.systems-network-administration.network-design.coax-and-docsis
name: coax-and-docsis
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, docsis, cable-modem, coax, hfc, snr, upstream-downstream]
level: practitioner
status: docs-checked
description: "Understand and troubleshoot DOCSIS cable broadband: HFC architecture, DOCSIS 4.0 speeds, modem signal levels (power, SNR/MER, codewords), and bridge mode."
sources:
  - https://www.cablelabs.com/specifications/search?category=DOCSIS
  - https://www.cablelabs.com/technologies/docsis-4-0-technology
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Coax and DOCSIS

## Architecture
Hybrid fibre-coax (HFC): fibre to a neighbourhood node, coax to homes; the CMTS (or remote PHY)
at the headend. Upstream capacity is shared within a node, so evening congestion is typical.

## Versions
| DOCSIS | Max down / up (typical) | Notes |
|---|---|---|
| 3.0, 3.1 | see the CableLabs specifications | not confirmed here |
| 4.0 | up to 10 Gbps down / up to 6 Gbps up | CableLabs DOCSIS 4.0 page |

## Signal levels (read from the modem status page; its address is in the modem's documentation)
Acceptable power and SNR/MER ranges depend on the modulation and the operator's specification:
take them from the ISP or the modem vendor, not from rules of thumb.
| Metric | What to watch |
|---|---|
| Downstream and upstream power | inside the operator's stated range |
| Downstream SNR / MER | inside the operator's range for the modulation in use |
| Uncorrectable codewords | should not increase steadily |
| Timeouts in the modem log | possible upstream noise or ingress |

## Faults
- High uncorrectables, log timeouts -> loose/corroded connectors, damaged coax, unterminated
  splitter ports, cheap splitters. Remove splitters and test at the point of entry.
- Speed fine at night, poor evenings -> node congestion (ISP issue).
- Modem in router mode behind your firewall -> double NAT; request bridge mode/IP passthrough.
- Business static IPs on cable often use a gateway that must stay in a specific mode; check ISP docs.

## Verify
- [ ] Modem levels within range, uncorrectables stable over 24 h, latency under load measured, and bridge mode confirmed when your firewall holds the public IP.

## Checked

- Date: 2026-10-28
- Confirmed: DOCSIS 4.0 supports up to 10 Gbps downstream and up to 6 Gbps upstream over HFC (CableLabs DOCSIS 4.0 page).
- Removed: DOCSIS 3.0 and 3.1 speed figures, all dBmV and dB ranges, the 192.168.100.1 address, T3/T4 timer names (CableLabs specification page unreadable).

Method: documentation only; no commands were run.
