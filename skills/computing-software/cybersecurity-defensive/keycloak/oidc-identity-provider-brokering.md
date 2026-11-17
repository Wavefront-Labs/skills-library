---
id: computing-software.cybersecurity-defensive.keycloak.oidc-identity-provider-brokering
name: oidc-identity-provider-brokering
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, identity-brokering, oidc-idp, client-authentication, issuer]
level: practitioner
status: docs-checked
description: "Add an external OpenID Connect identity provider to a Keycloak realm with endpoint URLs, client authentication, issuer validation and scope settings."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/identity-broker/oidc.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# oidc identity provider brokering
Brokering lets users log in through an external OIDC provider. In the admin console choose *Identity Providers* > *OpenID Connect v1.0*, then enter the options or import them from a URL or file pointing to OpenID Provider Metadata (for a Keycloak IdP: `<root>/realms/<realm>/.well-known/openid-configuration`).

Settings documented:
- **Authorization URL**, **Token URL**, optional **Logout URL**, **User Info URL**.
- **Backchannel Logout**: out-of-band REST request to the IdP; some IdPs log out through browser redirects only.
- **Client Authentication**: method used with the authorization code flow. For JWT signed with a private key, Keycloak uses the realm private key; otherwise define a client secret.
- **Client ID** and **Client Secret** (secret from an external vault) for the authorization code flow.
- **Client Assertion Signature Algorithm**: required for JWT signed with private key or client secret as JWT; defaults are RS256 for the private-key JWT and HS256 for client secret as JWT. **Client Assertion Audience** defaults to the IdP's token endpoint URL.
- **Issuer**: Keycloak validates issuer claims in IdP responses against this value.
- **Default Scopes**: space-separated; default `openid`.
- **Prompt** and **Accepts prompt=none forward from client**; **Requires short state parameter** for IdPs that cannot handle long `state` values.
- **Validate Signatures** with **Use JWKS URL** / **JWKS URL**, or **Validating Public Key** and **Validating Public Key Id** when JWKS is off. Backchannel logout tokens are always validated.

## Checked
2026-11-03. Confirmed against server_admin/topics/identity-broker/oidc.adoc (configuration table). Removed (not on the page): the `/broker/<alias>/endpoint` redirect URI, the Trust Email takeover warning, the "empty Issuer skips validation" claim and the Verify step.
Method: documentation only; no commands were run.
