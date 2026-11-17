---
id: computing-software.cybersecurity-defensive.authelia.oidc-claims-policies-and-custom-scopes
name: oidc-claims-policies-and-custom-scopes
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, claims-policy, custom-scopes, id-token-claims, user-attributes, cel]
level: sme
status: docs-checked
description: "Define Authelia claims policies, custom scopes and CEL user attributes to supply claims clients expect, and know when to avoid them."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/provider/
  - https://www.authelia.com/configuration/definitions/user-attributes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three related features shape which claims clients receive.

User attribute definitions use Common Expression Language to derive attributes from existing data:

```yaml
definitions:
  user_attributes:
    is_admin:
      expression: '"admin" in groups'
    access_level:
      expression: '"admin" in groups ? 10 : 5'
```

The key becomes the attribute name and must not clash with backend extra attributes or common attributes. Extensions enabled include strings, lists, sets, math, encoders, bindings and regex.

Custom scopes add to the standard ones:

```yaml
identity_providers:
  oidc:
    claims_policies:
      app_roles_policy:
        custom_claims:
          is_admin:
            name: 'is_admin'
            attribute: 'is_admin'
    scopes:
      app_roles:
        claims: ['is_admin']
    clients:
      - client_id: '<CLIENT_ID>'
        claims_policy: 'app_roles_policy'
        scopes: ['openid', 'app_roles']
```

Every claim a scope lists must be a standard claim or one supplied by the client's `claims_policy`.

Claims policies are named under `claims_policies` and referenced by a client's `claims_policy` field. The `id_token` list copies claims into the ID token in addition to the standard ones, once the relevant scope is granted. The documentation calls this an escape hatch for clients that do not really support OpenID Connect, discourages it, and warns that clients linking users by claims other than `iss` and `sub` have a significant security flaw. `id_token_audience_mode` should normally stay unset.

Attributes `openid_authreq_claim_value` and `openid_authreq_claim_values` must not be used in security-sensitive logic unless requests are protected by JAR with encryption or by PAR.

Check: log in to a test client that requests the custom scope and confirm the claim appears in the ID token or userinfo response.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Provider configuration page (claims_policies id_token, access_token, custom_claims name and attribute, id_token_audience_mode, scopes claims rule, security notice) and the User Attributes page (CEL, default extensions, name conflict rule, authreq claim attributes notice). Changed: the scope example now includes the custom_claims mapping and client claims_policy that the page requires. Removed: an unsourced CLI command.

Method: documentation only; no commands were run.
