---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-wg-show-scripting-output
name: wireguard-wg-show-scripting-output
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wg-show, latest-handshakes, transfer, dump, monitoring, wg-hide-keys, wg-color-mode]
level: practitioner
status: docs-checked
description: "Read WireGuard status in scripts: wg show fields, the dump format, handshake ages and the display environment variables."
sources: ["https://man7.org/linux/man-pages/man8/wg.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# wg show for monitoring and scripts

`wg` with no command runs `wg show all`. Forms:

```bash
wg show interfaces                      # one interface name per line
wg show wg0                             # pretty, terminal-oriented output
wg show wg0 latest-handshakes           # <peer pubkey>\t<latest handshake>
wg show wg0 transfer                    # <peer>\t<rx bytes>\t<tx bytes>
wg show all endpoints                   # first column is the interface name
wg show wg0 dump
```

Selectable fields: `public-key`, `private-key`, `listen-port`, `fwmark`, `peers`, `preshared-keys`, `endpoints`, `allowed-ips`, `latest-handshakes`, `persistent-keepalive`, `transfer`, `dump`. With a field name the output is tab/newline separated for scripts.

`dump` prints one interface line (private-key, public-key, listen-port, fwmark, tab-separated) then one line per peer: public-key, preshared-key, endpoint, allowed-ips, latest-handshake, transfer-rx, transfer-tx, persistent-keepalive.

Handshakes repeat every few minutes (see wireguard-handshake-timers-and-key-rotation), so the latest-handshake value of a peer that is in use should stay recent.

Environment: `WG_HIDE_KEYS=never` shows private and preshared keys in pretty output (by default they print as `(hidden)`); `WG_COLOR_MODE=always|never|auto` controls ANSI colour.

Verify: the first line of `wg show wg0 dump` has four tab-separated fields.

## Checked

2026-11-03. Confirmed: show targets, selectable fields, script-friendly output, interface-name first column for all, dump field order, WG_HIDE_KEYS and WG_COLOR_MODE against the wg(8) man page; handshake cadence against the protocol page. Removed: unix-time unit for latest-handshakes, the meaning of 0, and the alert-threshold advice (not in the docs).

Method: documentation only; no commands were run.
