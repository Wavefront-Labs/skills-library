---
id: computing-software.cybersecurity-defensive.pomerium.reverse-tunnel-r-syntax
name: reverse-tunnel-r-syntax
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [dynamic-forwarding, static-forwarding, remote-port-zero, wildcard-routes, tunnel-troubleshooting]
level: advanced
status: docs-checked
description: "Write correct OpenSSH -R arguments for Pomerium reverse tunnels: static vs dynamic forwarding, port 0 rule, route-name globs and common mismatches."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/reverse-tunneling.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`-R` takes one or two `name:port` addresses; the remote address comes first, the optional local address is used only by the client.

Pomerium rules:
- Remote port `0` means dynamic forwarding: omit the local address. Never use 0 when you provide one.
- `name` is the route hostname (host part of `from`, no scheme).
- `port` picks the protocol: `443` matches HTTP routes, `22` matches SSH routes. Fixed, not tied to Pomerium's listening ports.
- Each `-R` is a separate request. Unix sockets are unsupported.

**Static**: local address present; connections go to that host and port; the route `to` scheme still sets the protocol.
**Dynamic**: local address omitted; the server chooses. One client can forward many routes. `name` accepts globs matching route hostnames; with several `to` URLs Pomerium round-robins (dynamic only).

Glob caveat: `*` and `?` work only with remote port 0 (e.g. `-R *.example.com:0`). Without it `-R *.example.com:443` matches only the literal `https://*.example.com` route.

Mismatches (Pomerium and the client must agree on dynamic):
- Remote port 0 with local host:port, e.g. `ssh -R https-*:0:localhost:8080 example.com`: downstream requests and health checks time out; the TUI warns.
- Non-zero remote port with local omitted, e.g. `ssh -R https-route.example.com:443 example.com`: immediate downstream errors.

## Checked

2026-11-04. Read the Reverse Tunneling page: -R address structure, port 0 rule, name and port meaning (443 HTTP, 22 SSH), static and dynamic modes, wildcard behaviour and both mismatch cases all confirmed. Nothing removed.

Method: documentation only; no commands were run.
