---
id: computing-software.systems-network-administration.headscale.subnet-routers
name: subnet-routers
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, subnet-router, advertise-routes, approve-routes, accept-routes]
level: practitioner
status: docs-checked
description: "Advertise a subnet from a Tailscale node, approve it in Headscale, and make clients accept routes. Double opt-in and IP forwarding."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subnet routers

Routes need approval on both the router node and the control server.

```
sudo tailscale up --login-server <YOUR_HEADSCALE_URL> --advertise-routes=10.0.0.0/8,192.168.0.0/24
sudo tailscale set --advertise-routes=10.0.0.0/8,192.168.0.0/24
headscale nodes list-routes
headscale nodes approve-routes --identifier 1 --routes 10.0.0.0/8,192.168.0.0/24
sudo tailscale set --accept-routes
```

- `tailscale up` registers and advertises; `tailscale set` changes an already registered node.
- `--identifier` is the node ID; `--routes` a comma-separated list.
- On clients that should use the routes: `tailscale set --accept-routes`.

## Auto-approval

Use `autoApprovers` in the policy (route-restriction-policy):

```
sudo tailscale up --login-server <YOUR_HEADSCALE_URL> --advertise-tags tag:router --advertise-routes 192.168.0.0/24
```

## Gotchas

- Subnet routers require IP forwarding on the host; the docs defer to Tailscale's documentation.
- With no policy, all nodes can use any advertised route.
- Two nodes advertising the same prefix enable high availability (ha-routing).

## Checked

2026-11-04. Confirmed against the Headscale routes reference: double opt-in, `tailscale up/set --advertise-routes`, `headscale nodes list-routes`, `approve-routes --identifier --routes`, `--accept-routes`, auto-approval example, IP forwarding deferral, and no-policy default.
Method: documentation only; no commands were run.
