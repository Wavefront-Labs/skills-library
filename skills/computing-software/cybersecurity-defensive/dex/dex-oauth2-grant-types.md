---
id: computing-software.cybersecurity-defensive.dex.dex-oauth2-grant-types
name: dex-oauth2-grant-types
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [oauth2, grant-types, password, device-code, token-exchange]
level: practitioner
status: docs-checked
description: "Enable or disable Dex grants with oauth2.grantTypes, and know the defaults and the special requirements of password and client credentials."
sources:
  - https://dexidp.io/docs/configuration/oauth2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`oauth2.grantTypes` lists the grants Dex accepts.

```yaml
oauth2:
  grantTypes:
    - "authorization_code"
    - "refresh_token"
    - "urn:ietf:params:oauth:grant-type:token-exchange"
```

Available values:

- `authorization_code`: recommended for web and mobile apps.
- `refresh_token`: obtain new tokens without user interaction.
- `password`: deprecated and less secure. Requires `passwordConnector` to be set.
- `client_credentials`: server to server. Requires the feature flag `DEX_CLIENT_CREDENTIAL_GRANT_ENABLED_BY_DEFAULT=true`.
- `urn:ietf:params:oauth:grant-type:token-exchange`: RFC 8693 exchange of external tokens.
- `urn:ietf:params:oauth:grant-type:device_code`: RFC 8628 device grant.

If `grantTypes` is not specified the defaults are `authorization_code`, `refresh_token` and the token-exchange grant.

Gotchas:

- Implicit flow is not a grant type here. Use `responseTypes`.
- Token exchange works with OIDC connectors. The device code flow needs additional configuration.

Token exchange and device grants need the supported upstream connector to be properly configured. Token exchange works with OIDC connectors, while the device code flow requires additional configuration.

## Checked

2026-11-03: read against Dex docs, OAuth2 configuration (https://dexidp.io/docs/configuration/oauth2/).

Removed or corrected: The inference that setting the list disables all others, the "OIDC only" wording and the Check step.

Method: documentation only; no commands were run.
