---
id: computing-software.cybersecurity-defensive.zitadel.saml-concepts-for-sso
name: saml-concepts-for-sso
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, saml, sso, service-provider, identity-provider, assertions]
level: intro
status: docs-checked
description: "Learn the SAML terms ZITADEL's documentation relies on, such as service provider, ACS, assertions, relay state and metadata, before configuring SAML login."
sources:
  - https://zitadel.com/docs/guides/integrate/login/saml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SAML is a long-standing standard for identity federation and single sign-on. The documentation gives reasons to choose it: compatibility with legacy systems used since 2002, enterprise cases that need rich attributes and complex authorization, and a mature ecosystem. It also notes SAML can be prone to security flaws if implemented incorrectly.

Terms:

- Service Provider (SP): the application the user tries to sign in to.
- Identity Provider (IdP): the central point of authentication.
- SAML request: SP to IdP.
- SAML response: IdP to SP, carrying assertions about the user.
- Assertions: statements about the user, signed with XML signatures (DSig).
- Assertion Consumer Service (ACS): the SP endpoint that processes the response.
- Attributes: user information in the response.
- Relay State: lets the IdP remember where the user was before authentication.
- SAML trust: the settings between IdP and SP.
- Metadata: trust information exchanged between the two.

ZITADEL's documentation also has guides for adding external SAML identity providers such as Okta, OneLogin and Entra ID through identity brokering. Exchange metadata first, check the ACS URL, and verify that the attributes you map exist in the response.

## Checked
2026-11-08. Confirmed against the ZITADEL SAML guide: reasons to choose SAML, definitions of SP, IdP, assertions, ACS, attributes, relay state, trust and metadata, and Okta and Entra ID guides.
Method: documentation only; no commands were run.
