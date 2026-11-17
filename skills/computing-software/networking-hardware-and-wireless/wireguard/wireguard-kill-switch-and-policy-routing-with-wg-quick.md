---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-kill-switch-and-policy-routing-with-wg-quick
name: wireguard-kill-switch-and-policy-routing-with-wg-quick
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [kill-switch, iptables, policy-routing, ip-rule, postup, predown, fwmark, split-tunnel]
level: advanced
status: docs-checked
description: "Add an iptables kill-switch or per-port policy routing to a wg-quick config using fwmark, Table, PostUp and PreDown."
sources: ["https://man7.org/linux/man-pages/man8/wg-quick.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kill-switch and policy routing with wg-quick

Kill-switch for a full-tunnel client (a peer with `AllowedIPs = 0.0.0.0/0`): add to `[Interface]`

```
PostUp = iptables -I OUTPUT ! -o %i -m mark ! --mark $(wg show %i fwmark) -m addrtype ! --dst-type LOCAL -j REJECT
PreDown = iptables -D OUTPUT ! -o %i -m mark ! --mark $(wg show %i fwmark) -m addrtype ! --dst-type LOCAL -j REJECT
```

It works with the fwmark wg-quick sets on WireGuard's own UDP socket: anything leaving by another interface without that mark is rejected, so no cleartext leaks if the tunnel drops. DHCP mostly keeps working because most clients use PF_PACKET sockets that bypass Netfilter. For IPv6 add equivalent `ip6tables` lines.

Policy routing example: send only SSH (TCP port 22) through the tunnel.

```
[Interface]
Address = 10.192.122.1/24
PrivateKey = <base64>
Table = 1234
PostUp = ip rule add ipproto tcp dport 22 table 1234
PreDown = ip rule delete ipproto tcp dport 22 table 1234

[Peer]
PublicKey = <base64>
AllowedIPs = 0.0.0.0/0
```

`Table = 1234` puts the peer routes in table 1234 instead of main, and the `ip rule` steers matching traffic to it. `Table = off` disables route creation entirely when you manage routing yourself.

Keep private keys out of the file with `PreUp = wg set %i private-key <(pass WireGuard/private-keys/%i)`.

Verify: `iptables -S OUTPUT` shows the REJECT rule while the interface is up and no longer shows it after `wg-quick down`.

## Checked

2026-11-03. Confirmed: Kill-switch PostUp/PreDown iptables lines, fwmark interplay, DHCP/PF_PACKET note, ip6tables remark, the Table/PostUp/PreDown SSH policy-routing example, Table=off and the pass PreUp example against the wg-quick(8) man page.

Method: documentation only; no commands were run.
