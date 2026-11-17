---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.ip-restriction
name: ip-restriction
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, ip-restriction, whitelist, blacklist, cidr, access-control, plugin]
level: intro
status: docs-checked
description: "Allow or deny client IPs and CIDR ranges in APISIX with ip-restriction: whitelist or blacklist, custom message, and 403 or 404 response_code."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/ip-restriction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ip-restriction

Attributes:
- `whitelist`: array of IPs or CIDR ranges that are allowed.
- `blacklist`: array of IPs or CIDR ranges that are denied.
- `message`: 1-1024 characters; default `Your IP address is not allowed`.
- `response_code`: 403 (default) or 404.

Use `whitelist` or `blacklist`, not both.

```json
{
  "plugins": {
    "ip-restriction": {
      "whitelist": ["192.168.1.241"],
      "message": "Access denied"
    }
  }
}
```

A blocked request gets `403 Forbidden` (or the configured `response_code`) with a body such as `{"message":"Access denied"}`.

## Checked

2026-11-04. Confirmed against the APISIX ip-restriction plugin page: whitelist and blacklist attributes, response_code, the 403 and its message. Nothing removed.

Method: documentation only; no commands were run.

