---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-entity-descriptor
name: saml-entity-descriptor
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-entity-descriptor, saml-metadata, metadata, entitydescriptor, idpssodescriptor, spssodescriptor, entityid, identity-protocols]
level: practitioner
status: docs-checked
description: "Author and read SAML metadata: entityID, endpoints with bindings, NameIDFormat, WantAssertionsSigned and AuthnRequestsSigned flags."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EntityDescriptor, IDPSSODescriptor and SPSSODescriptor

Goal: produce correct metadata for an SP or IdP.

SP essentials: `EntityDescriptor entityID` (a unique URI of at most 1024 characters), `SPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol"`, `AuthnRequestsSigned`, `WantAssertionsSigned`, one or more `AssertionConsumerService` (Binding, Location, index, isDefault), optional `SingleLogoutService`, `NameIDFormat`.
IdP essentials: `IDPSSODescriptor` with `WantAuthnRequestsSigned`, `SingleSignOnService` per binding, `SingleLogoutService`, `KeyDescriptor`.

Gotchas:
- The entityID must be unique across all entities in a deployment, and one URI must not refer to different entities. It may be a URN; only metadata published at a well-known location needs it to be a URL, and then https is strongly recommended.
- `protocolSupportEnumeration` is required on each role descriptor; `Binding` and `Location` are required on endpoints; `index` is required on `AssertionConsumerService`, and `isDefault` marks the default one.
- Published metadata documents should be signed (see saml-metadata-exchange-refresh); consumers must validate signatures that are present.

Verify: validate against the metadata XSD and load it into the peer.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Metadata to text and read entityIDType (1024 characters, uniqueness), the endpoint, role descriptor, SPSSODescriptor and IDPSSODescriptor attribute definitions and section 4. Removed the claims that changing entityID breaks persistent NameIDs, that locations must be https, and that an ACS with HTTP-Redirect is invalid (not stated there).
