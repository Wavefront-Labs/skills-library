---
id: computing-software.rpa-and-low-code.n8n.ssrf-protection
name: ssrf-protection
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, ssrf, security, http-request, allowlist, blocked-ranges]
level: advanced
status: docs-checked
description: "Turn on n8n SSRF protection with N8N_SSRF_PROTECTION_ENABLED, understand default blocked ranges and the hostname, IP allowlist and blocklist precedence."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/enable-ssrf-protection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop workflow nodes (such as HTTP Request) from reaching internal addresses, cloud metadata endpoints or localhost. Available from n8n 2.12.0. It is defense in depth: firewalls, security groups and network policies stay the primary control.

Enable: `N8N_SSRF_PROTECTION_ENABLED=true`. n8n then validates outbound requests from user-controllable nodes, including redirect targets and DNS resolution (to defeat DNS rebinding).

## Default blocked
`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`; loopback `127.0.0.0/8`, `::1/128`; link-local `169.254.0.0/16`, `fe80::/10`; IPv6 unique local `fc00::/7`, `fd00::/8`; reserved ranges `0.0.0.0/8`, `192.0.0.0/24`, `192.0.2.0/24`, `198.18.0.0/15`, `198.51.100.0/24`, `203.0.113.0/24`. Extend with `N8N_SSRF_BLOCKED_IP_RANGES=default,100.0.0.0/8`.

## Allow legitimate internal services
Precedence: hostname allowlist, then IP allowlist, then IP blocklist.
```
N8N_SSRF_ALLOWED_HOSTNAMES=*.n8n.internal,*.company.local
N8N_SSRF_ALLOWED_IP_RANGES=10.0.1.0/24,10.0.2.50/32
```
Hostname allowlists bypass the IP blocklist checks, so list only hostnames in DNS zones you control.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Enable SSRF protection" page (docs.n8n.io, Markdown version, read in full).
Nothing removed; variable names, blocked ranges, precedence and the hostname allowlist caution match the page.
