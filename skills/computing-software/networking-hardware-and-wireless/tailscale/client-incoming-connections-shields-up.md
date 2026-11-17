---
id: computing-software.networking-hardware-and-wireless.tailscale.client-incoming-connections-shields-up
name: client-incoming-connections-shields-up
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [shields-up, incoming-connections, client-defaults]
level: intro
status: docs-checked
description: "Default client behaviour and how to toggle incoming connections."
sources: ["https://tailscale.com/kb/1072"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shields up

Goal: let a device make outgoing connections but accept none.

**Defaults.** A client allows incoming connections and uses Tailscale DNS settings. macOS, Windows and other non-Linux devices use Tailscale subnets by default; Linux devices do not.

**Incoming connections.** If access policies allow another device to connect, the connection is created. Policies are directional.

**Blocking.** Turn off Allow Incoming Connections ("shields up"). The device stays visible and can send traffic, but accepts no connections over Tailscale, including pings.

- Tailscale v1.60.0 or later: menu bar, Tailscale, Settings, uncheck Allow incoming connections.
- Earlier than v1.60.0: menu bar, Tailscale, uncheck it.

**CLI**
```
tailscale set --shields-up
tailscale set --shields-up=false
```
The second returns to the default of allowing connections. `--shields-up` is also a `tailscale up` flag.

System policies can manage the same setting with `AllowIncomingConnections`.

**Checklist**

1. Use shields up on personal devices.
2. Remember pings are blocked too.
3. Check version for the menu location.

## Checked

2026-11-03. Read Client preferences (kb/1072) and Tailscale SSH (kb/1193) and confirmed the Allow incoming connections setting, v1.60.0 menu change and `tailscale set --shields-up`; reworded the `up` flag mention. Nothing else was removed.

Method: documentation only; no commands were run.
