---
id: computing-software.cybersecurity-defensive.dex.dex-supported-scopes
name: dex-supported-scopes
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [scopes, openid, groups, offline-access]
level: practitioner
status: docs-checked
description: "List the scopes Dex supports: openid, email, profile, groups, federated:id, offline_access and audience:server:client_id."
sources:
  - https://dexidp.io/docs/configuration/custom-scopes-claims-clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs give an exhaustive list of scopes Dex supports:

- `openid`: required for all login requests.
- `email`: ID token claims include the user's email and whether the upstream provider verified it.
- `profile`: claims include the username.
- `groups`: claims include a list of groups the user belongs to.
- `federated:id`: claims include information from the ID provider, the connector id and the user id assigned there.
- `offline_access`: the token response includes a refresh token. It does not work with some connectors, notably the SAML connector ignores it.
- `audience:server:client_id:(client-id)`: dynamic scope asking for an ID token issued on behalf of another client (see the cross-client trust skill).

Example scope request from a client:

```
scope=openid email groups offline_access
```

Gotchas:

- The `offline_access` scope does not work with some connectors; check the connector's page.

## Checked

2026-11-08: Read the Dex Scopes and Claims page in full. Confirmed the scope list, each description, the SAML offline_access note and the audience dynamic scope. Removed connector-specific group settings and upstream default scopes, which that page does not state.
Method: documentation only; no commands were run.
