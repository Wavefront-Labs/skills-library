---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.jwt-auth-setup
name: jwt-auth-setup
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, jwt-auth, jwt, authentication, token, credential, plugin]
level: practitioner
status: docs-checked
description: "Use jwt-auth in APISIX: credential key, secret and algorithm, token header, query and cookie names, claims_to_verify, anonymous consumer, and the 401 on a bad token."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/jwt-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jwt-auth setup

Credential (under a consumer) attributes:
- `key` (required): identifies the credential.
- `secret`: shared key for HS256/384/512; stored encrypted.
- `public_key`: PEM for asymmetric algorithms.
- `algorithm`: default `HS256`; also RS, ES, PS families and `EdDSA`.
- `exp`: 86400 seconds; `base64_secret`: false; `lifetime_grace_period`: 0.

Route attributes:
- `header` default `authorization`; `query` default `jwt`; `cookie` default `jwt`.
- `hide_credentials`: false; `anonymous_consumer`: optional.
- `claims_to_verify`: default `["exp","nbf"]`.
- `key_claim_name`: default `key` (for example `iss`).
- `store_in_ctx`: false; `realm`: `jwt`.

Create a credential:

```json
{"id":"cred-jack-jwt-auth","plugins":{"jwt-auth":{"key":"jack-key","secret":"<LONG_SECRET>"}}}
```

Enable on a route with `"jwt-auth":{}`. Generate the token yourself (for example at jwt.io) with the payload `{"key":"jack-key","nbf":<UNIX_TIME>}`, then call:

```shell
curl -i "http://127.0.0.1:9080/headers" -H "Authorization: ${jwt_token}"
```

Success is 200 and the upstream gets `X-Consumer-Username` and `X-Credential-Identifier`. A bad token returns 401 `{"message":"failed to verify jwt"}`.

## Checked

2026-11-04. Confirmed against the APISIX jwt-auth plugin page: credential and route attributes with defaults, algorithm list, claims_to_verify default, key_claim_name, realm, the X-Consumer-Username and X-Credential-Identifier headers, the 401 message, nbf in the payload, encrypted secret storage. Removed the unconfirmed note about writing `\n` in the public_key JSON string.

Method: documentation only; no commands were run.
