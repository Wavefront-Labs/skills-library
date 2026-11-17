---
id: computing-software.cybersecurity-defensive.zitadel.service-account-client-credentials
name: service-account-client-credentials
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, service-accounts, client-credentials, machine-to-machine, access-token]
level: practitioner
status: docs-checked
description: "Authenticate a ZITADEL service account with a client id and secret to get an access token, with the audience scopes for ZITADEL APIs."
sources:
  - https://zitadel.com/docs/guides/integrate/service-accounts/client-credentials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a service account under Service Accounts with New, a username and a display name. Open Actions in the top right and choose Generate Client Secret. Copy the ClientID and ClientSecret from the dialog immediately; the secret cannot be shown again, and a lost one means generating a new one.

Request a token from the token endpoint:

```bash
curl --request POST \
  --url https://${CUSTOM_DOMAIN}/oauth/v2/token \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data grant_type=client_credentials \
  --data scope='openid profile' \
  --user "$CLIENT_ID:$CLIENT_SECRET"
```

`grant_type` is `client_credentials`, and `scope` must include `openid`. Credentials go in basic authentication.

The response holds `access_token`, `token_type` (Bearer) and `expires_in` in seconds. By default the token is opaque.

Audience scopes matter:

- To call ZITADEL's own APIs, include `urn:zitadel:iam:org:project:id:zitadel:aud`.
- If your backend will validate the token by introspection, include `urn:zitadel:iam:org:project:id:{projectid}:aud` for your project. Without it introspection fails.

## Checked

2026-11-08. Read in full: the client credentials guide for service accounts. Removed the unsupported line about administrator roles and the comparison with other methods.

Method: documentation only; no commands were run.
