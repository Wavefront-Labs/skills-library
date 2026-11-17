---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.ip-restriction
name: ip-restriction
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, ip-restriction, cidr, allow-deny, plugins, access-control]
level: intro
status: docs-checked
description: "ip-restriction plugin: allow or deny lists of IPs and CIDR ranges, at least one required, optional custom status and message, and the protocols it covers."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/ip-restriction/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ip-restriction

Config fields:
- `allow`: array of IPs or CIDR ranges
- `deny`: array of IPs or CIDR ranges
- `status`: number; HTTP status for rejected requests (optional)
- `message`: string; response body for rejected requests (optional)

At least one of `allow` or `deny` must be set (an `at_least_one_of` entity check).

Protocols default to `http`, `https`, `tcp`, `tls`, `grpc`, `grpcs`, so it also works on stream Routes.

The schema gives no defaults for `status` or `message`; set them explicitly if you need a particular response.

## Checked

2026-11-04. Confirmed against the ip-restriction schema.lua: allow and deny as IP or CIDR arrays, optional status and message, at_least_one_of check, default protocols. Removed the sentence tying the evaluated address to real_ip_header and trusted_ips: the cited page does not state it.

Method: documentation only; no commands were run.
