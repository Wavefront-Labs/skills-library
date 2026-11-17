---
id: computing-software.cybersecurity-defensive.pomerium.tcp-bastion-and-chaining
name: tcp-bastion-and-chaining
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [bastion-host, proxy-chaining, tcp-listen-address, stdin-stdout, tcp-https]
level: advanced
status: docs-checked
description: "Use pomerium-cli tcp advanced modes: custom listen address, STDIN/STDOUT piping, bastion-style route URLs and chaining to another HTTP-to-TCP proxy."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/non-http/tcp.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Listen address**: `pomerium-cli tcp` accepts an optional address and port to listen on. Using `-` attaches STDIN and STDOUT directly to the remote connection, useful for SSH or for sending data through a shell pipe.

**Bastion host** (Pomerium not reachable on 443, or route not in external DNS):
- Route `from`: `tcp+https://proxy.corp.example.com:8443/redis.internal.example.com:6379`
- CLI: `pomerium-cli tcp tcp+https://proxy.corp.example.com:8443/redis.internal.example.com:6379`

The CLI connects to the proxy host and port, then requests the route for the target host and port. The source's explanatory text names `pomerium.corp.example.com:8443`, which differs from the `proxy.corp.example.com` used in the examples; follow the examples.

**Proxy chaining**: the scheme of `to` decides what Pomerium does upstream.
- `tcp://` opens a raw TCP connection.
- `http://` sends an HTTP CONNECT request upstream, so another HTTP-to-TCP proxy can sit behind Pomerium.

Example: `from: tcp+https://example.corp.com:10002`, `to: http://second-proxy.example.corp.com:10003`.

Client certificate setup for these modes is covered in a shared include not captured here. See tcp-route-ports for the basics.

## Checked

2026-11-04. Read the TCP over HTTP Support page: listen address and dash option, bastion URL syntax and the page's hostname inconsistency, tcp:// versus http:// upstream behaviour and the chaining example confirmed. Removed an unsourced ProxyCommand reference.

Method: documentation only; no commands were run.
