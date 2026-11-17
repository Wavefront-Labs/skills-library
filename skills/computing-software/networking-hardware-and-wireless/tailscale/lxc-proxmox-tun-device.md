---
id: computing-software.networking-hardware-and-wireless.tailscale.lxc-proxmox-tun-device
name: lxc-proxmox-tun-device
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [lxc, proxmox, dev-net-tun]
level: practitioner
status: docs-checked
description: "Give the container access to /dev/net/tun or use userspace networking."
sources: ["https://tailscale.com/kb/1130"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailscale in LXC containers

Goal: run Tailscale inside an unprivileged LXC.

Tailscale encapsulates frames in UDP, so it needs no kernel modules or privileged operations to form tunnels, but it needs access to `/dev/net/tun`.

**Proxmox UI**

1. Create the container.
2. Resources tab, Add, Device Passthrough.
3. Device Path `/dev/net/tun`, Add.
4. If running, shut down and start again.
5. Install the Tailscale Linux package inside.

**Proxmox CLI** (`CTID` is the container ID):
```
pct set CTID --dev0 /dev/net/tun
pct set CTID --features keyctl=1,nesting=1
```

**Older config (Proxmox 7 example)** add to the container config file:
```
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
```
Restart a running container for it to take effect.

The `pct set` form is the Proxmox container tools alternative to the UI, and the config-file form is for Proxmox versions without UI support for the device.

**Alternative.** Userspace networking mode avoids needing any administrative access, if you do not want to grant `/dev/net/tun`.

**Checklist**

1. TUN device passed through.
2. Container restarted.
3. Or choose userspace mode.

## Checked

2026-11-03. Read Tailscale in LXC (kb/1130) and confirmed `/dev/net/tun` passthrough, `pct set` commands and the older config lines. Nothing else was removed.

Method: documentation only; no commands were run.
