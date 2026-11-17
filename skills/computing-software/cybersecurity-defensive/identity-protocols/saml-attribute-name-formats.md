---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-attribute-name-formats
name: saml-attribute-name-formats
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-attribute-name-formats, saml-attributes, attribute, nameformat, friendlyname, oid, urn, identity-protocols]
level: practitioner
status: docs-checked
description: "Choose between uri, basic and unspecified NameFormat; use OID names with FriendlyName as a display hint only."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attribute NameFormat and FriendlyName

Goal: send attribute names the SP will recognise.

Method: `saml:Attribute Name=... NameFormat=...` (Name required, NameFormat and FriendlyName optional).
- `urn:oasis:names:tc:SAML:2.0:attrname-format:uri`: the name follows URI-reference convention; its interpretation is application-specific. The X.500/LDAP attribute profile requires this format with names built from the `urn:oid:` namespace, for example `urn:oid:2.5.4.3`.
- `urn:oasis:names:tc:SAML:2.0:attrname-format:basic`: the name must be a valid `xs:Name`.
- `urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified`: interpretation left to implementations. This is the default when NameFormat is omitted.

`FriendlyName` is a human-readable hint and MUST NOT be used to identify attributes. Under the X.500/LDAP profile two Attribute elements are the same attribute only if their Name values are equal, and FriendlyName plays no part.

Gotchas:
- The SP must be configured with exactly the Name and NameFormat the IdP sends; a Name sent under a different NameFormat is a different classification.
- Put each value of a multi-valued attribute in its own `AttributeValue` (RECOMMENDED). If any value has an `xsi:type`, all values of that attribute must have the identical type.
- An attribute that exists but has no values: omit `AttributeValue` inside an AttributeStatement.

Verify: decode the assertion and compare Name and NameFormat with the SP configuration.

## Checked

Method: 2026-11-09 docs-only; read SAML 2.0 core (OASIS PDF via pdftotext) 2.7.3.1 and 8.2, and profiles 8.2.2 to 8.2.2.1. Removed unsourced claims about Microsoft claim URIs, case-sensitivity of libraries and mail OID value.
