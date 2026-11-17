---
id: computing-software.cybersecurity-defensive.pomerium.tcp-route-ports
name: tcp-route-ports
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [tcp-routes, pomerium-cli-tcp, connect-method, transport-port, route-match-port]
level: practitioner
status: docs-checked
description: "Protect non-HTTP services with Pomerium TCP routes over HTTP CONNECT, the difference between transport and route-match ports, and pomerium-cli usage."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/non-http/tcp.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium tunnels TCP over HTTP using `CONNECT`; the client is `pomerium-cli` (or Pomerium Desktop). For SSH prefer native SSH access; use TCP tunnels for other protocols or when sshd cannot be changed.

Route example from the docs:
- `from: tcp+https://redis.corp.example.com:6379`
- `to: tcp://redis.internal.example.com:6379`
- policy allowing a contractor email or `claim/groups`.

Two ports:
1. **Transport port**: where the client reaches Pomerium, matching `address` (443 by default). If not 443 pass `--pomerium-url` with the port.
2. **Route-match port**: the port in `from`, sent in the CONNECT `:authority` header to identify the route. Use the destination service port. One hostname can host several TCP routes on different ports.

Do not change `from` to 443 merely for an outbound firewall. Ports in `from` and `to` are independent.

Deployment: do not put Pomerium behind another HTTP proxy; use an L4/TCP load balancer, or ensure the proxy forwards `CONNECT`.

HTTP-only settings (`regex_rewrite_pattern`, `set_request_headers`) do nothing on TCP routes. Traffic from the proxy to the upstream is unencrypted unless the protocol itself encrypts.

Connect: `pomerium-cli tcp redis.localhost.pomerium.io:6379`. It listens on loopback on a random port by default; the first connection goes through the standard Pomerium authentication flow. Note: the source page's CLI example shows 6739 where the route uses 6379, so use the route's port. See tcp-bastion-and-chaining.

## Checked

2026-11-04. Read the TCP over HTTP Support page: CONNECT tunnelling, the two ports, route example, firewall advice, L4 load balancer advice, HTTP-only settings, encryption caveat, loopback listener and the 6739 typo in the page confirmed. Reworded the first-connection authentication line to match the page.

Method: documentation only; no commands were run.
