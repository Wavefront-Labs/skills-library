---
id: computing-software.systems-network-administration.network-design.wifi-antenna-selection-and-mounting
name: wifi-antenna-selection-and-mounting
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wireless-design, antenna-selection, omni-antenna, directional-antenna, eirp, ap-mounting]
level: practitioner
status: draft
description: "Choose internal vs external antennas, omni vs patch vs sector, and mount APs correctly: gain, beamwidth, EIRP limits, ceiling height and orientation mistakes."
sources:
  - https://www.cisco.com/c/en/us/products/collateral/wireless/aironet-antennas-accessories/product_data_sheet09186a008008883b.html
  - https://www.cwnp.com/cwna/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Antenna selection and mounting

## Types
| Antenna | Pattern | Use |
|---|---|---|
| Internal omni (most APs) | doughnut, downward-optimised for ceiling mount | offices, classrooms, ceilings up to ~4-5 m |
| External dipole/omni | doughnut | flexible orientation, plenum mounting |
| Patch / panel | 60-90 degree beam | warehouses aisles, high ceilings, auditoriums (pointed down), wall mounting |
| Sector | 60-120 degree, long | outdoor, stadiums |
| Yagi / dish / grid | narrow, high gain | point-to-point links |

## Gain and EIRP
- EIRP (dBm) = Tx power + antenna gain - cable loss. Regulators cap EIRP; higher gain forces lower
  Tx power on many systems and narrows coverage vertically.
- High gain omni = flatter doughnut: good across a wide warehouse at moderate height, poor right
  underneath.
- Client devices have weak radios; high AP power creates asymmetric links where the client hears
  the AP but the AP cannot hear the client. Balance with lower AP power and more APs.

## Mounting rules
- Ceiling-mounted internal-antenna APs: flat, logo facing down, below metal grids/ducts not above.
  Wall-mounting a ceiling AP sends the pattern sideways into the next floor.
- Ceilings > 6-7 m: use downtilt patch antennas or drop the AP on a pole/pendant.
- Keep 1 m+ clearance from metal objects, light fittings, and other radios.
- External antennas: all elements connected (unused ports confuse MIMO), same orientation for
  dipoles (vertical for clients standing up), correct band per port.
- Outdoor: weatherproof connectors, drip loops, lightning protection/grounding.

## Verify
- [ ] Post-install validation survey shows design RSSI/SNR at working height, including directly below and between APs.
