---
id: computing-software.networking-hardware-and-wireless.tailscale.exit-node-setup
name: exit-node-setup
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [exit-node, autogroup-internet, allow-lan-access]
level: practitioner
status: docs-checked
description: "Advertise, approve and permit an exit node so devices can route internet traffic through it."
sources: ["https://tailscale.com/kb/1103"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Exit node setup

Goal: route a device's public internet traffic through another tailnet device.

**Opt-in chain.** Three things must all happen: the device advertises itself as an exit node, an Owner, Admin or Network admin allows it, and each client explicitly chooses to use it.

**Steps**

1. Install Tailscale on the exit node (Linux, macOS, Windows, Android, iOS or tvOS) and advertise it as an exit node. Clients and node must run v1.20 or later.
2. Allow it: Machines page, find the Exit Node badge (filter `property:exit-node`), menu, Edit route settings, Use as exit node. If the advertising user can approve exit nodes in `autoApprovers`, this is automatic.
3. Grant access. With the default policy any user may use it. With a custom policy you need a rule whose `dst` is `autogroup:internet`:
```
{"src": ["group:developers"], "dst": ["autogroup:internet"], "ip": ["*"]}
```
Adding the exit node device itself as `dst` only permits connecting to it (for example SSH), not using it as a gateway.
4. On each client select the exit node. Exit nodes capture all traffic not already directed to a subnet router or app connector (default routes 0.0.0.0/0 and ::/0).

**Local network.** A client loses access to its own LAN while using an exit node. Enable Allow Local Network Access, or pass `--exit-node-allow-lan-access` to `tailscale up` or `tailscale set`.

**Checklist**

1. Advertised.
2. Allowed in the admin console.
3. `autogroup:internet` in policy.
4. LAN access decided.

## Checked

2026-11-03. Read Exit nodes (kb/1103) and confirmed the advertise/allow/choose chain, v1.20 requirement, `autogroup:internet` rule, default routes and LAN access flag. Nothing else was removed.

Method: documentation only; no commands were run.
