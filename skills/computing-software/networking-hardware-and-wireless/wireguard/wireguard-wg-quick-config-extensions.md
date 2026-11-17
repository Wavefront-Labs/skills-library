---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-wg-quick-config-extensions
name: wireguard-wg-quick-config-extensions
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wg-quick, address, dns, mtu, table, postup, predown, saveconfig, resolvconf]
level: practitioner
status: docs-checked
description: "Use wg-quick: up, down, save, strip, and the extra Interface keys Address, DNS, MTU, Table, hooks and SaveConfig."
sources: ["https://man7.org/linux/man-pages/man8/wg-quick.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# wg-quick and its config keys

`wg-quick [up|down|save|strip] [CONFIG_FILE|INTERFACE]`. A bare interface name loads `/etc/wireguard/INTERFACE.conf` first, then distro-specific paths; a file path must be named `<interface>.conf`. Interface names match `[a-zA-Z0-9_=+.-]{1,15}`.

`up` adds the interface, assigns addresses, sets MTU and routes, runs hooks. `down` optionally saves config, removes the interface. `save` writes live state to the file. `strip` prints a plain wg config.

Extra keys in `[Interface]` (everything else goes to `wg setconf`):
- `Address`: comma list or repeated; IPv4/IPv6 with optional CIDR.
- `DNS`: IPs become DNS servers, non-IP names become search domains. Runs `resolvconf -a tun.INTERFACE -m 0 -x` on up and `resolvconf -d tun.INTERFACE` on down. Use PostUp/PostDown instead if you do not want resolvconf.
- `MTU`: derived from endpoint addresses or the default route when omitted.
- `Table`: `auto` (default) adds routes to the default table and enables special handling of default routes; `off` creates no routes; a number selects a table.
- `PreUp`, `PostUp`, `PreDown`, `PostDown`: bash snippets; `%i` expands to the interface name; repeatable and run in order.
- `SaveConfig = true`: on shutdown the file is rewritten from the live interface, discarding manual edits made while it was up.

Routes are inferred from every peer's `AllowedIPs`. If one is `0.0.0.0/0` or `::/0`, wg-quick uses `ip rule` to override the default gateway. The man page says wg-quick is for simple needs; for more advanced setups use wg and ip directly.

Example full-tunnel client: `Address = 10.200.100.8/24`, `DNS = 10.200.100.1`, one peer with `AllowedIPs = 0.0.0.0/0`.

Verify: after `wg-quick up`, `wg show` lists the interface and `ip route` shows routes for the peers' AllowedIPs.

## Checked

2026-11-03. Confirmed: Subcommands, config lookup order, interface-name pattern, Address/DNS/MTU/Table/hook/SaveConfig semantics, resolvconf invocations, default-route handling, the full-tunnel example, against the wg-quick(8) man page. Fixed: Table=auto adds routes to the default table (not 'main'). Removed: the grep-based verify command.

Method: documentation only; no commands were run.
