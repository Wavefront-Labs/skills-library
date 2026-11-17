---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-eduperson-attribute-profile
name: saml-eduperson-attribute-profile
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-eduperson-attribute-profile, saml-attributes, eduperson, x500, federation, identity-protocols]
level: advanced
status: docs-checked
description: "Use the SAML X.500/LDAP attribute profile to carry directory attributes such as eduPerson schema attributes: OID names, encoding, comparison."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X.500/LDAP attribute profile (carrying eduPerson and similar schemas)

Goal: express directory attributes (X.500, inetOrgPerson, eduPerson and private schemas) as SAML attributes interoperably.

Method (profiles 8.2, profile id `urn:oasis:names:tc:SAML:2.0:profiles:attribute:X500`):
- `NameFormat` MUST be `urn:oasis:names:tc:SAML:2.0:attrname-format:uri`; `Name` is `urn:oid:` plus the attribute type's OBJECT IDENTIFIER (RFC 3061), for example `urn:oid:2.5.4.3` (cn) or `urn:oid:2.5.4.42` (givenName).
- `FriendlyName` is optional and, if present, SHOULD be one of the attribute type's defined short names (for example givenName).
- Two Attribute elements are the same attribute if and only if their Name values are equal under RFC 3061; FriendlyName is ignored.
- Values: only for attributes with LDAP syntaxes. Syntaxes whose LDAP encoding is always UTF-8 text are carried as the text with `x500:Encoding="LDAP"`; for all other syntaxes the value is the base64 of the LDAP-encoded ASN.1 OCTET STRING, also with Encoding "LDAP".

Gotchas:
- The profile defines naming and encoding only; which eduPerson attributes to release, scoped-value rules and the OIDs of specific attributes come from the schema owner and federation policy, which this skill did not verify. Look up each OID in the schema file before configuring.

Verify: decode the assertion and confirm each Attribute has NameFormat uri and a urn:oid Name that matches the schema's OID.

## Checked

Method: 2026-11-09 docs-only; read SAML 2.0 profiles (OASIS PDF via pdftotext) section 8.2 in full. Removed specific eduPerson OIDs, shibmd:Scope and ePPN reassignment claims because the cited document does not state them.
