---
id: computing-software.systems-network-administration.cisco-networking.etherchannel-troubleshooting
name: etherchannel-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, etherchannel, port-channel, lacp, etherchannel-troubleshooting, suspended-member, stand-alone, show-etherchannel-summary, show-lacp, member-mismatch]
level: practitioner
status: docs-checked
description: "Fix Catalyst 9300 EtherChannel bundles that will not form: read the summary flags, use the mode combinations that bundle, match member settings and check LACP with show lacp."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_etherchannels.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/12023-4.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EtherChannel troubleshooting

Based on the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring EtherChannels".

## Read the summary
```
show etherchannel summary
```
Flag legend from the guide's sample output:

| Flag | Meaning |
|---|---|
| P | bundled in port-channel |
| I | stand-alone |
| s | suspended |
| D | down |
| H | hot-standby (LACP only) |
| w | waiting to be aggregated |
| u | unsuitable for bundling |
| M | not in use, minimum links not met |
| f | failed to allocate aggregator |
| R / S | Layer 3 / Layer 2 |
| U | in use |
| A | formed by Auto LAG |

So `Po1(SU)` is a Layer 2 port channel in use.

Why ports are suspended, per the guide:
- A port-mode or VLAN mask misconfiguration is detected.
- Ports configured in `on` mode with incompatible characteristics (speed, duplex).
- No response from an LACP peer: the guide says standalone mode is enabled by default and ports then move to suspended state.

## Mode combinations
| Side A | Side B | Result |
|---|---|---|
| active | active or passive | bundles |
| passive | passive | never bundles (neither side starts negotiation) |
| desirable (PAgP) | desirable or auto | bundles |
| auto | auto | never bundles |
| on | on | bundles without negotiation |
| LACP | PAgP | cannot interoperate |

Ports in `on` mode exchange no PAgP packets and a usable on-mode channel exists only when both ends are on.

## Members must match
Per the guide:
- Same speed and duplex on all ports.
- Layer 2: all ports in the same VLAN or all trunks; ports with different native VLANs cannot form a channel; the allowed VLAN range must be identical on trunks, or the ports do not bundle even in PAgP auto or desirable mode.
- A port must not be in more than one channel group, and a channel group must not mix PAgP and LACP.
- Different spanning-tree path costs do not by themselves prevent bundling.
- A port that is an active or not-yet-active EtherChannel member cannot be an IEEE 802.1x port; enabling 802.1x there gives an error message.
- A port shut down with `shutdown` is treated as a link failure and traffic moves to the remaining ports.
- Changes on the port-channel interface apply to all physical members; changes on a physical port affect only that port.
- Layer 3: put the IP address on the port-channel interface, not the members.

```
show running-config interface Gi1/0/1
show etherchannel detail
```

## LACP checks
```
show lacp neighbor
show lacp sys-id
show lacp counters
show lacp internal
```
These are the `show lacp [channel-group-number] {counters | internal | neighbor | sys-id}` forms in the guide's monitoring table. Use them to compare partner details per member and LACPDU counters.

## Verify
- All members show `P` in `show etherchannel summary`, and the port channel shows `SU` (Layer 2) or `RU` (Layer 3).
- `show lacp neighbor` returns the partner for each member.

## Checked
Date: 2026-11-08. Read end to end: Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring EtherChannels" (fetched via tools/review/fetch_pages.py): Restrictions, PAgP/LACP mode tables and compatibility rules, EtherChannel On Mode, Layer 2 guidelines, Configuration Guidelines, Auto-LAG flag legend, Monitoring table. Cisco document 12023 was read (PAgP section: only auto-desirable, desirable-desirable and on-on form a channel).
Removed or corrected: the description of `I` as "forwards on its own" and `s` as "wrong partner" (the guide says suspended for mode/VLAN misconfiguration, incompatible on-mode ports, or no LACP peer response), MTU, STP port settings and port-security as member match conditions, `show interfaces Gi1/0/2 etherchannel`, the `| i` filter on show etherchannel detail, `default interface` re-add advice, SA/FA flags for show lacp neighbor, the "different partner system IDs means two switches" and "LACPDUs sent but none received" diagnoses, and the whole EtherChannel guard / `%PM-4-ERR_DISABLE: channel-misconfig` section (not on either page).
Method: documentation only; no commands were run.
