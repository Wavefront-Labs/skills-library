---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.csrf-protection
name: csrf-protection
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, csrf, csrf-token, cookie, security, plugin]
level: practitioner
status: docs-checked
description: "Add CSRF protection to an APISIX route with the csrf plugin: key, cookie name, expires, which methods are checked, and the 401 returned for a missing token."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/csrf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# csrf protection

Attributes:
- `key` (required): secret used to encrypt the cookie; stored encrypted in etcd.
- `name`: cookie and header name, default `apisix-csrf-token`.
- `expires`: seconds, default 7200; 0 skips the expiry check.

How it works:
- `GET`, `HEAD` and `OPTIONS` are safe and not checked.
- A GET response sets a cookie with an encrypted token, and a new cookie is issued on every request.
- Any other method must send the token in a request header named by `name`, and also carry the cookie.

```json
{
  "uri": "/hello",
  "plugins": { "csrf": { "key": "<CSRF_SECRET>" } },
  "upstream": { "type": "roundrobin", "nodes": { "127.0.0.1:9001": 1 } }
}
```

An unsafe-method request without the header token returns 401 with `{"error_msg":"no csrf token in headers"}`.

## Checked

2026-11-04. Confirmed against the APISIX csrf plugin page: attributes, token cookie and header flow, the 401 message for a missing header token. Nothing removed.

Method: documentation only; no commands were run.

