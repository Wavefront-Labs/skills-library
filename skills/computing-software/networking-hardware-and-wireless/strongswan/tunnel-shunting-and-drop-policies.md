---
id: computing-software.networking-hardware-and-wireless.strongswan.tunnel-shunting-and-drop-policies
name: tunnel-shunting-and-drop-policies
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, tunnel-shunting, drop-policy, trap, traffic-leak]
level: advanced
status: docs-checked
description: "Stop traffic leaking outside strongSwan tunnels: start_action trap, IPsec drop policies via mode = drop, iptables policy match REJECT, and kernel xfrm default block."
sources:
  - https://docs.strongswan.org/docs/latest/howtos/securityRecommendations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tunnel shunting and drop policies
Linux IPsec is policy-based with no tunnel interface, so traffic with no matching IPsec policy is not processed and can leak to the LAN or WAN, for example when a site-to-site child uses `start_action = none` and firewall rules do not drop it.

**Use trap.** Set `start_action = trap` in site-to-site setups: the kernel asks charon to create a Child SA when none exists and traffic is held until it is up.

**Block private destinations** with the iptables policy match, e.g. reject RFC1918 destinations that lack an IPsec policy:

```
iptables -A FORWARD -d 10.0.0.0/8 -m policy --pol none --dir out -j REJECT
```

**Drop policies in swanctl.conf.** A child with `mode = drop` and `start_action = trap` installs a lower-priority policy that blocks unprotected traffic. The page example defines a connection `shunts` with `rekey_time = 0`, `local_addrs` and `remote_addrs` of 127.0.0.1, and a child `drop-rwv4` with `local_ts = 0.0.0.0/0` and `remote_ts` set to the roadwarrior pool subnet.

- If you NAT into the tunnel (DNAT, SNAT, MASQUERADE) adjust the drop traffic selector; the SPD and charon do not know your NAT rules.
- Dropping `0.0.0.0/0,::/0` blocks all unprotected traffic except IKE (socket-specific bypass policies), so add bypass policies for SSH or ICMP, particularly ICMPv6 for NDP.
- Enabling `policies_fwd_out` is needed for other children so forwarded traffic is not dropped.

**Kernel alternative.** `ip xfrm policy setdefault in|out|fwd block` sets a default drop per direction; bypass policies are still required.

## Checked
2026-11-04. Confirmed against the strongSwan Security Recommendations page (Tunnel Shunting): start_action = trap, iptables policy match, mode = drop example connection, NAT caveat, 0.0.0.0/0,::/0 drop and bypass needs, policies_fwd_out, ip xfrm policy setdefault. Nothing removed.

Method: documentation only; no commands were run.
