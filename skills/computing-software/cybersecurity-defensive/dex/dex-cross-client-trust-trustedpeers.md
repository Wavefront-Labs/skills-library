---
id: computing-software.cybersecurity-defensive.dex.dex-cross-client-trust-trustedpeers
name: dex-cross-client-trust-trustedpeers
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [trusted-peers, audience, azp, static-clients]
level: advanced
status: docs-checked
description: "Let one Dex client mint ID tokens for another with trustedPeers and the audience:server:client_id scope, producing aud and azp claims."
sources:
  - https://dexidp.io/docs/configuration/custom-scopes-claims-clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex can issue ID tokens to clients on behalf of other clients. The token's `aud` is then a different client id than the one that performed the login. A web app can, for instance, generate a token for a command line tool.

```yaml
staticClients:
- id: web-app
  redirectURIs:
  - 'https://web-app.example.com/callback'
  name: 'Web app'
  secret: web-app-secret
- id: cli-app
  redirectURIs:
  - 'https://cli-app.example.com/callback'
  name: 'Command line tool'
  secret: cli-app-secret
  trustedPeers:
  - web-app
```

The target client (`cli-app`) must explicitly trust the requester (`web-app`) through `trustedPeers`. The web app then requests the scope:

```
audience:server:client_id:cli-app
```

The resulting ID token includes:

```json
{ "aud": "cli-app", "azp": "web-app", "email": "foo@bar.com" }
```

A client secret can also come from an injected environment variable with `secretEnv` instead of `secret`.

Gotcha: the trust is declared on the audience client (`cli-app`), not on the requester.

## Checked

2026-11-08: Read the Dex Scopes and Claims page in full. Confirmed cross-client trust, the aud and azp claims, the trustedPeers example, the audience:server:client_id scope and secretEnv. Removed the Kubernetes API server use case and the one-directional claim, which that page does not state.
Method: documentation only; no commands were run.
