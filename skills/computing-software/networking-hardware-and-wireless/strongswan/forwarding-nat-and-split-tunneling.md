---
id: computing-software.networking-hardware-and-wireless.strongswan.forwarding-nat-and-split-tunneling
name: forwarding-nat-and-split-tunneling
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, forwarding, split-tunneling, nat, masquerade, ip-forward]
level: practitioner
status: docs-checked
description: "Forward roadwarrior traffic through a strongSwan gateway: sysctl forwarding, return routes, farp or NDP proxy, NAT exemption for IPsec policies, and IKEv2 split-tunneling."
sources:
  - https://docs.strongswan.org/docs/latest/howtos/forwarding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forwarding nat and split tunneling
**Enable forwarding** on Linux gateways: `sysctl net.ipv4.ip_forward=1` and `sysctl net.ipv6.conf.all.forwarding=1`. With a restrictive firewall, `updown = /usr/libexec/ipsec/_updown iptables` on the child adds forwarding rules.

**Return routes.** Every host the gateway forwards to must route replies for the virtual IPs back via the gateway.
- Virtual IPs from the LAN subnet: use the farp plugin so LAN hosts learn to reply to the gateway (dhcp plugin or a distinct slice of the LAN). For IPv6 use NDP proxying, e.g. an updown script running `ip -6 neigh add proxy` on `up-client-v6` and `ip -6 neigh del proxy` on `down-client-v6`.
- Distinct subnet or site-to-site: add routes on LAN hosts, a static route on the real default gateway, or NAT the virtual IPs to the gateway address.
- If the gateway is not the LAN default gateway, set `net.ipv4.conf.all.send_redirects=0` (and `default`).

**NAT.** Packets with a matching IPsec policy must skip NAT, otherwise SNAT or MASQUERADE changes the source and the policy no longer matches. Insert before any NAT rule:

```
iptables -t nat -I POSTROUTING -m policy --pol ipsec --dir out -j ACCEPT
```

Without existing NAT, also add a MASQUERADE rule for the virtual subnet.

**Split-tunneling (IKEv2).** Traffic selectors are narrowed: the client proposes `remote_ts = 0.0.0.0/0`, and the gateway narrows it with `local_ts = <subnets>`. Most clients propose 0.0.0.0/0, so configure the gateway; results depend on the client. strongSwan clients support narrowing; Windows needs client-side route settings or PowerShell (`Add-VpnConnectionRoute`).

## Checked
2026-11-04. Confirmed against the strongSwan Forwarding and Split-Tunneling page: sysctl settings, updown iptables, farp and NDP proxy script, send_redirects, NAT exemption rule, IKEv2 narrowing, Windows notes. Nothing removed.

Method: documentation only; no commands were run.
