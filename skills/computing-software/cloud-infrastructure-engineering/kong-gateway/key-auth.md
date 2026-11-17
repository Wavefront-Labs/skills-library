---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.key-auth
name: key-auth
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, key-auth, apikey, key-names, authentication, plugins]
level: intro
status: docs-checked
description: "key-auth plugin settings: key_names default apikey, key_in_header/query/body, hide_credentials, anonymous, run_on_preflight, realm, and how clients send the key."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/key-auth/schema.lua
  - https://developer.konghq.com/plugins/key-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# key-auth

| Field | Default |
|---|---|
| `key_names` | `["apikey"]` |
| `key_in_header` | `true` |
| `key_in_query` | `true` |
| `key_in_body` | `false` |
| `hide_credentials` | `false` (strip the key before proxying) |
| `anonymous` | none (Consumer ID or username used when auth fails) |
| `run_on_preflight` | `true` (when `false`, OPTIONS preflight is always allowed) |
| `realm` | none (sent in `WWW-Authenticate` on failure) |

Header names are case-insensitive; query parameter names are case-sensitive. Keys in query strings can leak into logs and URLs, so enable only the locations you need. Body lookup is less performant.

Create a credential under a Consumer (`/consumers/{usernameOrId}/key-auth`), or `keyauth_credentials` in declarative config.

Call with a key:

```bash
curl http://kong:8000/$PROXY_PATH -H 'apikey: <API_KEY>'
curl "http://localhost:8000/$PROXY_PATH?apikey=<API_KEY>"
```

Results: valid key proxied (200); missing or unknown key, 401; runtime error, 500.

## Checked

2026-11-04. Confirmed against the key-auth schema.lua (all defaults) and the plugin page (case sensitivity, key location advice, keyauth_credentials and /consumers/{usernameOrId}/key-auth, curl examples, 200/401/500 behaviour matrix).

Method: documentation only; no commands were run.
