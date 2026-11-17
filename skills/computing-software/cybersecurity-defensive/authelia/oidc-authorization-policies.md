---
id: computing-software.cybersecurity-defensive.authelia.oidc-authorization-policies
name: oidc-authorization-policies
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, openid-connect, authorization-policy, rbac, deny, two-factor, access-denied]
level: advanced
status: docs-checked
description: "Gate OIDC clients with Authelia authorization_policies and the client authorization_policy field; access_control rules do not apply."
sources:
  - https://www.authelia.com/configuration/identity-providers/openid-connect/provider/
  - https://www.authelia.com/configuration/identity-providers/openid-connect/clients/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `access_control` section does not apply to OpenID Connect. Clients have their own policy.

A client's `authorization_policy` is `one_factor`, `two_factor` or the name of a custom policy defined under `identity_providers.oidc.authorization_policies`:

```yaml
identity_providers:
  oidc:
    authorization_policies:
      policy_name:
        default_policy: 'two_factor'
        rules:
          - policy: 'deny'
            subject: 'group:services'
    clients:
      - client_id: 'client_with_policy_name'
        authorization_policy: 'policy_name'
```

How it works:

- The policy applies only to authorization requests.
- Each custom policy has a `default_policy` and ordered `rules`; the first fully matching rule wins.
- A rule can use `deny`, which is available only here. When it matches, the user is not asked for consent and Authelia returns the OpenID Connect `access_denied` error.
- The documentation says this feature is not a substitute for access control in applications that lack it. The page generally recommends relying on the relying party for RBAC based on the available claims.
- The differences from access control rules are intentional and explained in the OpenID Connect FAQ and architecture decision record 1.

Use this for coarse gates, such as "admins only" or "require two-factor for this client". Anything finer belongs in the application.

Check: log in as a user in the denied group and confirm the client receives an `access_denied` error.

## Checked

2026-11-08. Confirmed against the OpenID Connect 1.0 Provider and Clients configuration pages (authorization_policies structure, default_policy, ordered rules, deny and access_denied, client authorization_policy values, FAQ and ADR1 pointers, access control note). Removed: the example claim name `groups`.

Method: documentation only; no commands were run.
