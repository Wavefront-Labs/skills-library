---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-nameid-formats
name: saml-nameid-formats
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-nameid-formats, saml-assertions, nameid, persistent, transient, emailaddress, spnamequalifier, nameidpolicy, identity-protocols]
level: practitioner
status: docs-checked
description: "Choose between persistent, transient, emailAddress and unspecified NameID formats, and set NameIDPolicy and SPNameQualifier to avoid account-linking mistakes."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NameID formats and subject identifiers

Goal: pick a NameID that is stable, unique and not re-assignable.

Formats (prefix `urn:oasis:names:tc:SAML:2.0:nameid-format:` or `urn:oasis:names:tc:SAML:1.1:nameid-format:`):
- `persistent`: opaque, pseudo-random, pair-wise pseudonym for an IdP and an SP (or affiliation of SPs), at most 256 characters; the usual choice for account linking. `SPNameQualifier` names the SP or affiliation it was generated for. It must not be shared in clear text with other providers or appear in logs without appropriate controls.
- `transient`: an opaque, temporary value the relying party should not keep; at most 256 characters.
- `emailAddress` (1.1): an RFC 2822 addr-spec (local-part@domain). The spec does not say an address stays with one person, so do not make it your only key (practice, not from the spec).
- `unspecified`: interpretation is left to the implementation; document what your IdP sends.

Method: the SP asks via `NameIDPolicy Format=... AllowCreate="true"`. `AllowCreate` defaults to false, which limits the IdP to principals it has already established an identifier for; set it to true to let the IdP create one (mainly useful with `persistent`). If the NameIDPolicy is not acceptable to the IdP, it must return an error Status, which may carry the second-level code `InvalidNameIDPolicy`. If `Format` is omitted or `unspecified`, the IdP may return any kind of identifier.

Gotchas:
- Matching local accounts on a reusable email lets a new owner of an address inherit an old account.
- The persistent identifier's `NameQualifier` (the IdP that created it) stays fixed for the life of the identifier, so store it with the value.

Verify: log in twice and confirm persistent is identical, transient differs.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted the SAML V2.0 Core PDF to text and read section 8.3 (NameID format URIs: unspecified, emailAddress, persistent, transient) and the NameIDPolicy definition (Format, SPNameQualifier, AllowCreate default, InvalidNameIDPolicy). Removed the claim that persistent IDs change if the IdP entityID changes (the spec says NameQualifier is permanently established).
