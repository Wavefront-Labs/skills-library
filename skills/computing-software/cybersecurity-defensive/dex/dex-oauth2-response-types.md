---
id: computing-software.cybersecurity-defensive.dex.dex-oauth2-response-types
name: dex-oauth2-response-types
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oauth2, response-types, implicit-flow, hybrid-flow]
level: practitioner
status: docs-checked
description: "Choose OAuth2 flows with oauth2.responseTypes: code, id_token, id_token token and the hybrid combinations."
sources:
  - https://dexidp.io/docs/configuration/oauth2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`responseTypes` selects which authentication flow Dex allows.

```yaml
oauth2:
  grantTypes: [ "authorization_code" ]
  responseTypes: [ "code" ]
```

Valid values and the flow each maps to:

| value | flow |
|---|---|
| `code` | Authorization Code Flow |
| `id_token` | Implicit Flow |
| `id_token token` | Implicit Flow |
| `code id_token` | Hybrid Flow |
| `code token` | Hybrid Flow |
| `code id_token token` | Hybrid Flow |

The flows themselves are described in the OpenID Connect specification.

Enable Implicit Flow through `responseTypes`, not `grantTypes`:

```yaml
oauth2:
  responseTypes: [ "id_token", "token" ]
```

Gotchas:

- Implicit Flow is not configured through `grantTypes`; use `responseTypes`.
- The page recommends the `authorization_code` grant for web and mobile applications.

## Checked

2026-11-08: Read the Dex OAuth2 page in full. Confirmed the responseTypes table, the config example, the grantTypes note for Implicit Flow and the authorization_code recommendation. Removed the rejection check and the does-nothing claim, which that page does not state.
Method: documentation only; no commands were run.
