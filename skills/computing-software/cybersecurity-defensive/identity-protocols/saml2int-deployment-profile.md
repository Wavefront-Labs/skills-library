---
id: computing-software.cybersecurity-defensive.identity-protocols.saml2int-deployment-profile
name: saml2int-deployment-profile
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml2int-deployment-profile, saml-conformance-interop, saml2int, interoperability, deployment-profile, kantara, conformance, identity-protocols]
level: advanced
status: docs-checked
description: "Apply the SAML2int deployment profile: metadata rules, bindings, signing and encryption, subject identifiers, SLO and clock skew for SPs and IdPs."
sources:
  - https://kantarainitiative.github.io/SAMLprofiles/saml2int.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML2int interoperability profile

Goal: configure SPs and IdPs the way the Kantara SAML2int profile requires.

General: allow 3 to 5 minutes of clock skew either way; limit string elements and attributes to 256 characters; never produce a DTD in a protocol message; name deployments by an absolute URI of at most 256 characters. Behaviour is provisioned solely from SAML metadata. Metadata must be verified by signature (strongly recommended) or TLS server certificate, MUST carry `validUntil` on the root (reject metadata without it or beyond a community threshold), and keys must be X.509 certificates in `KeyDescriptor` (RSA at least 2048 bits, 3072 recommended for new deployments; EC at least 256 bits). Metadata needs `mdui:UIInfo` with DisplayName and Logo (SP also PrivacyStatementURL), a technical ContactPerson with email, and for IdPs an https `errorURL`.

SP (Web Browser SSO):
- AuthnRequest goes by HTTP-Redirect; no frames or anything needing third-party cookies; omit `NameIDPolicy` (recommended) or use AllowCreate true with no Format; use `AssertionConsumerServiceURL` (exact match to metadata), never `AssertionConsumerServiceIndex`.
- Omit `RequestedAuthnContext` unless specific class refs are required; then use Comparison `exact`.
- Receive Response by HTTP-POST over TLS; must decrypt `EncryptedAssertion`; must not require a NameID; for persistent identification support the SAML Subject Identifier attributes (subject-id or pairwise-id), and tie identifier scopes to authorised IdPs (the `shibmd:Scope` extension is recommended).
- Support multiple IdP signing certificates and multiple decryption keys; allow more than one IdP per application; support deep linking.

IdP:
- Receive AuthnRequest by HTTP-Redirect over TLS; accept unsigned requests unless SP metadata sets `AuthnRequestsSigned`; verify any signature; check `AssertionConsumerServiceURL` against metadata (case-sensitive comparison recommended, else use the default endpoint).
- Honour `ForceAuthn` with a fresh `AuthnInstant`, or fail.
- Send Response by HTTP-POST; successful responses are signed on the Response; exactly one assertion with exactly one AuthnStatement and at most one AttributeStatement; assertions are encrypted (`EncryptedAssertion`) with no EncryptedID or EncryptedAttribute inside; include a transient NameID (for logout).
- Support subject-id and/or pairwise-id; list scopes in metadata with `shibmd:Scope` and no regexps; Attribute NameFormat is `urn:oasis:names:tc:SAML:2.0:attrname-format:uri`; one `AttributeValue` per value.

Single Logout: the IdP MUST support SLO; LogoutRequest and LogoutResponse use HTTP-Redirect and are signed; the NameID is unencrypted and must exactly match the one received; an SP ends its local session before sending LogoutRequest and must not send one on idle timeout.

Gotchas:
- This is a deployment profile, not the OASIS conformance document; the OASIS conformance PDF was not read and was dropped as a source.
- The algorithm list and the required metadata element lists were not read in full.

Verify: test against two independent implementations and check each MUST above against the metadata and traces.

## Checked

Method: 2026-11-09 docs-only; fetched saml2int.html and read every normative sentence by search for MUST/SHOULD/RECOMMENDED (the algorithm table and metadata bullet lists were not read). Corrected earlier claims: SLO is required of IdPs (not optional), NameID is transient with subject-id or pairwise-id for persistence, and SPs must not require a NameID. Dropped the mdattr claim.
