---
id: computing-software.cybersecurity-defensive.zitadel.identity-brokering-and-sso
name: identity-brokering-and-sso
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, identity-brokering, federation, oidc, saml, ldap]
level: intro
status: docs-checked
description: "Explain how ZITADEL acts as an identity broker for OIDC, SAML and LDAP providers, with just-in-time user creation, and how it differs from plain SSO."
sources:
  - https://zitadel.com/docs/concepts/features/identity-brokering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Identity brokering connects external identity providers to your central ZITADEL so applications trust one issuer instead of building a trust relationship with every provider. Compatibility rests on standard protocols: OpenID Connect, SAML 2.0 and LDAP.

The documented flow:

1. An unauthenticated user opens an application.
2. The application redirects to ZITADEL.
3. Based on the tenant's settings ZITADEL shows the configured providers, or redirects directly to the primary external provider, for example Entra ID.
4. After authentication the user returns to ZITADEL. If the user does not exist yet, ZITADEL creates it just in time and links it to the external identity.
5. ZITADEL issues its own token to the application, exactly as for a local login.

Single sign-on means logging in once at a central provider and reaching several applications without logging in again. Brokering means users log in with external providers that have an established trust with your provider. SSO can be implemented as part of a brokering solution.

Practical effect: adding a provider is a ZITADEL configuration change. Your applications keep validating tokens from the one issuer.

## Checked

2026-11-08. Read the identity brokering page in full.

Method: documentation only; no commands were run.
