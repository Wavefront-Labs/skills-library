---
id: computing-software.systems-network-administration.network-design.media-converters
name: media-converters
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, media-converter, fiber-to-copper, link-fault-pass-through, transceivers]
level: practitioner
status: draft
description: "Use fibre-to-copper media converters properly: when they are justified, speed/duplex and SFP matching, link fault pass-through, power and managed vs unmanaged units."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/10561-3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Media converters

## When to use one
- Extend copper beyond 100 m (camera on a pole, remote building) without a switch.
- Connect a copper-only device (PLC, old firewall) to a fibre backbone.
- Temporary bridge during migrations.
Prefer a small switch with SFP uplink where you also need management, PoE or redundancy.

## Matching
- Fibre type and wavelength must match the far end (MM 850 nm vs SM 1310 nm, LC vs SC, BiDi pairs).
- Speed: 100BASE-FX converters do not talk to 1000BASE-X ports. Gigabit converters with fixed
  1000BASE-X will not autonegotiate down.
- Duplex: copper side autonegotiates with the device; hard-coded duplex on the device often
  produces a mismatch because the converter expects autoneg.
- SFP-slot converters: the SFP must be supported by the converter (some are coded).

## Link fault pass-through (LFP / LLCF)
Without it, when the fibre breaks the copper side stays up, so the switch/router never sees the
link down and keeps sending traffic (no failover, no alert). Enable LFP/LLCF (DIP switch) on both
units so a failure on either side drops the other.

## Power and environment
External wall-wart PSUs are the usual failure point; use chassis-mounted converters with
redundant PSUs in racks, industrial DIN-rail units (wide temp, 12-48 VDC) in cabinets.

## Troubleshooting
LEDs per side (link/act, FDX); swap the fibre pair (Tx/Rx crossed); check optical power on the
switch side; try a known-good converter pair.

## Verify
- [ ] Unplugging the fibre drops the copper link on both ends (LFP works), and monitoring alarms.
