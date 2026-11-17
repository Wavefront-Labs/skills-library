---
id: computing-software.systems-network-administration.headscale.exit-nodes
name: exit-nodes
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, exit-node, advertise-exit-node, suggest, default-route]
level: practitioner
status: docs-checked
description: "Set up a Headscale exit node: advertise, approve 0.0.0.0/0, select it on clients, and use auto selection with suggest-exit-node attributes."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exit nodes

Same double opt-in as subnet routers.

```
sudo tailscale up --login-server <YOUR_HEADSCALE_URL> --advertise-exit-node
sudo tailscale set --advertise-exit-node
headscale nodes approve-routes --identifier 1 --routes 0.0.0.0/0
sudo tailscale set --exit-node myexit
```

- Approving either the IPv4 or IPv6 default route is enough; the other is approved automatically.
- Tagged exit node: `sudo tailscale up --login-server <YOUR_HEADSCALE_URL> --advertise-tags tag:exit --advertise-exit-node`.

## Automatic selection

```
sudo tailscale exit-node suggest
sudo tailscale set --exit-node=auto:any
```

The policy `nodeAttrs` entries `suggest-exit-node` and `suggest-exit-node-ui` control suggestions and the "Recommended" selector in GUIs.

## Gotchas

- Exit nodes require IP forwarding on the host.
- Without a policy, all nodes can use any exit node; restrict with `autogroup:internet` grants (route-restriction-policy).
- Auto-approve with `autoApprovers.exitNode` listing tags.

## Checked

2026-11-04. Confirmed against the Headscale routes reference: advertise, approve-routes, either-route approval, `tailscale set --exit-node`, tagged exit node, `suggest`, `auto:any`, the two nodeAttrs, autogroup:internet and autoApprovers.exitNode.
Method: documentation only; no commands were run.
