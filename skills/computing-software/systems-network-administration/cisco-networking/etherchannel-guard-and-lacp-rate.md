---
id: computing-software.systems-network-administration.cisco-networking.etherchannel-guard-and-lacp-rate
name: etherchannel-guard-and-lacp-rate
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, etherchannel, lacp, lacp-rate-fast, lacp-rate, max-bundle, min-links, lacp-port-priority, lacp-system-priority, standalone-disable, hot-standby]
level: advanced
status: docs-checked
description: "Tune LACP on Catalyst 9300 (IOS XE 17.9): lacp rate fast, max-bundle with hot standby, min-links, system and port priority, and the standalone-disable setting for server links."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_etherchannels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LACP tuning on Catalyst

Commands below are from the Catalyst 9300 Layer 2 Configuration Guide, IOS XE 17.9.x, chapter "Configuring EtherChannels". Check your platform and release before relying on them.

## LACP rate
`lacp rate` sets the rate at which LACP control packets are received on an LACP interface. The default is normal (30 seconds); fast is 1 second. It is supported only on LACP-enabled interfaces. `no lacp rate` resets it.
```
interface range Te1/0/1 - 2
 lacp rate fast
```
Verify with `show lacp internal` (the Flags column shows `F` for a port requesting fast LACPDUs, `S` for slow, `A` active, `P` passive) and `show lacp counters`.

## Max-bundle, hot standby and min-links
```
interface Port-channel1
 lacp max-bundle 4          ! range 1-8; remaining ports become hot-standby
 port-channel min-links 2   ! range 2-8
lacp system-priority 100    ! global; range 1-65535, default 32768, lower = higher priority
interface Te1/0/5
 lacp port-priority 100     ! range 1-65535, default 32768, lower = more likely used
```
- By default LACP tries to bundle up to 16 compatible ports; only eight are active and the rest are hot-standby. `lacp max-bundle` lowers the number of active ports; the rest become hot-standby (example in the guide: five ports with a max-bundle of three leaves two hot-standby).
- The system with the numerically lower system priority and system ID decides which ports are active; it then uses its own port priority and port number. The other system's port values are not used.
- `min-links` keeps a port channel from coming up (and takes it down) when fewer than the configured number of member ports are up and bundled.
- `show etherchannel summary` marks hot-standby ports with the `H` flag.

## Standalone-disable on server links
The guide states that with CSCtn96950 standalone mode is enabled by default and that ports are moved to suspended state when no response is received from an LACP peer. The guide's `port-channel standalone-disable` (on the Port-channel interface) disables the standalone member-port state. Its AP example (to avoid PoE or LACP negotiation errors) configures the Port-channel side with `switchport nonegotiate`, `no port-channel standalone-disable` and `spanning-tree portfast`. Read the guide section for the release you run before choosing, and test a PXE boot on the actual platform.

## Verify
- `show lacp internal` and `show lacp counters` after changing the rate.
- `show etherchannel summary` for `H` (hot-standby) members.
- Test min-links by shutting members in a change window.

## Checked
Date: 2026-11-08. Read end to end: Cisco Catalyst 9300 Layer 2 Configuration Guide 17.9.x, "Configuring EtherChannels" (fetched with tools/review/fetch_pages.py, since plain curl is blocked). Confirmed: lacp rate {normal | fast} (30 s default, 1 s fast, LACP interfaces only); lacp max-bundle (range 1 to 8, hot-standby behaviour); port-channel min-links (range 2 to 8); lacp system-priority and lacp port-priority (range 1 to 65535, default 32768); active/standby election by lower system priority and system ID; 16-port bundle with 8 active; the H flag in show etherchannel summary; F/S/A/P flags in show lacp internal; standalone-disable text and the AP example.
Removed because the page does not confirm them: the 90 s and 3 s timeout figures, the `spanning-tree etherchannel guard misconfig` section and its `channel-misconfig` err-disable claim, the Nexus `lacp suspend-individual` lines, the claim that the default allows individual ports, the MAC-flap claim, `show lacp neighbor detail`, and the `FA`/`SA` attribution to show lacp neighbor (the guide shows those flags in show lacp internal). The second source (Cisco document 12023) covers load balancing only and was dropped from sources.
Method: documentation only; no commands were run.
