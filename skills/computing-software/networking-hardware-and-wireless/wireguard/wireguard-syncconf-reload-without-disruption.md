---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-syncconf-reload-without-disruption
name: wireguard-syncconf-reload-without-disruption
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wg-syncconf, wg-quick-strip, wg-addconf, config-reload, no-downtime, wg-setconf]
level: advanced
status: docs-checked
description: "Apply config changes to a live tunnel without dropping sessions using wg syncconf and wg-quick strip."
sources: ["https://man7.org/linux/man-pages/man8/wg.8.html", "https://man7.org/linux/man-pages/man8/wg-quick.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reload WireGuard config without disrupting sessions

Three ways to load a file into an interface, with different effects:
- `wg setconf wg0 file`: replaces the whole configuration (can disturb existing peers).
- `wg addconf wg0 file`: appends the file's content to the current configuration.
- `wg syncconf wg0 file`: reads the existing configuration first and applies only the differences, so current peer sessions are not disrupted. It is much less efficient than `setconf`.

All three require plain wg format. If the file is a wg-quick file (`Address`, `DNS`, `PostUp` and so on), convert it first with `wg-quick strip`, which outputs the file with every wg-quick-specific option removed:

```bash
wg syncconf wgnet0 <(wg-quick strip wgnet0)
```

This reloads `/etc/wireguard/wgnet0.conf` after you edit peers, leaving routes, addresses and hooks alone. `wg-quick strip` removes the wg-quick-specific keys (`Address`, `Table`, `DNS`, `MTU`, hooks), so changes to them are not applied by this command.

`wg showconf wg0` prints the live configuration in file format, handy for diffing against what you intended and for bootstrapping a config file from a hand-built interface. `wg-quick save wg0` writes the configuration of an existing interface back to its file without bringing it down.

Verify: `wg showconf wg0` after the reload shows the edited peers.

## Checked

2026-11-03. Confirmed: setconf, addconf and syncconf semantics, wg-quick strip, the syncconf-with-strip example, showconf and wg-quick save against the wg(8) and wg-quick(8) man pages. Removed: 'safe for large production interfaces' and the bring-down-and-up advice.

Method: documentation only; no commands were run.
