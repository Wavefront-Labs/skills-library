---
id: computing-software.systems-network-administration.headscale.route-restriction-policy
name: route-restriction-policy
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, autoapprovers, via, tagowners, grants, route-policy]
level: advanced
status: docs-checked
description: "Control who can advertise and use Headscale routes and exit nodes: tagOwners, autoApprovers, grants with via, and autogroup:internet limits."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restricting and auto-approving routes

Policy keys used by the routes docs:

- `hosts`: names to addresses (e.g. `router`, `service.example.net`).
- `tagOwners`: tag to owners (`tag:router`, `tag:exit`).
- `autoApprovers.routes`: prefix to tags, so tagged routers' prefixes are approved automatically.
- `autoApprovers.exitNode`: tags whose exit nodes are approved automatically.
- `grants`: `src`, `dst`, `ip`, and `via`.
- `nodeAttrs`: `target` and `attr` (`suggest-exit-node`, `suggest-exit-node-ui`).

## Restrict a subnet

A grant can deny access to the router itself while allowing access to a service behind it, using `dst` as the service host and `ip` as ports such as `"80,443"`.

## Restrict exit nodes

`autogroup:internet` as `dst` limits who can use any exit node. Tag-based grants with `via` assign specific users to specific exit nodes (e.g. `tag:exit1`, `tag:exit2`). In the documented example, each user's grant has `via` set to that exit node's tag.

## Gotchas

- Without a policy, every node can use any advertised route or exit node.
- Tagged router registration needs the user in `tagOwners` (register-tagged-nodes).
- See policy-basics for how policy changes are applied.

## Checked

2026-11-04. Confirmed against the Headscale routes reference: hosts/grants example denying the router itself, autoApprovers routes and exitNode, autogroup:internet, per-user exit node grants with via, and the no-policy default. Reworded the via explanation and the reload remark to what the page shows.
Method: documentation only; no commands were run.
