---
id: computing-software.cybersecurity-defensive.authentik.provider-saml
name: provider-saml
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, saml-provider, nameid, property-mappings, assertion-encryption, forceauthn]
level: advanced
status: docs-checked
description: "authentik SAML provider reference: endpoints, metadata, EntityID override, signing and encryption certificates, property mappings, NameID policies and ForceAuthn."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/saml/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make authentik a SAML2 identity provider for a service provider (SP).

## Endpoints
Unified SSO + SLO endpoint `/application/saml/<application_slug>/` (HTTP Redirect or POST, detected from the message), IdP-initiated `/application/saml/<application_slug>/init/`, metadata `/application/saml/<application_slug>/metadata/`. Older `/sso/binding/...` and `/slo/binding/...` paths still work.

Import SP metadata to configure a provider automatically; export authentik metadata to the SP.

## EntityID/Issuer override
Default Issuer/EntityID is the metadata URL. The override (under **Advanced protocol settings**; formerly "Issuer") is only for SPs requiring another value. Do not clear it without updating the SP's IdP Entity ID.

## Certificates
Signing certificate signs assertions/responses (choose signing and digest algorithms such as RSA-SHA256, SHA-256); verification certificate validates signed SP requests; encryption certificate encrypts sensitive assertion data for the SP, which decrypts it with its private key.

## Property mappings
Fields: Name, SAML Attribute Name, Friendly Name, Python Expression. Defaults (removable) cover Email, Groups, Name, UPN, User ID, Username and WindowsAccountName; view them with the **Managed** filter set to All. Split names:
```python
return request.user.name.rsplit(" ", 1)[-1]   # surname
return request.user.name.split(" ", 1)[0]     # givenname
```
(attribute names `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` and `.../givenname`).

## NameID
**NameID Property Mapping** overrides the SP's policy. Default policy: Persistent (hashed ID), X509 Subject (`distinguishedName`, falls back to persistent), Windows (UPN), Transient (session ID), Email address. Avoid email as NameID since users can change it.

## ForceAuthn and AuthnContextClassRef
Since 2026.8 an `AuthnRequest` with `ForceAuthn="true"` sends the user through the authentication flow again (provider flow, else brand flow); if users are prompted more often after upgrade, check the SP. AuthnContextClassRef comes from the **AuthnContextClassRef Property Mapping**, else from how the user authenticated.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/saml/.
Removed as not confirmed by that page: EncryptedAssertion wording, sign/encrypt ordering and AES encryption algorithm field.
Method: documentation only; no commands were run.
