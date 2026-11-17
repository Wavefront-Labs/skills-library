---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-persistent-keepalive-and-nat
name: wireguard-persistent-keepalive-and-nat
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [persistent-keepalive, nat-traversal, stateful-firewall, keepalive, roaming, nat-mapping]
level: practitioner
status: docs-checked
description: "Decide when to set PersistentKeepalive, what value to use, and how it keeps NAT and firewall mappings alive."
sources: ["https://man7.org/linux/man-pages/man8/wg.8.html", "https://www.wireguard.com/protocol/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PersistentKeepalive and NAT

WireGuard is silent when idle. A peer behind NAT or a stateful firewall that rarely sends traffic, but must be reachable at any moment, loses its mapping and cannot be contacted. `PersistentKeepalive` sends an authenticated empty packet to that peer every N seconds (1 to 65535) to keep the mapping valid. The quick start calls 25 seconds a sensible interval that works with a wide variety of firewalls, and notes that most users do not need the feature. Default is off; `0` or `off` disables.

```ini
[Peer]
PublicKey = <base64>
Endpoint = vpn.example.com:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

Set it on the peer that is behind NAT or a firewall and wants to receive incoming packets while idle. Live change: `wg set wg0 peer PUBKEY persistent-keepalive 25`.

Related protocol timers (from the protocol page): a peer that has received a packet but not sent one back within KEEPALIVE ms sends an empty packet; if it sent and heard nothing for KEEPALIVE plus REKEY_TIMEOUT ms it starts a new handshake. These are built in and distinct from the persistent option.

Verify: `wg show wg0` lists the keepalive interval for the peer.

## Checked

2026-11-03. Confirmed: PersistentKeepalive range (1 to 65535 s), 0 or off disables, default off, 25 s example, config-file and wg set forms, and the protocol keepalive timers, against the wg(8) man page, the quick start NAT section and the protocol page. Removed: the NAT-rebinding/roaming paragraph and the idle-then-ping verify procedure (not in the docs).

Method: documentation only; no commands were run.
