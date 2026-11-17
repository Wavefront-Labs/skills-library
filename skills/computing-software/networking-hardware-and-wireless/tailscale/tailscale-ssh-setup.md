---
id: computing-software.networking-hardware-and-wireless.tailscale.tailscale-ssh-setup
name: tailscale-ssh-setup
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [tailscale-ssh, check-mode, ssh-policy]
level: practitioner
status: docs-checked
description: "Advertise Tailscale SSH and write the network plus SSH access rules it needs."
sources: ["https://tailscale.com/kb/1193"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailscale SSH setup

Goal: let Tailscale authenticate and authorize SSH connections instead of managing keys.

**Server side.** The server component runs on Linux and on macOS using the open source `tailscale` + `tailscaled` CLI devices, and needs v1.24 or later. Any platform can be a client. On the destination host run:
```
tailscale set --ssh
```
This generates a host key pair, shares the public half with the control plane, and intercepts tailnet traffic to port 22 on the Tailscale IP. Existing SSH connections to that IP will hang. Your `/etc/ssh/sshd_config` and `~/.ssh/authorized_keys` are not modified, so non-Tailscale SSH still works.

**Policy.** Both of these must be permitted in the tailnet policy file:

1. A network rule from source to destination (an ACL or grant).
2. An `ssh` rule naming the users allowed on the host.

The default policy grants both for the whole tailnet; you only edit if you changed the default. Editing the policy requires Admin or Network admin.

**Behaviour**

- Authentication uses Tailscale node keys over WireGuard; Tailscale writes the client `known_hosts` just in time so `ssh myhost` works.
- Tailscale only uses accounts that already exist on the host; it does not create them.

**Checklist**

1. `tailscale set --ssh` on the host.
2. Network rule present.
3. `ssh` rule present.
4. Version at least v1.24.

## Checked

2026-11-03. Read Tailscale SSH (kb/1193) and confirmed `tailscale set --ssh`, v1.24 server requirement, the two policy rules, the default policy and unchanged sshd config. Nothing else was removed.

Method: documentation only; no commands were run.
