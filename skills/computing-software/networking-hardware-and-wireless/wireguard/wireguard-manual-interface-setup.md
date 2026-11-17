---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-manual-interface-setup
name: wireguard-manual-interface-setup
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wireguard, ip-link, wg-setconf, wg-set, manual-setup, interface-bringup, wireguard-go]
level: practitioner
status: docs-checked
description: "Create and bring up a WireGuard interface by hand with ip link, ip address and wg, without wg-quick."
sources: ["https://www.wireguard.com/quickstart/", "https://man7.org/linux/man-pages/man8/wg.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WireGuard manual interface setup

Four steps, each a separate tool:

```bash
ip link add dev wg0 type wireguard
ip address add dev wg0 192.168.2.1/24              # or: 192.168.2.1 peer 192.168.2.2 for two peers only
wg setconf wg0 /path/to/wg0.conf                   # keys and peers from a wg-format file
ip link set up dev wg0
```

Instead of a file you can set values inline:

```bash
wg set wg0 listen-port 51820 private-key /path/to/private-key \
  peer BASE64PUBKEY allowed-ips 192.168.88.0/24 endpoint 203.0.113.14:8172
```

Non-Linux users write `wireguard-go wg0` instead of the `ip link add` line.

The file given to `wg setconf` must be in wg format; wg-quick's extra keys such as `Address` or `DNS` are handled by wg-quick, and `wg-quick strip` outputs a file with them removed (see wireguard-syncconf-reload-without-disruption and wireguard-wg-quick-config-extensions).

View state with `wg show` (the default command; with no arguments it shows every WireGuard interface) and `wg showconf wg0`. The wg utility sets WireGuard-specific aspects only; addresses and routes are set with `ip address` and `ip route`.

Verify: `wg show wg0` lists the peer with the endpoint you configured.

## Checked

2026-11-03. Confirmed: The ip link / ip address / wg setconf or wg set / ip link set up sequence, the two-peer address form, wireguard-go for non-Linux, and wg show defaults against the quick start and wg(8) man page. Removed: 'also loads the kernel module', 'kernels without the module use userspace', the ip link del teardown line and the latest-handshake output wording (not on the pages).

Method: documentation only; no commands were run.
