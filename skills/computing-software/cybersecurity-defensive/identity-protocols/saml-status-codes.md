---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-status-codes
name: saml-status-codes
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-status-codes, saml-authn-request-response, status, statuscode, authnfailed, nopassive, requester, responder, identity-protocols]
level: practitioner
status: docs-checked
description: "Interpret the Status element: top-level Success, Requester, Responder, VersionMismatch and second-level codes such as AuthnFailed, NoPassive and InvalidNameIDPolicy."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAML response status codes

Goal: diagnose failed SSO from the Status in the response.

Top-level codes (`urn:oasis:names:tc:SAML:2.0:status:`): `Success`, `Requester` (the request was wrong), `Responder` (IdP-side failure), `VersionMismatch`.
Second-level codes nest inside: `AuthnFailed`, `InvalidAttrNameOrValue`, `InvalidNameIDPolicy`, `NoAuthnContext`, `NoAvailableIDP`, `NoPassive`, `NoSupportedIDP`, `PartialLogout`, `ProxyCountExceeded`, `RequestDenied`, `RequestUnsupported`, `UnknownPrincipal`, `UnsupportedBinding`; the spec defines more, for example `RequestVersionTooHigh` and `TooManyResponses`.
`StatusMessage` is free text for humans and `StatusDetail` carries extra XML.

Gotchas:
- Do not show StatusMessage to end users verbatim; log it.
- `Requester` errors are fixed in SP config or metadata; `Responder` errors go to the IdP admin.

Verify: reproduce each code with a bad NameIDPolicy, a passive request and a disabled user.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read SAML V2.0 Core (saml-core-2.0-os, status code section): every top-level and second-level URI listed is defined there, and so are StatusMessage and StatusDetail. Removed the claim that failed responses carry no assertion (not confirmed).
