---
id: computing-software.cybersecurity-defensive.dex.dex-oidc-connector-basics
name: dex-oidc-connector-basics
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oidc, connector, issuer, upstream]
level: practitioner
status: docs-checked
description: "Use an upstream OpenID Connect provider with the Dex oidc connector: issuer, issuerAlias, credentials, scopes, basicAuthUnsupported."
sources:
  - https://dexidp.io/docs/connectors/oidc/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `oidc` connector lets Dex authenticate against another OpenID Connect provider such as Google Accounts, Salesforce or Azure AD v2 (not v1).

```yaml
connectors:
- type: oidc
  id: google
  name: Google
  config:
    issuer: https://accounts.google.com
    clientID: $GOOGLE_CLIENT_ID
    clientSecret: $GOOGLE_CLIENT_SECRET
    redirectURI: http://127.0.0.1:5556/dex/callback
    scopes:
    - profile
    - email
```

- `issuer`: canonical URL of the provider, also used for discovery. It must match the value returned in the provider's discovery document.
- `issuerAlias`: for off-spec providers (Azure, Oracle IDCS) whose discovery URL differs from the issuer, which makes issuer validation fail. It overrides the issuer from `.well-known/openid-configuration`.
- `redirectURI`: Dex's issuer URL plus `/callback`.
- `basicAuthUnsupported: true`: send `client_secret` in POST parameters for providers that need it.
- `scopes`: defaults to profile and email.
- `insecureSkipEmailVerified: true`: for providers that omit `email_verified`.
- `promptType`: for `offline_access` Dex sets `prompt=consent` by default, which not all providers support (some use `login` or `none`).

Gotcha: values starting with `$` are read from the environment.

## Checked

2026-11-03: read against Dex docs, OpenID Connect connector (https://dexidp.io/docs/connectors/oidc/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.
