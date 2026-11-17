---
id: computing-software.systems-network-administration.network-design.dac-aoc-and-breakout-cables
name: dac-aoc-and-breakout-cables
category: computing-software
field: systems-network-administration
product: network-design
tags: [transceivers, dac, aoc, breakout-cable, qsfp, sfp28, twinax, data-centre-cabling]
level: practitioner
status: docs-checked
description: "Choose and deploy DAC, AOC and breakout cables: passive vs active reach, breakout ports, FEC settings, and compatibility checks."
sources:
  - https://www.cisco.com/c/en/us/products/collateral/interfaces-modules/transceiver-modules/datasheet-c78-736950.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAC, AOC and breakout cables

## Options inside a rack or row
| Type | Reach | Notes |
|---|---|---|
| Passive DAC (twinax copper) | short; Cisco lists its 25G SFP28 passive cables in 1 to 5 m lengths | cheapest, lowest power and latency, thick and stiff |
| Active DAC (ACC/AEC) | longer than passive; see the vendor datasheet | electronics in the connector |
| AOC (active optical) | Cisco lists its 25G SFP28 AOCs in 1 to 10 m lengths | thin, light; fixed length, whole cable replaced on failure |
| Optics + fibre | anything | flexible, patchable, most expensive |

Rule of thumb: DAC top-of-rack to servers, AOC across racks in a row, optics + structured fibre
beyond.

## Breakout
Breakout cables (or MPO-to-LC fan-outs with optics) split one high-speed port into several lower-speed
ports. Which ports can break out, into what, and the configuration syntax are platform specific and
some ports cannot break out at all: take them from the switch's hardware and configuration guide.

## FEC and auto-negotiation
Host-port FEC must match what the cable needs; a mismatch can leave the link down with no obvious error.
Cisco's 25G SFP28 datasheet lists, for its passive copper cables, no FEC for 1, 1.5 and 2 m, BASE-R
(FC-FEC) for 2.5 and 3 m, and RS-FEC for 4 and 5 m; its AOCs need BASE-R or RS-FEC on the host ports.
Check the datasheet of the cable you buy, and set both ends explicitly when a link will not come up.

## Compatibility
- Switches may reject cables or optics that are not coded for them; buy coded for the switch end.
- Check the vendor compatibility matrix for cable, switch and software release.
- A DAC longer than its rated length can work in the lab and fail with CRC errors later.

## Verify
- [ ] The switch's transceiver and interface status show the expected cable type and speed;
  CRC counters stay at zero under load.

## Checked

2026-10-28: Confirmed against the Cisco 25G SFP28 DAC/AOC datasheet (datasheet-c78-736950): passive cable lengths of 1 to 5 m, AOC lengths of 1 to 10 m, and the FEC requirement by cable length. Removed: reach figures for active DAC and long AOCs, lane-count arithmetic, per-vendor breakout and FEC configuration examples, the unsupported-transceiver remark and the compatibility-matrix product name, none of which a fetched page supported. Replaced the dead datasheet source URL.
Method: documentation only; no commands were run.
