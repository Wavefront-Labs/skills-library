---
id: computing-software.systems-network-administration.cisco-networking.etherchannel-load-balancing-hash
name: etherchannel-load-balancing-hash
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, etherchannel, port-channel, lacp, etherchannel-load-balance, port-channel-hash, port-channel-load-balance, src-dst-ip, src-dst-mixed-ip-port, test-etherchannel-load-balance, uneven-utilisation]
level: practitioner
status: docs-checked
description: "Choose and verify the EtherChannel load-balance method on Catalyst: the 9300 options and default, why a flow stays on one member, and why 3, 5, 6 or 7 members share unevenly."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/12023-4.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9300_cg/configuring_etherchannels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EtherChannel load-balancing method

EtherChannel reduces part of the binary pattern of the frame's addresses (and, with some methods, L4 ports) to a number that selects one member link. The Cisco hash is deterministic: the same addresses and session information always select the same port, which prevents out-of-order delivery. You cannot control which port a given flow uses; you can only influence balance by choosing a method that gives the greatest variety of values.

## See and set (Catalyst 9300, IOS XE 17.9)
```
show etherchannel load-balance
port-channel load-balance src-dst-mixed-ip-port     ! global
```
- The method is global: it applies to all EtherChannels on the device.
- Keywords: `dst-ip`, `dst-mac`, `dst-mixed-ip-port`, `dst-port`, `extended`, `src-dst-ip`, `src-dst-mac`, `src-dst-mixed-ip-port`, `src-dst-port`, `src-ip`, `src-mac`, `src-mixed-ip-port`, `src-port`.
- The 9300 guide's default is `src-mac`.
- `port-channel load-balance extended {dst-ip | dst-mac | dst-port | ipv6-label | l3-proto | src-ip | src-mac | src-port}` combines fields.
- Other Catalyst families have different keyword sets (the Cisco load-balance document lists, for example, no mixed-ip-port keywords for the 3750/3560 and 4500). Check the guide for your platform.

## Choosing
Use the option that gives the greatest variety in your traffic. Examples from the Cisco documents:
- If a channel's traffic goes to a single MAC address, destination-MAC always picks the same link; source addresses or IP addresses may balance better.
- In the 9300 guide's figure, workstations talk to a router (a single-MAC device), so source-based forwarding on the switch uses all links, while the router uses destination-based forwarding because the many workstations spread traffic evenly.
- The mixed IP+port keywords add TCP/UDP ports, which helps when few IP pairs carry many sessions.

## Uneven utilisation (Catalyst 6500/6000 hash, per the Cisco load-balance document)
The hash yields a value 0 to 7 and each member accepts a share of the values:

| Members | Share ratio |
|---|---|
| 8 | 1:1:1:1:1:1:1:1 |
| 7 | 2:1:1:1:1:1:1 |
| 6 | 2:2:1:1:1:1 |
| 5 | 2:2:2:1:1 |
| 4 | 2:2:2:2 |
| 3 | 3:3:2 |
| 2 | 4:4 |

Perfect balance, even with random addresses, needs two, four or eight members. The document states this for the 6500/6000; do not assume the same ratios on every platform.

## Predict a flow's member
The Cisco load-balance document shows `test etherchannel load-balance interface port-channel <n> {ip | l4port | mac} <src> <dst>` on the Catalyst 6500 (run on the switch processor via `remote login switch`) and on the 3750/3560. It was not documented in the 9300 guide, so confirm availability on your platform.

## Gotchas
- On a Catalyst 6500, the document warns that `port-channel load-balance src-dst-mixed-ip-port` can change hardware forwarding and interrupt traffic for seconds to minutes; change the method outside production hours. This warning is for the 6500.
- The Cisco document says a hash algorithm cannot be configured or changed on the 6500; only the frame-distribution method can.

## Verify
- `show etherchannel load-balance` shows the method you set.
- Compare member interface rate counters under mixed load.

## Checked
Date: 2026-11-08. Read end to end: Cisco "Understand EtherChannel Load Balance and Redundancy on Catalyst Switches" (document 12023, updated Nov 2023) and Catalyst 9300 Layer 2 Configuration Guide 17.9.x "Configuring EtherChannels" (fetched with tools/review/fetch_pages.py). Confirmed: keyword list and default src-mac and the extended keywords (9300 guide), global scope, show etherchannel load-balance, deterministic hash and the 0-7 value / ratio table with the 2, 4, 8 members statement (document 12023, 6500 section), single-MAC destination example, router/workstation figure, test etherchannel load-balance syntax (6500 and 3750/3560 sections), 6500 mixed-ip-port warning.
Corrected: default is src-mac on the 9300, not src-dst-ip. Removed because unconfirmed: the C9500/C9600 extended claim, the routed Port-channel table row, hash polarisation and `ip cef load-sharing algorithm universal`, the per-direction/both-ends advice, the "8 buckets on most platforms" claim, `show interfaces Po1 etherchannel`, and the elephant-flow sentence.
Method: documentation only; no commands were run.
