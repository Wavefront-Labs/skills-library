---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.jwt
name: jwt
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, jwt, key-claim-name, claims-to-verify, authentication, plugins]
level: practitioner
status: docs-checked
description: "jwt plugin config: uri_param_names, cookie_names, header_names, key_claim_name iss, claims_to_verify exp/nbf, maximum_expiration, plus credential fields."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/jwt/schema.lua
  - https://developer.konghq.com/plugins/jwt/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jwt plugin

Config defaults:

| Field | Default |
|---|---|
| `uri_param_names` | `["jwt"]` |
| `cookie_names` | `[]` |
| `header_names` | `["authorization"]` |
| `key_claim_name` | `iss` |
| `secret_is_base64` | `false` |
| `claims_to_verify` | none; elements must be `exp` or `nbf` |
| `maximum_expiration` | `0` (range 0 to 31536000 seconds) |
| `run_on_preflight` | `true` |
| `anonymous`, `realm` | none |

If `maximum_expiration` is above 0, `claims_to_verify` must include `exp`.

Clients may send the token in a query parameter, a cookie, or a header such as `Authorization: Bearer <token>`. If Kong finds multiple differing tokens, even valid ones, it rejects the request to prevent JWT smuggling.

Kong looks up the credential by the `key_claim_name` claim in the payload, then the header.

Credential (under `/consumers/{consumer}/jwt`, or `jwt_secrets` in declarative config):
- `algorithm`: HS256 or RS256 (ES256 also covered)
- `key`: identifier that goes in the token's `iss` claim
- `secret`: required by decK and KIC; use a dummy value for RS/ES/PS
- `rsa_public_key`: required for RS256 and ES256

## Checked

2026-11-04. Confirmed against the jwt schema.lua (all defaults, ranges, the maximum_expiration/exp entity check, key_claim_name read from payload then header) and the plugin page (token locations, multiple-token rejection, jwt_secrets, credential fields, dummy secret for RS/ES/PS).

Method: documentation only; no commands were run.
