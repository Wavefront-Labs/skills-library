---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-debugging-and-logging
name: wireguard-debugging-and-logging
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [dynamic-debug, dmesg, log-level, wg-debug, ifconfig-debug, troubleshooting, wireguard-module]
level: practitioner
status: docs-checked
description: "Turn on WireGuard debug output for the Linux kernel module, BSD interfaces and userspace implementations."
sources: ["https://man7.org/linux/man-pages/man8/wg.8.html", "https://www.wireguard.com/quickstart/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging WireGuard

Runtime state is the first stop: `wg show` (fields include endpoints, latest-handshakes and transfer) and `wg showconf wg0`.

For packet-level logging:
- Linux kernel module on a kernel with dynamic debugging (output goes to dmesg), as root:

```bash
modprobe wireguard && echo module wireguard +p > /sys/kernel/debug/dynamic_debug/control
dmesg -w
```

- OpenBSD and FreeBSD, per interface: `ifconfig wg0 debug`.
- Userspace implementations: set `LOG_LEVEL=verbose` in the environment before starting, for example `LOG_LEVEL=verbose wireguard-go -f wg0`.

Related facts from the docs: handshakes depend on the system time, which should not jump (see wireguard-known-limitations); `AllowedIPs` decides where outgoing traffic for a peer is directed; and `WG_ENDPOINT_RESOLUTION_RETRIES` sets DNS retries for peer endpoints (15 if unset).

Verify: after enabling dynamic debug, `dmesg` shows WireGuard lines when traffic passes through the tunnel.

## Checked

2026-11-03. Confirmed: Dynamic-debug command, OpenBSD/FreeBSD ifconfig debug, LOG_LEVEL=verbose for userspace, wg show and showconf, and WG_ENDPOINT_RESOLUTION_RETRIES against the wg(8) man page and the quick start. Removed: the generic no-traffic checklist and the claim that ip link add auto-loads the module.

Method: documentation only; no commands were run.
