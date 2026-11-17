---
id: computing-software.systems-network-administration.cisco-networking.lldp-timers-holdtime-reinit
name: lldp-timers-holdtime-reinit
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, lldp, lldp-timers, lldp-holdtime, lldp-reinit, lldp-med, neighbor-discovery]
level: practitioner
status: docs-checked
description: "Tune LLDP timer, holdtime and reinit on IOS/IOS XE, understand the TTL they advertise, and fix stale or missing neighbours caused by timer choices."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg/configuring_lldp__lldp_med__and_wired_location_service.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LLDP timers: timer, holdtime, reinit

## Defaults and ranges (Catalyst 9300, IOS XE 17.9)
| Setting | Default | Range | Meaning |
|---|---|---|---|
| `lldp timer` | 30 s | 5 to 65534 | sending frequency of LLDP updates |
| `lldp holdtime` | 120 s | 0 to 65535 | time a receiving device holds our information before discarding it |
| `lldp reinit` | 2 s | 2 to 5 | delay for LLDP to initialize on an interface |

```
conf t
 lldp run
 lldp timer 10
 lldp holdtime 40
 lldp reinit 2
show lldp                     ! global timers, holdtime, reinit delay
show lldp neighbors detail
show lldp traffic
```
LLDP is disabled globally by default; `lldp run` enables it.

## Choosing values
- The defaults give a holdtime of four times the timer; keep holdtime well above the timer so a
  lost frame does not age a neighbour out.
- Holdtime is what the **neighbour** uses for **your** entry. A stale neighbour on the far side
  after you unplug is governed by your holdtime, not theirs.

## Troubleshooting
- Neighbour missing: `show lldp interface Gi1/0/1`, and check `lldp transmit` and `lldp receive`
  on the interface. LLDP is automatically disabled on a tunnel port. Where CDP and LLDP both run
  and CDP negotiates power, the guide says to disable LLDP on that interface (`no lldp transmit`
  and `no lldp receive`, or `no lldp tlv-select power-management`).
- Check `show lldp traffic` for packets discarded and unrecognised TLVs.
- After a re-patch, old entries remain until holdtime expires; `clear lldp table` deletes the
  neighbour table to refresh.

## Verify
- [ ] `show lldp` shows intended timer/holdtime on all switches (template it).
- [ ] Unplug test: neighbour disappears within holdtime on the far side.

## Checked
2026-11-08. Confirmed against the Cisco Catalyst 9300 17.9 Interface and Hardware guide chapter
"Configuring LLDP, LLDP-MED, and Wired Location Service": default table, command ranges, tunnel
port and CDP power restrictions, show and clear commands. Removed unsupported claims (3-4x ratio
advice, voice VLAN negotiation speed, 802.1X blocking, "Time remaining" field). The original
config-guide URL 404s; the chapter now lives in the int_hw guide. IEEE 802.1AB page was not
used for any claim and was dropped from sources.
Method: documentation only; no commands were run.
