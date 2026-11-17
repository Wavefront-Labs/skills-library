---
id: computing-software.software-engineering.api-design.openapi-security-schemes
name: openapi-security-schemes
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, openapi, security-schemes, bearer-auth, oauth2, openidconnect, api-key, mutualtls]
level: practitioner
status: docs-checked
description: "Declare authentication in OpenAPI 3.1: securitySchemes, security requirements, bearer, apiKey, oauth2 flows, openIdConnect, mutualTLS, overrides."
sources: ["https://spec.openapis.org/oas/v3.1.0"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI security schemes

Define schemes once under `components.securitySchemes`, then require them globally or per operation.

```yaml
components:
  securitySchemes:
    bearerAuth: { type: http, scheme: bearer, bearerFormat: JWT }
    apiKey:     { type: apiKey, in: header, name: X-API-Key }
    oauth:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.test/authorize
          tokenUrl: https://auth.example.test/token
          scopes: { 'orders:read': Read orders, 'orders:write': Modify orders }
    oidc: { type: openIdConnect, openIdConnectUrl: https://auth.example.test/.well-known/openid-configuration }
    mtls: { type: mutualTLS }
security:                              # global default
  - bearerAuth: []
paths:
  /health:
    get: { security: [] , responses: { '200': { description: OK } } }   # public override
  /orders:
    post: { security: [ { oauth: ['orders:write'] } ], responses: { '201': { description: Created } } }
```

## Semantics
- Entries in the `security` list are alternatives (OR: one entry must be satisfied); schemes inside one entry are combined (AND: all must be satisfied).
- An empty array (`security: []`) removes the top-level declaration; omitting `security` on an operation inherits it. An empty entry `{}` in the list makes security optional.
- For oauth2/openIdConnect the value is the list of required scope names (may be empty). For other types it may list role names, which are not defined or exchanged in-band; otherwise use `[]`.
- Valid `type` values: `apiKey`, `http`, `mutualTLS`, `oauth2`, `openIdConnect`. `apiKey` needs `name` and `in` (`query`, `header` or `cookie`); `http` needs `scheme` (use values from the IANA Authentication Scheme registry); `bearerFormat` is only a documentation hint; `oauth2` needs `flows`; `openIdConnect` needs `openIdConnectUrl`.
- OAuth flow keys: `implicit`, `password`, `clientCredentials`, `authorizationCode`. `authorizationUrl` is required for `implicit` and `authorizationCode`, `tokenUrl` for `password`, `clientCredentials` and `authorizationCode`, and `scopes` (may be empty) always.

## Gotchas
- The spec only describes the schemes; whether a request is authorized is enforced in the gateway or code, not by the document.
- The spec notes the implicit flow is about to be deprecated by the OAuth 2.0 Security Best Current Practice, and recommends the Authorization Code flow with PKCE for most uses.

Verify: lint the document and confirm every non-public operation resolves to a non-empty effective security requirement.

## Checked
2026-11-08. Confirmed by reading the Security Scheme, OAuth Flows, OAuth Flow and Security Requirement sections and the `security` field text of the OpenAPI 3.1.0 specification (rest of the page searched only). Removed: the "added in 3.1" remark on mutualTLS, "other types must use []" (the spec allows role names), the claim that `password` is deprecated (the spec only says this of implicit), and the Spectral rule names (not in the sources).
Method: documentation only; no commands were run.
