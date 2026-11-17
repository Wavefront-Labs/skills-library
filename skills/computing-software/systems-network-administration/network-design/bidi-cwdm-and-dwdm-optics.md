---
id: computing-software.systems-network-administration.network-design.bidi-cwdm-and-dwdm-optics
name: bidi-cwdm-and-dwdm-optics
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, bidi-optics, cwdm, dwdm, wdm, transceivers, fiber-capacity]
level: practitioner
status: docs-checked
description: "Use BiDi, CWDM and DWDM optics to multiply capacity on scarce fibre: wavelength grids, mux/demux, pairing BiDi ends, power budgets and common mistakes."
sources:
  - https://www.itu.int/rec/T-REC-G.694.2
  - https://www.itu.int/rec/T-REC-G.694.1
  - https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/datasheet-c78-736950.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BiDi, CWDM and DWDM optics

## BiDi (single fibre)
Transmit and receive on different wavelengths over one strand. Optics come in **pairs**: Cisco's
10G/25G BiDi parts are sold as BXU and BXD variants (for example SFP-10/25G-BXU-I and SFP-10/25G-BXD-I).
Halves fibre use; good for scarce dark fibre or single-strand carrier tails.

## CWDM (ITU-T G.694.2)
Coarse wavelength grid with wide channel spacing. Take the channel wavelengths from the standard or
the mux/demux datasheet; reach depends on the optic.

## DWDM (ITU-T G.694.1)
Dense grid with narrow channel spacing, so channels need stable (cooled) lasers; supports amplification
for long haul. Take the grid and channel plan from the standard and the vendor datasheets.

## Design steps
1. Count strands available and services needed (per site pair).
2. Pick channels and document wavelength per service on both ends.
3. Optical budget: Tx power - Rx sensitivity >= fibre loss + mux/demux insertion loss + connectors +
   splices + margin, with each figure taken from datasheets and test results.
4. Check maximum Rx power too (short links may need attenuators).
5. Order mux/demux with matching channel set and an express/upgrade port.

## Common mistakes
- Plugging an optic into the wrong mux channel port (no light).
- Pairing two BiDi optics of the same variant instead of a BXU/BXD pair.
- Ignoring dispersion limits on long links.

## Verify
- [ ] The switch's transceiver detail output: Rx power within spec for every channel with margin, and channel plan table in the documentation.

## Checked

2026-10-28: Confirmed in the Cisco transceiver datasheet: BiDi 10G/25G optics are sold as separate BXU and BXD part numbers. The ITU-T G.694.1 and G.694.2 pages returned only titles, so grid figures could not be confirmed. Removed: wavelength pairs and channel counts, 20 nm/100 GHz/50 GHz spacing, reach figures, the 1471/1491 nm example, dB loss and margin figures, EDFA and 400G ZR/ZR+ claims, and the water-peak remark. Dropped the FS blog source (no content returned).
Method: documentation only; no commands were run.
