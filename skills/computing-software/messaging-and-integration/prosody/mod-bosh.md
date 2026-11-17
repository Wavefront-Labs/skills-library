---
id: computing-software.messaging-and-integration.prosody.mod-bosh
name: mod-bosh
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, bosh, xep-0124, http, web-clients]
level: practitioner
status: docs-checked
description: "mod_bosh in Prosody: enabling BOSH (XEP-0124/0206), bosh_max_inactivity 60, consider_bosh_secure, and the advanced hold, request and wait limits."
sources:
  - https://prosody.im/doc/modules/mod_bosh
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_bosh

Add `"bosh"` to `modules_enabled`. Implements XEP-0124 and XEP-0206. Options go in the global section.

| Option | Default |
|---|---|
| `bosh_max_inactivity` | 60 seconds |
| `consider_bosh_secure` | false |

Advanced (leave alone unless needed): `bosh_default_hold` 1, `bosh_max_requests` 2, `bosh_max_wait` 120, `trusted_proxies` `{ "127.0.0.1", "::1" }`.

```lua
bosh_max_inactivity = 60
consider_bosh_secure = true -- when proxying HTTPS to HTTP
```

`consider_bosh_secure` lets BOSH work when encryption is required even though Prosody sees a plain connection.

CORS: cross-domain requests are allowed by default; change via the HTTP server's CORS settings (`http_cors_override`).

Verify: a BOSH client connects through the HTTP server.

## Checked

2026-11-04. Read the mod_bosh page and the Prosody HTTP page: XEP-0124 and XEP-0206, global-only options, bosh_max_inactivity 60, consider_bosh_secure false, advanced defaults (hold 1, max_requests 2, max_wait 120, trusted_proxies loopback), CORS allowed by default and http_cors_override all match. Removed the claim that prosodyctl shell http list shows the bosh URL (the BOSH page does not say so).

Method: documentation only; no commands were run.
