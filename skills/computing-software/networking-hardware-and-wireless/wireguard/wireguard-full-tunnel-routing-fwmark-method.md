---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-full-tunnel-routing-fwmark-method
name: wireguard-full-tunnel-routing-fwmark-method
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [default-route, fwmark, suppress-prefixlength, ip-rule, routing-loop, full-tunnel, endpoint-exemption]
level: advanced
status: docs-checked
description: "Route all traffic through WireGuard without a routing loop: compare default-route tricks with the fwmark rule method."
sources: ["https://www.wireguard.com/netns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Routing all traffic through WireGuard

The endpoint's own UDP packets must not go into the tunnel. Classic solutions, in order of improvement:

1. Replace the default route and add a host route for the endpoint:
   `ip route del default; ip route add default dev wg0; ip route add 203.0.113.9/32 via 192.168.1.1 dev eth0`. DHCP daemons tend to undo it.
2. Override instead of replace with two more specific routes: `ip route add 0.0.0.0/1 dev wg0` and `ip route add 128.0.0.0/1 dev wg0`, plus the endpoint host route. The endpoint route is forgotten when eth0 flaps.
3. Rule-based routing: `ip rule add to 203.0.113.9 lookup main pref 30`, `ip rule add to all lookup 80 pref 40`, `ip route add default dev wg0 table 80`. Endpoint rules go stale when the endpoint roams and are not cleaned up.
4. fwmark method (what wg-quick uses):

```bash
wg set wg0 fwmark 1234
ip route add default dev wg0 table 2468
ip rule add not fwmark 1234 table 2468
ip rule add table main suppress_prefixlength 0
```

All packets from WireGuard's socket carry mark 1234 and skip table 2468. Everything else uses table 2468 (the tunnel). The `suppress_prefixlength 0` rule lets traffic match more specific local routes in the main table (non-default routes), so the LAN stays reachable.

The authors want a kernel `notoif` feature to avoid the loop natively; the page says it had not been merged.

Verify: `ip rule` shows the `not fwmark 1234` rule and the `suppress_prefixlength 0` rule.

## Checked

2026-11-03. Confirmed: All four routing techniques, their listed drawbacks, the fwmark commands and explanation, and the notoif note against the WireGuard routing and network namespaces page (the page uses its own demo endpoint address; the skill uses a documentation-range address). Removed: the 'repeat with -6 for IPv6' instruction (not on the page) and the IP-echo verify.

Method: documentation only; no commands were run.
