---
id: computing-software.networking-hardware-and-wireless.opnsense.ipv6-troubleshooting-workflow
name: ipv6-troubleshooting-workflow
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [ipv6-troubleshooting, wan-ipv6, lan-ipv6, ping-6]
level: practitioner
status: docs-checked
description: "Two-step IPv6 debugging on OPNsense: prove WAN and default route first, then LAN RA and DHCPv6, using ping -6, netstat, packet capture and client tests."
sources: ["https://docs.opnsense.org/manual/ipv6.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPv6 troubleshooting workflow

Provide IPv6 in two steps and never debug step 2 before step 1 works.

Step 1, WAN and the firewall itself: select the IPv6 mode your ISP requires, reconfigure the WAN, then test from the firewall. Run ping -6 against an IPv6 host (Interfaces > Diagnostics > Ping works too) and check the default route with netstat -nr6 | grep default (or System > Routes > Status and search for default). If either fails you have a WAN-side configuration issue or the ISP does not support IPv6 for you.

Step 2, LAN clients: use static or tracking mode. Tracking is enabled by default and the WAN DHCPv6 sets up Router Advertisements and the DHCPv6 server automatically, including delegation to clients if the present prefix has room. In static mode, or tracking with Manual configuration, configure RAs and the DHCPv6 server from the menu; they default to off. Most endpoints need only RAs, but downstream routers benefit from DHCPv6. Some stacks such as Android phones only support SLAAC from RAs; DHCPv6 leases do not work there.

While testing, enable both DHCPv6 server and RAs, and disable one later if unneeded. Test on several clients, and use test-ipv6.com or ipv6-test.com for further diagnosis. Use Interfaces > Diagnostics > Packet Capture to see whether the expected ICMPv6 RS and RA traffic and DHCPv6 messages actually flow. Configuration examples exist for Zen UK, an IPv6 tunnel broker and generic DSL dialup.

## Checked

2026-11-03. Confirmed against the OPNsense IPv6 setup manual page, section Basic setup and troubleshooting: the two steps, the ping and default-route tests, tracking and static behaviour, the Android note, test sites, packet capture advice. Fixed: the example list now matches the page (it names no specific tunnel provider).

Method: documentation only; no commands were run.
