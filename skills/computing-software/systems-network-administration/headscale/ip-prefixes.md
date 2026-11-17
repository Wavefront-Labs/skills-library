---
id: computing-software.systems-network-administration.headscale.ip-prefixes
name: ip-prefixes
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, prefixes, allocation, cgnat, ipv6]
level: practitioner
status: docs-checked
description: "Configure the tailnet IPv4 and IPv6 prefixes and allocation mode in Headscale, and the constraint that they stay inside Tailscale's ranges."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/about/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IP prefixes and allocation

```yaml
prefixes:
  v4: 100.64.0.0/10
  v6: fd7a:115c:a1e0::/48
  allocation: sequential
```

- The prefixes MUST be subsets of the standard Tailscale ranges. Tailscale supports `100.64.0.0/10` and `fd7a:115c:a1e0::/48` (or smaller subnets).
- `allocation: sequential` (default) assigns the next free IP from the previously given IP on a best-effort basis, so it might leave or fill holes in the range; `random` assigns the next free IP from a pseudo-random generator (crypto/rand).
- Using ranges outside CGNAT/ULA is not supported and causes undefined behaviour; using a subset such as `100.64.0.0/24` is supported.
- Migrating prefixes updates the IP addresses of all nodes; see migrate-ip-prefixes.

## Related

- `disable-ipv4` node attribute can help with CGNAT conflicts for specific nodes (policy-node-attributes).
- Dual stack IPv4 and IPv6 is supported (feature-support).
- The FAQ's migration steps include updating the policy to reflect IP address changes.

## Checked

2026-11-04. Confirmed against config-example.yaml (`prefixes`, allocation modes, range warning) and the Headscale FAQ (supported prefixes, migration). Removed the Gotchas about choosing a smaller subnet up front and backing up before touching prefixes, which are not stated outside the migration warning.

Method: documentation only; no commands were run.
