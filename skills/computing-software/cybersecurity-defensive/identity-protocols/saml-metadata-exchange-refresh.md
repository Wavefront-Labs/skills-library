---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-metadata-exchange-refresh
name: saml-metadata-exchange-refresh
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-metadata-exchange-refresh, saml-metadata, validuntil, cacheduration, mdq, metadata-refresh, signed-metadata, identity-protocols]
level: advanced
status: docs-checked
description: "Distribute and refresh SAML metadata: signed metadata, validUntil, cacheDuration, well-known URL publication and trust in the document."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata exchange, validUntil and cacheDuration

Goal: keep trust data current without manual uploads.

Method:
- The root element of a metadata instance must carry `validUntil` (expiration time of the metadata) or `cacheDuration` (maximum time a consumer should cache it, an xs:duration); the spec recommends that only the root element carries them.
- Published metadata documents should be signed (enveloped XML signature on the element, referencing its ID attribute), and a consumer must validate signatures when present. The publisher must use a document-integrity mechanism; trust can also come from TLS server authentication of the metadata URL or a signed DNS zone.
- An entity may publish its metadata at a well-known location: the URL that is its entityID, https strongly recommended, content type `application/samlmetadata+xml`, root an `EntityDescriptor` whose entityID matches the location.
- Aggregates use `md:EntitiesDescriptor` containing many entities, but it must not be used in documents published at a well-known location.

Gotchas:
- Transport for retrieving metadata should provide server authentication and integrity protection (HTTP-based resolution should use TLS); relying parties should have some means to establish trust in metadata before relying on it.
- A cached document may not carry its TLS trust, so other mechanisms such as signatures should be used for it.
- Plan renewals before `validUntil` passes (practice).

Verify: set a short validUntil in a test and confirm the consumer refuses stale metadata.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Metadata to text and read EntitiesDescriptor (validUntil, cacheDuration, root rule), section 3.1 (signature profile) and section 4 (well-known location publication, trust processing). Removed the Metadata Query Protocol URL forms and the PT6H example (not in this specification), plus the claim that an expired file makes an SP reject the IdP.
