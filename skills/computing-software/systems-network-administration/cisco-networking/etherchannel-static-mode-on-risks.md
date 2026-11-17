---
id: computing-software.systems-network-administration.cisco-networking.etherchannel-static-mode-on-risks
name: etherchannel-static-mode-on-risks
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, etherchannel, etherchannel-mode-on, static-lag, lacp, loop, port-channel]
level: practitioner
status: docs-checked
description: "What EtherChannel mode on does on Catalyst 9300 (no negotiation), what the guide warns about misconfiguration, when on is needed, and how to move a bundle to LACP."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_etherchannels.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/12023-4.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static EtherChannel (mode on) and its risks

Source: Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, "Configuring EtherChannels".

## What mode on does
`channel-group N mode on` forces the port to channel without PAgP or LACP. The guide says:
- A usable EtherChannel exists only when the devices at both ends of the link are configured in the on mode.
- Ports in on mode in the same channel group must have compatible characteristics such as speed and duplex; incompatible ports are suspended even in on mode.
- Caution from the guide: it is a manual configuration, ports on both ends must have the same configuration, and if the group is misconfigured, packet loss or spanning-tree loops can occur.
- Ports in on mode do not exchange PAgP packets, and PAgP and LACP groups cannot interoperate with each other.

## When on is used
The guide says on mode "can be useful if the remote device does not support PAgP or LACP". The Cisco load-balance document (12023) adds that if the device on one side does not support PAgP, such as a router, the other side must be set to on for a channel to form, and that only auto-desirable, desirable-desirable and on-on combinations form a PAgP-era channel.

## Moving to LACP
Because an on-mode channel exists only when both ends are on, and LACP ports need an LACP partner (active with active or passive), change both ends in the same maintenance window:
```
interface range Gi1/0/1-4
 no channel-group 1
 channel-group 1 mode active
```
Syntax from the guide: `channel-group channel-group-number mode {auto [non-silent] | desirable [non-silent] | on} | {active | passive}`. Expect the bundle to be down while the two ends differ.

## Verify
```
show etherchannel summary
show lacp neighbor
```
Flags in the guide's sample output: `P` bundled in port-channel, `I` stand-alone, `s` suspended, `H` hot-standby, `w` waiting to be aggregated, `D` down. The Protocol column shows LACP once migrated.

## Checked
Date: 2026-11-08. Read end to end: Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring EtherChannels" (fetched via tools/review/fetch_pages.py): "EtherChannel On Mode" section and caution, channel-group mode keywords step, active/passive mode rules, the summary flag legend in the Auto-LAG examples, and the list of show commands. The Cisco 12023 document's PAgP section was re-read for the "on-on" statement.
Removed because the sources do not confirm them: the scenarios of blackholed flows toward two unrelated switches, unidirectional links staying in the bundle, BPDU-filtering loops, the misconfig-guard sentence, the VMware "Route based on IP hash" example, the storm-control and BPDU guard advice, the shut-all-but-one migration procedure, and `show etherchannel 1 detail | include Protocol`. Document 12023 was added to sources for the on-on statement.
Method: documentation only; no commands were run.
