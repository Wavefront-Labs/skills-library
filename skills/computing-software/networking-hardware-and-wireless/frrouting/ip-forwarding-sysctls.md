---
id: computing-software.networking-hardware-and-wireless.frrouting.ip-forwarding-sysctls
name: ip-forwarding-sysctls
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, sysctl, ip-forward, ipv6-forwarding, arp, ndisc, linux-kernel]
level: practitioner
status: docs-checked
description: "Kernel sysctls FRR expects on Linux for IPv4 and IPv6 forwarding, address retention and ARP or ND behaviour, plus the show commands that report forwarding state."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
  - https://docs.frrouting.org/en/latest/vrrp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP forwarding sysctls
Check state with `show ip forward` and `show ipv6 forward`.

Expected:
- `net.ipv4.ip_forward=1` global IPv4 forwarding.
- `net.ipv4.conf.{all,default,<interface>}.forwarding=1` per-interface IPv4 (checked on the ingress interface).
- `net.ipv6.conf.{all,default,<interface>}.forwarding=1` per-interface IPv6.
- `net.ipv6.conf.all.keep_addr_on_down=1` keeps IPv6 addresses when an interface goes down.
- `net.ipv6.route.skip_notify_on_dev_down=1` suppresses netlink notifications for routes removed when a device goes down.

Optional:
- `...bc_forwarding=0`; set to 1 to route directed broadcast packets.
- `...arp_accept=1`; set to 0 to avoid creating new ARP entries from gratuitous ARP.
- `...arp_ignore=0` ARP reply policy (0 any local, 1 same interface, 2 same interface and subnet).
- `...arp_notify=1` sends gratuitous ARP on interface up.
- `net.ipv6.conf.{all,default,<interface>}.ndisc_notify=1` sends an unsolicited neighbor advertisement on interface up.

Useful: `net.ipv6.conf.all.use_oif_addrs_only=1` restricts the candidate source addresses for destinations routed via an interface to the addresses configured on that interface (RFC 6724 section 4).

The VRRP page suggests `net.ipv4.conf.eth0.ignore_routes_with_linkdown=1` when a master router is not forwarding traffic.

## Checked

2026-11-08. Read the sysctl section and show ip forward commands of the FRR zebra page, and the VRRP troubleshooting section. Reworded the use_oif_addrs_only and VRRP lines to what the pages say.
Method: docs-only read of cited pages, 2026-11-08
