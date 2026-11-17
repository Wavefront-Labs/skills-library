---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-assertion-structure
name: saml-assertion-structure
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-assertion-structure, saml-assertions, saml, assertion, issuer, authnstatement, attributestatement, conditions, identity-protocols]
level: practitioner
status: docs-checked
description: "Read a SAML 2.0 Assertion: Issuer, Subject, Conditions, AuthnStatement, AttributeStatement and the required attributes ID, Version and IssueInstant."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML assertion structure

Goal: know what every element of an assertion means so you can review or debug one.

- Required on `saml:Assertion`: `ID` (xs:ID, unique under the Core identifier rules), `Version="2.0"`, `IssueInstant` (UTC) and a `saml:Issuer`.
- `Subject` (optional in Core; profiles such as Web Browser SSO require it) holds an identifier plus zero or more `SubjectConfirmation` elements.
- `Conditions` carries `NotBefore`, `NotOnOrAfter` and `AudienceRestriction`; an assertion whose conditions are invalid, or Indeterminate (a condition cannot be evaluated or an element is not understood), must be rejected by the relying party.
- `AuthnStatement` records the required `AuthnInstant`, an optional `SessionIndex` and an `AuthnContext` describing how the user authenticated.
- `AttributeStatement` lists `Attribute` elements with `Name` and optional `NameFormat` and `FriendlyName`.

Gotchas:
- The Web Browser SSO profile requires the assertion to contain an `AuthnStatement` (with a bearer `SubjectConfirmation`).
- Time values are xs:dateTime in UTC form with no time zone component.

Verify: decode the response, confirm Issuer equals the metadata entityID, and that every condition passes at the current time.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Core to text and read 2.3.3 (Assertion attributes and Issuer), 1.3.3 (UTC), 2.5 (Conditions validity: Valid, Invalid, Indeterminate), 2.7 (AuthnStatement, Attribute) and Profiles 4.1.4.2. Removed the must-not-start-with-a-digit remark and the Z suffix claim (not stated); corrected Subject to optional in Core.
