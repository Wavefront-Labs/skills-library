---
id: computing-software.systems-network-administration.pi-hole.wireguard-route-all-traffic
name: wireguard-route-all-traffic
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [full-tunnel-vpn, wireguard-default-route, split-tunnel]
level: advanced
status: draft
description: "Send all client Internet traffic through the Pi-hole's WireGuard tunnel using AllowedIPs 0.0.0.0/0, ::/0 and avoid the no-Internet pitfall."
sources: ["https://docs.pi-hole.net/guides/vpn/wireguard/route-everything/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Route all traffic through WireGuard

Routing everything is optional. It helps on untrusted networks, such as open Wi-Fi, and makes your traffic exit from the server's location, which can hide your real location or reach geo-blocked content.

**Prerequisite.** IP forwarding and NAT must already be set up. If not, clients appear to have no Internet while local connections may still work, which is hard to debug.

**Client change.** In each client's `[Peer]` section:

```text
AllowedIPs = 0.0.0.0/0, ::/0
```

A full client example keeps `Address`, `DNS = 10.100.0.1`, `Endpoint = <server>:47111`, `PublicKey`, `PresharedKey` and `PersistentKeepalive = 25`.

**Important.** Change this only on clients. Do not set it in the server's `[Interface]` section; WireGuard sets up routing for the clients automatically.

**Tip.** Create a second profile with the modified `AllowedIPs` rather than editing the existing one, so you can choose DNS-only or full tunnel from your phone.

**Verify.** Use an online IP check to see that your public address is now the WireGuard server's. You can apply the change to selected clients only.

**Checklist**

1. Confirm forwarding and NAT work first.
2. Add the default routes on the client.
3. Check your public IP changed.
