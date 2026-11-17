---
id: computing-software.systems-network-administration.pi-hole.router-dhcp-dns-opnsense-usg
name: router-dhcp-dns-opnsense-usg
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [opnsense-pihole, ubiquiti-usg-pihole, router-dns-method]
level: practitioner
status: draft
description: "Make a router hand out Pi-hole as DNS through DHCP, or forward its own DNS to Pi-hole, on OPNsense and Ubiquiti USG."
sources: ["https://docs.pi-hole.net/routers/OPNsense/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pointing a router at Pi-hole

First get the Pi-hole's addresses: `ifconfig eth0` (use your interface) shows the `inet` address and the `inet6` address starting with `fe` (link-local). Use these as the DNS servers.

**Method 1: distribute Pi-hole by DHCP.** Path: Clients, then Pi-hole, then upstream.

- OPNsense: Services, ISC DHCPv4, select the interface, put the Pi-hole IPv4 in the first DNS servers line. For IPv6 allow manual adjustment of DHCPv6 and Router Advertisements under the interface, then Services, Router Advertisement, DNS servers. Link-local IPv6 is not reachable from other VLANs.
- Ubiquiti USG (UniFi Network): Settings, Networks, the network, DHCP section, "Show options", enable DHCP DNS Server and enter the IPv4; under IPv6 DHCPv6/RDNSS DNS Control uncheck Auto and enter the IPv6.

**Method 2: router forwards to Pi-hole.** Path: Clients, router, Pi-hole, upstream.

- OPNsense: Settings, General, Networking, add the Pi-hole under DNS Servers and uncheck "Allow DNS server list to be overridden by DHCP/PPP on WAN".
- USG: Settings, Internet, the WAN, Advanced, uncheck Auto and add the Pi-hole IPv4.

**Resolver loop.** If your router's IP is also a Pi-hole upstream, method 2 creates a resolver loop. Keep another external upstream, or use Unbound.

If clients are slow to update, toggle Wi-Fi or reconnect the cable.

**Checklist**

1. Pick method 1 or 2.
2. Set IPv4 and IPv6 addresses.
3. Confirm the loop warning is not triggered.
