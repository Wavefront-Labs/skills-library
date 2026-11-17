---
id: computing-software.database-administration.patroni.patroni-rest-api-security
name: patroni-rest-api-security
category: computing-software
field: database-administration
product: patroni
tags: [patroni, security, rest-api, basic-auth, allowlist]
level: practitioner
status: docs-checked
description: "Protect the Patroni REST API: safe versus unsafe endpoints, basic auth, allowlist and server_tokens."
sources:
  - https://patroni.readthedocs.io/en/latest/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restrict who can change cluster state through the API.

The REST API has safe endpoints (GET, read-only) and unsafe endpoints (PUT, POST, PATCH, DELETE, which change node state). It is used by Patroni itself in leader races, by patronictl, by load balancers for health checks, and for monitoring.

- Protect unsafe endpoints with HTTP basic-auth: `restapi.authentication.username` and `password`. There is no way to protect safe endpoints without enabling TLS.
- `allowlist`: hosts allowed to call unsafe endpoints, as host names, IPs or CIDR networks. Default is allow all. If `allowlist` or `allowlist_include_members` is set, anything not included is rejected.
- `allowlist_include_members: true` also lets other cluster members registered in DCS call unsafe endpoints (address taken from the member `api_url`). The OS may use a different outgoing IP.
- `request_queue_size` (default 5): once the TCP queue is full, further requests get "Connection denied".
- `server_tokens` controls the Server header: `Minimal` (Patroni version only, e.g. `Patroni/4.0.0`), `ProductOnly` (`Patroni`), or `Original` (default; BaseHTTP and Python versions).
- `http_extra_headers` and `https_extra_headers` add response headers, for example `X-Content-Type-Options: nosniff`, or `Strict-Transport-Security` over TLS (HTTPS headers also include the HTTP ones).
- `restapi.connect_address` must be reachable by all nodes and not be a loopback address in real clusters; Patroni uses it during the leader race to find nodes with minimal replication lag.
- `restapi.thread_pool_size`: default and minimum 5.

## Checked

2026-11-03. Confirmed against YAML Configuration Settings (restapi section) and the Security page: basic-auth on unsafe endpoints, allowlist, allowlist_include_members, request_queue_size, server_tokens values, extra header options, connect_address requirement and thread_pool_size.

Method: documentation only; no commands were run.
