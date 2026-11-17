---
id: computing-software.networking-hardware-and-wireless.tailscale.acl-rule-fields
name: acl-rule-fields
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [acl-syntax, proto-field, dst-ports]
level: advanced
status: docs-checked
description: "Use action, src, proto and dst in the acls section, including protocol aliases and port format."
sources: ["https://tailscale.com/kb/1337"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ACL rule fields

Goal: write correct `acls` entries.

```
{
  "action": "accept",
  "src": ["group:dev"],
  "proto": "tcp",
  "dst": ["tag:prod:22,443"]
}
```

**Fields**

- `action`: only `accept` exists because access is denied by default.
- `src` accepts `*`, a user email, `group:<name>`, a Tailscale IP, a CIDR, a host alias, `tag:<name>`, `autogroup:<role|property>`, and `autogroup:danger-all` (includes sources outside the tailnet). Optional `srcPosture` limits sources to devices matching posture conditions.
- `proto` is optional: an IANA protocol number 1-255 or a named alias such as `tcp` (6), `udp` (17), `sctp` (132), `gre` (47), `esp` (50), `ah` (51), `igmp` (2), `egp` (8), `igp` (9), `ipv4`/`ip-in-ip` (4). Without it, TCP and UDP apply. Needs v1.18.2 or later.
- `dst` entries use `<host>:<ports>`. IPv6 addresses use the form `[1:2:3::4]:80`.
- Only TCP, UDP and SCTP support specific ports; other protocols only support `*`.
- If traffic is allowed between a pair of IPs, ICMP is also allowed.
- The legacy `users` and `ports` fields still work, but use `src` and `dst`.

**Checklist**

1. Use `src` and `dst`.
2. Set `proto` only for non-default protocols.
3. Use `*` ports for non-TCP/UDP/SCTP.

## Checked

2026-11-03. Read Tailnet policy syntax (kb/1337) and confirmed action, src types, `srcPosture`, `proto` numbers and aliases (v1.18.2), dst port formats and ICMP behaviour. Nothing else was removed.

Method: documentation only; no commands were run.
