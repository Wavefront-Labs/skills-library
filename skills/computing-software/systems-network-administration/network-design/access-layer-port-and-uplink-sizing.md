---
id: computing-software.systems-network-administration.network-design.access-layer-port-and-uplink-sizing
name: access-layer-port-and-uplink-sizing
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, access-layer-design, uplink-oversubscription, port-density, poe-budget, campus-design]
level: practitioner
status: docs-checked
description: "Size campus access switches: port counts with growth, PoE budget, uplink speed and oversubscription ratio, stacking vs standalone, and wireless AP uplink needs."
sources:
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/HA_campus_DG/hacampusdg.html
  - https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html
  - https://www.arubanetworks.com/techdocs/VSG/docs/020-campus-design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access layer port and uplink sizing

## Port count
- Count per IDF: wall outlets actually patched, APs, cameras, phones (if separate drops), printers,
  building systems. Add a growth allowance and spare ports for troubleshooting.
- Prefer 48-port units; mix of mGig (2.5/5G) ports for Wi-Fi 6/6E/7 APs.

## PoE budget
Sum the real class of every PoE device (Cisco's campus guide cites PoE+, UPOE / 802.3bt Type 3 and UPOE+ / 802.3bt Type 4, up to 90 W per port). Size PSUs for full budget plus N+1 so a PSU failure does not shed APs/cameras. Check the switch's inline-power status output.

## Uplinks and oversubscription
Oversubscription = sum of access port speeds / sum of uplink speeds. Cisco's campus design guide says uplink ratios up to 20:1 between access and distribution and 4:1 between distribution and core have been implemented; the right ratio depends on business requirements.
- 48 x 1G users with 2 x 10G uplinks = 48:20 = 2.4:1 (fine).
- 48 x mGig 5G APs with 2 x 10G = 12:1; use 25G/40G uplinks for dense AP closets.
- Use two uplinks to two distribution switches (or a stacked/MLAG pair) in an EtherChannel/MLAG so
  both carry traffic and STP blocks nothing.

## Stack vs standalone
- Stacks: one management IP, cross-stack EtherChannel, but a stack upgrade reboots all members
  (unless ISSU/rolling supported) and stack cable faults split it.
- Standalone with L3 access: smaller failure domain, more devices to manage.
- Keep stacks to the vendor's tested size and spread uplinks across members.

## Verify
- [ ] Per IDF sheet: port count used/free, PoE budget vs PSU capacity with one PSU failed, uplink speed and ratio, and 95th percentile uplink utilisation after go-live.

## Checked

- Date: 2026-10-28
- Confirmed: Cisco campus LAN/WLAN design guide: up to 20:1 access-to-distribution and 4:1 distribution-to-core ratios implemented, mGig and PoE up to 90 W per port at the access layer, worked oversubscription examples; example ratios in the skill (2.4:1, 12:1) were checked by arithmetic.
- Removed: per-standard wattage figures, 20-30 % growth figure, stack size, the show command.
Method: documentation only; no commands were run.
