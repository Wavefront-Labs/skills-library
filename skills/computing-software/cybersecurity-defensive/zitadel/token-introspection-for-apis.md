---
id: computing-software.cybersecurity-defensive.zitadel.token-introspection-for-apis
name: token-introspection-for-apis
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, introspection, resource-server, api, oauth]
level: practitioner
status: docs-checked
description: "Protect an API by registering it in ZITADEL and validating access tokens through the introspection endpoint with JWT profile or basic auth."
sources:
  - https://zitadel.com/docs/guides/integrate/token-introspection
  - https://zitadel.com/docs/guides/integrate/token-introspection/basic-auth
  - https://zitadel.com/docs/guides/integrate/service-accounts/client-credentials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Token introspection checks whether an access token is valid. The API is separate from the front end and should not care whether it received a JWT or an opaque token; both work. What matters is how the API authenticates to the introspection endpoint: JWT profile (recommended) or basic authentication.

Register the API: in your project choose New, give a name, choose type API, then select the authentication method. With Basic you receive a Client ID and Client Secret. Under URLs note the issuer, token endpoint and introspection endpoint, and note the Project ID.

Basic request:

```bash
curl --request POST \
  --url ${CUSTOM_DOMAIN}/oauth/v2/introspect \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --header 'Authorization: Basic {your_basic_auth_header}' \
  --data token=VjVxyCZmRmWYqd3_F5db9Pb9mHR5fqzhn...
```

The header is `Basic ` plus base64 of the form-encoded client id and secret. Introspection works for opaque tokens and JWTs, and ensures they are not revoked.

Machine callers of your API, other systems that need to access it, must be declared as service accounts, not applications. If tokens for service accounts are introspected, request the scope `urn:zitadel:iam:org:project:id:{projectid}:aud` when getting them, or introspection fails.

## Checked

2026-11-08. Read in full: the token introspection overview, the basic authentication introspection guide and the client credentials guide. Removed the claim that revocation is detected by a client or by logout, and the comparison with local JWT validation; the pages only say introspection ensures tokens are not revoked.

Method: documentation only; no commands were run.
