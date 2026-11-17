---
id: computing-software.networking-hardware-and-wireless.opnsense.interface-advanced-settings-offloading
name: interface-advanced-settings-offloading
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [hardware-offload, tso, lro, vlan-hardware-filtering, interfaces-settings]
level: practitioner
status: docs-checked
description: "Interfaces > Settings on OPNsense: CRC, TSO, LRO offload, VLAN hardware filtering, ARP logging, Turn off IPv6, DHCPv6 release, log level and DUID."
sources: ["https://docs.opnsense.org/manual/interfaces_settings.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Interfaces > Settings

Changes here apply after a reboot or reconfiguration of each interface; leave defaults unless you have a reason.

- Hardware CRC: "Disable hardware checksum offloading" is checked by default. Offloaded checksums do not work with some technologies (IPS) and some drivers are buggy; the gain is debatable. Related ifconfig flags: txcsum, rxcsum, txcsum6, rxcsum6.
- Hardware TSO: disables TCP segmentation offload, checked by default; incompatible with IPS and broken on some NICs (tso, tso4, tso6).
- Hardware LRO: disables large receive offload, checked by default. For routing, avoid options that queue traffic on the card since that adds latency, and LRO may hurt forwarding or be incompatible with it (lro).
- VLAN Hardware Filtering: keep "Disable VLAN Hardware Filtering", the default since 20.7; forcing a driver mode led to random disconnects before.
- ARP Handling: by default the kernel logs IP address movement between MACs and ARP requests on the wrong interface (log_arp_movements, log_arp_wrong_iface). Checking the option stops that, useful when several interfaces share a broadcast domain.
- Turn off IPv6: ignore IPv6 configuration and generate a floating rule blocking all transit IPv6 traffic.
- Prevent release: do not send a DHCPv6 release on client exit, keeping the allocated address or prefix.
- Log level: info shows status, leases and addresses; debug gives full diagnostics for IPv6 clients.
- DHCP Unique Identifier: set an explicit DUID (types in RFC 8415 section 11); otherwise dhcp6c assigns one automatically.

## Checked

2026-11-03. Confirmed against the OPNsense Interfaces Settings manual page: each option, its default, the ifconfig flag names and the 20.7 VLAN hardware filtering default. Nothing removed.

Method: documentation only; no commands were run.
