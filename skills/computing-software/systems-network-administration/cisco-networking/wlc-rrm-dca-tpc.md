---
id: computing-software.systems-network-administration.cisco-networking.wlc-rrm-dca-tpc
name: wlc-rrm-dca-tpc
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-wireless, catalyst-9800, rrm, rrm-tuning, dca-tpc, dca, tpc, channel-planning, rf-management, rf-profile]
level: practitioner
status: draft
description: "Tune Catalyst 9800 RRM: DCA channel width and sensitivity, TPC min/max power, RF groups and RF profiles, and when to freeze or override automatic choices."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg/m_rrm.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/technotes/8-3/b_RRM_White_Paper.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RRM: DCA and TPC on Catalyst 9800

## Pieces
| Function | Does | Knobs |
|---|---|---|
| RF grouping | elects an RF group leader that runs RRM for neighbouring APs | RF group name, leader (auto/static) |
| DCA (Dynamic Channel Assignment) | picks channels and width per AP | interval/anchor time, sensitivity, channel list, width (20/40/80/best) |
| TPC (Transmit Power Control) | lowers/raises AP power to target neighbour RSSI | TPC threshold (default -70 dBm), min/max power |
| CHD (Coverage Hole Detection) | raises power for clients with poor SNR | |

## Configuration (GUI: Configuration > Radio Configurations > RRM)
```
ap dot11 5ghz rrm channel dca interval 24 anchor-time 2    ! once a day at 02:00
ap dot11 5ghz rrm channel dca sensitivity medium
ap dot11 5ghz rrm channel dca chan-width best
ap dot11 5ghz rrm channel dca remove 120 124 128            ! drop DFS/weather radar channels if needed
ap dot11 5ghz rrm txpower min 8
ap dot11 5ghz rrm txpower max 17
ap dot11 5ghz rrm tpc-threshold -67
show ap dot11 5ghz channel
show ap dot11 5ghz txpower
show ap dot11 5ghz summary
```
Use **RF profiles** (attached via RF tag) to give a high-density hall different power/channel
rules from offices.

## Practice
- DCA interval: run daily in an off-hours anchor time; the default 10-minute interval causes
  client disruption from channel changes.
- 5 GHz width: 20/40 MHz in high density; 80 MHz only with few APs and clean spectrum. 2.4 GHz: 1/6/11 only.
- Limit max power so APs do not out-shout client radios (asymmetric links); 2.4 GHz usually
  several dB lower than 5 GHz.
- After a big change (new APs) run `ap dot11 5ghz rrm channel-update` once rather than waiting.
- Check DFS events (`show ap auto-rf dot11 5ghz`); radar hits move APs off channel for 30 min.

## Verify
- [ ] No two adjacent APs on the same 5 GHz channel (`show ap auto-rf dot11 5ghz` neighbours).
- [ ] Power levels not pinned at max across the floor (sign of too few APs or wrong threshold).
