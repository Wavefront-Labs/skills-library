---
id: computing-software.networking-hardware-and-wireless.unbound.forward-zones
name: forward-zones
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, forward-zone, forward-addr, forward-first, forwarding, upstream-resolver]
level: practitioner
status: docs-checked
description: "Forward queries for a zone, or everything, to upstream resolvers using forward-zone: addresses, ports, fallback, TLS and cache bypass."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forward zones
A `forward-zone:` clause (repeatable) sends queries for a zone to given servers instead of recursing from the root.

- `name:` is the zone; the name `"."` forwards everything.
- `forward-addr:` is the upstream IP, and accepts `@port` and `#auth-name`.
- `forward-host:` is a hostname resolved first; same suffixes.
- The listed servers must be recursive resolvers, not authoritative servers: Unbound does no recursion itself for the zone. It chases CNAMEs itself, asking the forwarder for each name.
- `forward-first: yes` (default no) falls back to less specific resolution (another matching zone, or normal recursion) when the forwarded query gets SERVFAIL. It can also work around a `forward-host` circular dependency, but lets queries escape the zone on any failure.
- `forward-tls-upstream: yes` (alias `forward-ssl-upstream`, default no) uses TLS; needs `tls-cert-bundle` or `tls-win-cert`.
- `forward-tcp-upstream: yes` (default no) uses TCP.
- `forward-no-cache: yes` (default no) stops caching of answers from this zone.

Without `#auth-name` any certificate name is accepted, though it must chain to the `tls-cert-bundle`. If only `#` is used, the port defaults to `tls-port`.

Runtime: `unbound-control forward_add [+it] zone addr...` (`+i` also adds domain-insecure, `+t` uses TLS upstream), `forward_remove [+i] zone`, and `list_forwards`. `unbound-control forward [off | addr...]` changes only the `"."` forwarders, and the config file is unchanged so a reload undoes it.

Note: the `ratelimit` option excludes forwarders.

## Checked

2026-11-08. Read the whole Forward Zone Options section of the unbound.conf manual and the forward_add, forward_remove and forward commands. Corrected forward-first (falls back on SERVFAIL to less specific resolution, not any failure), added that forwarders must be recursive, the # and @ suffix rules and the forward command.

Method: documentation only; no commands were run.
