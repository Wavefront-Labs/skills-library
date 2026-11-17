---
id: computing-software.systems-network-administration.pi-hole.wireguard-access-internal-devices
name: wireguard-access-internal-devices
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [wireguard-nat, ip-forwarding, wireguard-allowedips]
level: advanced
status: draft
description: "Let WireGuard clients reach the LAN: enable IP forwarding, add NAT masquerade rules and extend AllowedIPs."
sources: ["https://docs.pi-hole.net/guides/vpn/wireguard/internal/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# WireGuard access to internal devices

By default, clients can reach only the server. To reach other LAN devices:

**1. Enable IP forwarding** in `/etc/sysctl.d/99-sysctl.conf`:

```text
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```

then `sudo sysctl --system`. A firewall is highly recommended for any Internet-facing device.

**2. Enable NAT** with `PostUp` and `PostDown` lines in the server's `[Interface]` section. With nftables, the guide adds a `wireguard` table with a postrouting chain and a masquerade rule, and deletes the tables in `PostDown`. On older distributions use iptables:

```text
PostUp = iptables -w -t nat -A POSTROUTING -o eth0 -j MASQUERADE; ip6tables -w -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -w -t nat -D POSTROUTING -o eth0 -j MASQUERADE; ip6tables -w -t nat -D POSTROUTING -o eth0 -j MASQUERADE
```

Replace `eth0` with your Internet-facing interface (check `ip a`); the nftables method needs no interface name.

**3. Extend client AllowedIPs** with the LAN range in CIDR notation:

```text
[Peer]
AllowedIPs = 10.100.0.0/24, fd08:4711::/64, 192.168.2.0/24
```

Do this only for the clients that should have LAN access; others stay isolated to the Pi-hole server.

**Checklist**

1. Enable forwarding and apply sysctl.
2. Add NAT lines with the correct interface.
3. Edit client AllowedIPs and reconnect.
