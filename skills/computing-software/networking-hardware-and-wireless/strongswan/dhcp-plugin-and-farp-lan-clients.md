---
id: computing-software.networking-hardware-and-wireless.strongswan.dhcp-plugin-and-farp-lan-clients
name: dhcp-plugin-and-farp-lan-clients
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, dhcp-plugin, farp, virtual-ip, arp]
level: advanced
status: docs-checked
description: "Hand out roadwarrior virtual IPs from a DHCP server with the strongSwan dhcp plugin and answer ARP for them with farp so clients act as hosts on the gateway LAN."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/dhcp.html
  - https://docs.strongswan.org/docs/latest/plugins/farp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dhcp plugin and farp lan clients
**dhcp plugin.** Disabled by default; build with `--enable-dhcp`. It forwards IKEv2 virtual IP requests to a DHCPv4 server, using broadcasts unless a server is configured. Enable per connection with `pools = dhcp`. The DHCP request MAC is random, or derived from the client IKE identity; an FQDN identity is also sent as host name option 12.

Options in `charon.plugins.dhcp`:
- `server` (default 255.255.255.255, unicast or broadcast address)
- `interface` (interface name used for address allocation; default binds to any) and `interface_receive` (interface for the receive socket; defaults to the send socket's interface, empty string avoids binding it)
- `identity_lease` (default no: derive the MAC from an identity hash and send identity in client identifier option 61)
- `force_server_address` (default no: always use the configured server address)
- `use_server_port` (default no: bind port 67 as source when relaying to a unicast server)

If the DHCP server runs on the same host, you may need `force_server_address = yes` and the local broadcast address as `server` (for example 192.168.0.255), because some DHCP daemons do not listen on loopback.

**farp plugin.** Disabled by default; build with `--enable-farp`. The daemon answers ARP requests for addresses in the remote traffic selectors (such as virtual IPs handed to clients, or whole subnets) with its own MAC address. Together with dhcp, a roadwarrior fully acts as a client on the responder LAN. If the plugin is unavailable (older versions relied on AF/PF_PACKET sockets only), proxy ARP can be done with arp(8) in an updown script: `arp -s ${PLUTO_PEER_SOURCEIP4_1} auto pub` on `up-client` and `arp -d ${PLUTO_PEER_SOURCEIP4_1} pub` on `down-client`.

## Checked
2026-11-04. Confirmed against the dhcp and farp plugin pages: configure flags, `pools = dhcp`, all five dhcp options and defaults, the MAC and option 61 and 12 behaviour, the same-host server note, and the arp(8) updown example. Corrected the `interface` and `interface_receive` descriptions and the farp behaviour text.

Method: documentation only; no commands were run.
