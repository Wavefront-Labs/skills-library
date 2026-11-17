---
id: computing-software.networking-hardware-and-wireless.opnsense.ips-interface-and-capture-mode
name: ips-interface-and-capture-mode
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [ids, ips, suricata, netmap, home-net]
level: advanced
status: docs-checked
description: "Pick interfaces and capture mode for OPNsense Suricata IDS/IPS: PCAP, Netmap, Divert, HOME_NET behind NAT, netmap tunable and offloading."
sources: ["https://docs.opnsense.org/manual/ips.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IDS/IPS interface and capture mode

OPNsense's IPS is Suricata with Netmap for speed. IDS alerts on suspicious patterns; IPS also drops matching packets. Choose the interface carefully: capturing on WAN with IPv4 NAT shows only translated traffic, so alerts point at the firewall rather than the internal machine, and rules rely on knowing the home network. Rules use $HOME_NET (configurable, usually RFC 1918) and $EXTERNAL_NET (everything else), so marking all traffic as home would match nothing. Because the firewall already drops unsolicited inbound traffic, IPS on WAN adds little. Usually protect LAN-side interfaces.

Services > Intrusion Detection > Administration > Settings:
- Enabled.
- Capture mode: PCAP live mode (IDS) alerts only; Netmap (IPS) alerts and drops via the netmap driver; Divert (IPS) redirects via firewall rules containing a Divert-to setting. Drops need the rule action to be drop, set per rule or by policy.
- Listeners (Divert): normally the CPU count.
- Promiscuous mode, Enable syslog alerts (fast log), Enable eve syslog output (info level; drop logs stay in the internal logger), Pattern matcher (Aho-Corasick default, Hyperscan best when available, else Aho-Corasick Ken Steele variant), Interfaces (in IPS mode real netmap-capable interfaces; with VLANs enable on the parent), Rotate log and Save logs.

Advanced toggle: Home networks (set when different from RFC 1918, e.g. IDPS on a WAN behind NAT) and default packet size (larger packets still process but slower).

In IPS mode disable all hardware offloading in Interfaces > Settings. If a NIC lacks native netmap support, set tunable dev.netmap.admode to 2 for emulated mode. IDS mode works on nearly all adapters.

## Checked

2026-11-03. Confirmed against the OPNsense Intrusion Prevention System manual page: interface choice and NAT, HOME_NET and EXTERNAL_NET, capture modes, every general and advanced option, offloading, and dev.netmap.admode value 2. Nothing removed.

Method: documentation only; no commands were run.
