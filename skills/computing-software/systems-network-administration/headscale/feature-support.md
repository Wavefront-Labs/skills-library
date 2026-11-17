---
id: computing-software.systems-network-administration.headscale.feature-support
name: feature-support
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, features, funnel, taildrop, supported, flow-logs]
level: intro
status: docs-checked
description: "Which Tailscale features Headscale supports (routes, DNS, SSH, Taildrive, peer relays, OIDC) and the ones it does not (Funnel, flow logs)."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature support

Supported:

- Node registration: web authentication and pre-authenticated keys.
- DNS: MagicDNS, global and split nameservers, search domains, Headscale-only extra records.
- File sharing: Taildrive and Taildrop.
- Tags; routes (subnet routers, exit nodes, route filtering with via).
- Dual stack IPv4 and IPv6; ephemeral nodes.
- Embedded DERP server; peer relays.
- Policy: ACLs, grants, some autogroups, auto approvers, Tailscale SSH, node attributes, tests and sshTests.
- OIDC single sign-on: basic registration and updating user profile from the identity provider.
- Serve.

Not supported:

- Funnel (issue #1040).
- Network flow logs (issue #1687).
- OIDC groups in ACLs.

## Design scope

Headscale aims to be a self-hosted, open source alternative to the Tailscale control server for self-hosters and hobbyists.

For policy differences from Tailscale, see policy-limitations.

## Checked

2026-11-04. Confirmed against the Headscale features page: every supported item, the three unchecked items with issue numbers #1040 and #1687, and the stated goal. Removed an unsourced single-tailnet remark and a generic gotcha.
Method: documentation only; no commands were run.
