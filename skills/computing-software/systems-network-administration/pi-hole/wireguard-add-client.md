---
id: computing-software.systems-network-administration.pi-hole.wireguard-add-client
name: wireguard-add-client
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [wireguard-client, preshared-key, persistent-keepalive]
level: practitioner
status: draft
description: "Add a WireGuard client peer: keys, preshared key, server peer entry, client config, PersistentKeepalive and QR code."
sources: ["https://docs.pi-hole.net/guides/vpn/wireguard/client/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Add a WireGuard client

For each client, create keys and a pre-shared key (PSK). The PSK adds symmetric cryptography for post-quantum resistance; generate one per peer pair and do not reuse it.

```bash
sudo -i
cd /etc/wireguard
umask 077
name="client_name"
wg genkey | tee "${name}.key" | wg pubkey > "${name}.pub"
wg genpsk > "${name}.psk"
```

**Server side:** append a peer to `wg0.conf` and reload:

```text
[Peer]
PublicKey = <client public key>
PresharedKey = <client psk>
AllowedIPs = 10.100.0.2/32, fd08:4711::2/128
```

```bash
wg syncconf wg0 <(wg-quick strip wg0)
```

`syncconf` applies only differences, so existing sessions are less disturbed than a restart. Increment the client IP for every new peer; the server holds `.1`.

**Client config:**

```text
[Interface]
Address = 10.100.0.2/32, fd08:4711::2/128
DNS = 10.100.0.1
PrivateKey = <client private key>

[Peer]
AllowedIPs = 10.100.0.1/32, fd08:4711::1/128
Endpoint = <public IP or domain>:47111
PersistentKeepalive = 25
```

plus the server `PublicKey` and the `PresharedKey`. `DNS` is your Pi-hole's IP. `PersistentKeepalive = 25` keeps NAT mappings open; 0 (the default) turns it off.

Transfer the file securely, since it contains the client's private key. For phones, `qrencode -t ansiutf8` prints a QR code.

**Checklist**

1. Unique IPs and keys per client.
2. Run `sudo wg` to see the peer.
3. Test DNS from the client.
