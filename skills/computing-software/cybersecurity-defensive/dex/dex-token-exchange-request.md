---
id: computing-software.cybersecurity-defensive.dex.dex-token-exchange-request
name: dex-token-exchange-request
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [token-exchange, curl, subject-token, connector-id]
level: advanced
status: docs-checked
description: "Call the Dex /token endpoint for a token exchange with connector_id, grant_type, subject_token and Basic client auth."
sources:
  - https://dexidp.io/docs/guides/token-exchange/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Perform an `application/x-www-form-urlencoded` POST to Dex's `/token` endpoint, following RFC 8693 section 2.1. Dex adds two requirements: the `connector_id` parameter, and the client id and secret as the username and password of Basic auth.

```bash
curl https://dex.example.com/token   --user my-app:my-secret   --data-urlencode connector_id=my-upstream   --data-urlencode grant_type=urn:ietf:params:oauth:grant-type:token-exchange   --data-urlencode scope="openid groups federated:id"   --data-urlencode requested_token_type=urn:ietf:params:oauth:token-type:access_token   --data-urlencode subject_token=$UPSTREAM_TOKEN   --data-urlencode subject_token_type=urn:ietf:params:oauth:token-type:access_token
```

Successful response:

```json
{
  "access_token": "eyJhbGciOi....aU5oA",
  "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
  "token_type": "bearer",
  "expires_in": 86399
}
```

Gotcha: regardless of the `requested_token_type`, the token is always returned in the `access_token` field. Read `issued_token_type` to see which kind it is (RFC 8693 section 2.2.1).

The guide's example requests `scope="openid groups federated:id"`, and its connector config lists `groups` and `federated:id` as additional scopes.

Dex issued tokens are bound to clients, so the Basic auth pair identifies the client the issued token belongs to. The caller therefore needs the client id and secret, which is why the docs make the client public for this flow. Repeat the exchange when the token expires.

## Checked

2026-11-08: Read the Dex Machine Authentication guide in full. Confirmed the POST to /token, the RFC 8693 references, connector_id, Basic client auth, the curl example, the response format and the access_token field behaviour. Removed the claims check, which that page does not state.
Method: documentation only; no commands were run.
