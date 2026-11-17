---
id: computing-software.systems-network-administration.incus.network-acl-rules
name: network-acl-rules
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, network-acl, firewall, ingress, egress, rule-properties, selectors, address-sets]
level: practitioner
status: docs-checked
description: "Write Incus network ACLs: create, add and remove rules, ACL naming limits, rule properties (action, state, protocol, ports, ICMP), selectors and address sets."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/network_acls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network ACL rules

```
incus network acl create <ACL> [options...]
incus network acl rule add <ACL> <ingress|egress> [properties...]
incus network acl rule remove <ACL> <direction> [properties...] [--force]
incus network acl edit <ACL>
```

- Names: 1-63 chars, ASCII letters, digits, dashes; no leading digit or dash, no trailing dash.
- ACL properties: `name`, `description`, `ingress`, `egress`, `config` (`user.*` only).
- Rule: `action` (`allow`, `allow-stateless` OVN only, `reject`, `drop`); `state` (`enabled` default, `disabled`, `logged`); `source` (ingress) / `destination` (egress) as CIDRs, IP ranges or selectors; `protocol` (`icmp4`, `icmp6`, `tcp`, `udp`); `source_port` / `destination_port`; `icmp_type`, `icmp_code`.
- Selectors: ACL group names (OVN), `@internal`, `@external`, `@<network>/<peer>` (OVN peers).
- Address sets: `$<name>` in source/destination (bridge with nftables, and OVN).
- Remove needs enough properties to match uniquely, or `--force` for all matches. Individual rules are edited only via `acl edit`.

## Checked

2026-11-04: confirmed against the Incus network ACLs how-to (name rules, ACL and rule properties, `allow-stateless` OVN only, selectors, address sets, remove with `--force`). Nothing removed.

Method: documentation only; no commands were run.
