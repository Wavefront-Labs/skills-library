---
id: computing-software.cybersecurity-defensive.dex.dex-kubernetes-oidc-api-server-flags
name: dex-kubernetes-oidc-api-server-flags
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [kubernetes, oidc, kube-apiserver, flags]
level: practitioner
status: docs-checked
description: "Point the Kubernetes API server at Dex with the --oidc-* flags: issuer URL, client id, CA file, username and groups claims."
sources:
  - https://dexidp.io/docs/guides/kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubernetes can use Dex as an OpenID Connect token authenticator. A client logs the user in through Dex, then presents the ID token as a bearer token to the API server, which verifies it with Dex's public keys. A claim becomes the username, and optionally groups, which RBAC can then authorise.

Flags for the API server, valid on all Kubernetes versions:

```
--oidc-issuer-url=https://dex.example.com:32000
--oidc-client-id=example-app
--oidc-ca-file=/etc/ssl/certs/openid-ca.pem
--oidc-username-claim=email
--oidc-groups-claim=groups
```

Points to know:

- Dex has to run on HTTPS, and custom CA files must be readable by the API server.
- Dex must be reachable from both your browser and the API server, but it does not have to be up when the API server starts. The server fetches Dex's keys at the beginning; other authenticators such as client certificates still work.
- For each bearer token the API server checks the signature, expiry, and claims (`aud`, `iss`), then reads subject attributes.
- If a claim other than `email` is used for the username, such as `sub`, it is prefixed with the issuer URL to namespace user-controlled claims that could be used for privilege escalation.
- These flags trust ID tokens issued to a single client. Use cross-client trust to let other clients mint tokens for it.

## Checked
2026-11-09: read the Dex Kubernetes Authentication guide in full; the flags, prerequisites, token checks, issuer-prefix rule for non-email claims and single-client limitation all match.
Method: documentation only; no commands were run.
