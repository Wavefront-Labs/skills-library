---
id: computing-software.systems-network-administration.network-design.poe-standards-and-power-budget
name: poe-standards-and-power-budget
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cabling, poe, poe-budget, 802-3af, 802-3at, 802-3bt, poe-plus, upoe, power-classes, psu-sizing, lldp-power-negotiation, poe-troubleshooting, show-power-inline]
level: practitioner
status: gated
description: "Plan PoE: 802.3af/at/bt classes and power at switch vs device, budget and PSU redundancy maths, LLDP power negotiation, cable heating, checking allocations."
sources:
  - https://www.ieee802.org/3/bt/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PoE standards and power budgets

## Standards
| Standard | Name | Power at switch port (PSE) | Guaranteed at device (PD) | Pairs |
|---|---|---|---|---|
| 802.3af | PoE (Type 1) | 15.4 W | 12.95 W | 2 |
| 802.3at | PoE+ (Type 2) | 30 W | 25.5 W | 2 |
| 802.3bt Type 3 | PoE++ / UPOE class 5-6 | 60 W | 51 W | 4 |
| 802.3bt Type 4 | class 7-8 | up to 90 W | 71.3 W | 4 |
The power figures above are from memory of IEEE 802.3 (gated: unconfirmed, source is paywalled or blocked): confirm the exact values in the current IEEE 802.3 text (af/at clause 33, bt clause 145) before sizing. IEEE completed 802.3bt (4-pair) as IEEE Std 802.3bt-2018. Cable loss is why PSE power exceeds PD power. Vendor names such as UPOE map only roughly onto these types; check the vendor datasheet.

## Budget maths
1. List devices per closet with **actual max draw** (datasheet), not class maximum: e.g. Wi-Fi 6E
   AP 30 W (needs PoE+, full features may need bt), phone 6 W, camera 13 W, PTZ camera 60 W.
2. Sum per switch/stack. Compare with the switch PoE budget (depends on PSU model and count).
3. Redundancy: size the budget for the case where one PSU has failed, if you need PoE to survive a PSU failure; check your switch's PSU modes in its hardware guide.
4. Keep headroom for growth and inrush.

## Allocation behaviour
- Static class-based allocation reserves the class maximum (wasteful); LLDP/CDP power
  negotiation lets devices request exact power (e.g. AP asks for 25.5 W).
- On Cisco IOS XE, per-port power priority and static maximums exist under `power inline`; confirm exact syntax in your platform's command reference (gated: unconfirmed, source is paywalled or blocked).

## Check on Cisco
```
show power inline                          ! per port: admin/oper, power, device, class
show power inline Gi1/0/12 detail
show power inline police
show environment power all
```
A faulty oper state or an AP running in reduced-radio mode suggests insufficient power; read the exact state names in your platform's reference.

## Gotchas
- 4-pair bt power heats cable bundles: large bundles of Cat5e at 90 W exceed temperature
  limits; use Cat6A and smaller bundles (see TIA TSB-184-A).
- Non-standard passive PoE injectors (24 V) can damage standard ports and vice versa.
- Midspan injectors: count them separately; they do not appear in switch budgets.

## Verify
- [ ] Spreadsheet: per closet total draw vs budget in the redundant-PSU case, with headroom.
- [ ] `show power inline` shows APs negotiated their full power, no faulty ports.

## Checked

2026-11-02. The cited Cisco hardware guide returned 404 and the IEEE 802.3bt task-force page contains no power tables, so the figures could not be confirmed. Confirmed: the IEEE page states 802.3bt completed with approval of IEEE Std 802.3bt-2018 (27 September 2018) and covers 4-pair power. Removed: the dead Cisco source URL, the 100-W upper figure for Type 4, the 100 m remark, the redundant/combined PSU mode behaviour, StackPower pooling and the specific Cisco `power inline static max` and err-disable details. Gated: the af/at/bt power table (confirm in IEEE 802.3) and the Cisco CLI priority syntax.

Method: documentation only; no commands were run.
