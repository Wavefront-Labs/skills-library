---
id: computing-software.systems-network-administration.pi-hole.wireguard-server-install
name: wireguard-server-install
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [wireguard-server, wg0-conf, wireguard-ddns]
level: advanced
status: draft
description: "Install a WireGuard server beside Pi-hole: packages, keys, wg0.conf, port forwarding, dynamic DNS and service startup."
sources: ["https://docs.pi-hole.net/guides/vpn/wireguard/server/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# WireGuard server for Pi-hole

WireGuard calls every device a peer; the guide uses "server" and "client" to ease the move from OpenVPN.

**Install**

```bash
sudo apt-get install wireguard wireguard-tools
```

On a kernel older than 5.6 (`uname -r`), `wireguard-dkms` is also needed.

**Keys and config**

```bash
sudo -i
cd /etc/wireguard
umask 077
wg genkey | tee server.key | wg pubkey > server.pub
```

Create `/etc/wireguard/wg0.conf`:

```text
[Interface]
Address = 10.100.0.1/24, fd08:4711::1/64
ListenPort = 47111
```

then append the key: `echo "PrivateKey = $(cat server.key)" >> /etc/wireguard/wg0.conf`.

**Router.** If a NAT device sits in front, forward `47111/UDP` to the server. Because home public IPs change, register a dynamic DNS name with your router or a provider.

**Start**

```bash
sudo systemctl enable wg-quick@wg0.service
sudo systemctl daemon-reload
sudo systemctl start wg-quick@wg0
sudo wg
```

Errors: "Operation not supported" means the module is not loaded (try `sudo modprobe wireguard` or reboot into the updated kernel); "File exists" means overlapping IP ranges.

**Pi-hole side.** Use the "Allow only local requests" listening mode (`LOCAL`); the docs say WireGuard peers are then correctly recognized as being only one hop away.

**Checklist**

1. Generate keys with `umask 077`.
2. Forward the UDP port.
3. Check `sudo wg` shows the interface.
