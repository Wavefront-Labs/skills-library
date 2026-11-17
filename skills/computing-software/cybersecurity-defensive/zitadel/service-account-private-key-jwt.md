---
id: computing-software.cybersecurity-defensive.zitadel.service-account-private-key-jwt
name: service-account-private-key-jwt
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, service-accounts, private-key-jwt, jwt-bearer, rfc7523]
level: advanced
status: docs-checked
description: "Authenticate a ZITADEL service account with a signed JWT using a generated key or your own uploaded public key."
sources:
  - https://zitadel.com/docs/guides/integrate/service-accounts/private-key-jwt
  - https://zitadel.com/docs/apis/openidoauth/grant-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This uses the `urn:ietf:params:oauth:grant-type:jwt-bearer` grant (RFC 7523) for non-interactive authentication.

How it works: a key pair is associated with the service account, ZITADEL stores the public key, and the client signs a JWT with the private key. The JWT's subject is the service account. The client sends it to the token endpoint as the assertion. ZITADEL validates the signature with the stored public key and returns an access token, which the client sends to the API in the Authorization header. A resource server validates it by token introspection.

Register a key in one of two ways:

- Option A: open the service account, go to the Keys tab, choose New, optionally set an expiration, then Download and keep the JSON file safe. ZITADEL cannot regenerate the private key.
- Option B: generate your own pair and upload only the public key through the User Service API.

```bash
openssl genrsa -out privatekey.pem 2048
openssl rsa -in privatekey.pem -pubout -out publickey.pem
```

The downloaded JSON has `type` (`serviceaccount`), `keyId`, `key` and `userId`.

You need a JWT library such as pyjwt for Python or jsonwebtoken for Node.js. With option B you upload only the public key.

## Checked

2026-11-08. Read in full: the private key JWT guide and the grant types page. Removed the unsupported claim that option B is the stronger choice.

Method: documentation only; no commands were run.
