---
id: computing-software.cybersecurity-defensive.identity-protocols.saml-authnrequest-fields
name: saml-authnrequest-fields
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [saml-authnrequest-fields, saml-authn-request-response, authnrequest, forceauthn, ispassive, assertionconsumerserviceurl, destination, identity-protocols]
level: practitioner
status: docs-checked
description: "Set AuthnRequest fields correctly: ID, Destination, AssertionConsumerServiceURL, ProtocolBinding, ForceAuthn, IsPassive and NameIDPolicy."
sources:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf
  - https://docs.oasis-open.org/security/saml/v2.0/saml-metadata-2.0-os.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AuthnRequest attributes and elements

Goal: build or audit an `samlp:AuthnRequest`.

- `ID` unique, `Version="2.0"`, `IssueInstant`, `Destination` = the address the request was sent to; if present, the recipient must check it matches where it was received and discard the request if not.
- `AssertionConsumerServiceURL` (by value, usually with `ProtocolBinding`) or `AssertionConsumerServiceIndex` (indirect) choose where the response goes; the two forms are mutually exclusive, and `ProtocolBinding` is also exclusive with the index. The responder must ensure by some means that a URL given by value is really associated with the requester (SP metadata, or signing the AuthnRequest). An IdP that accepts arbitrary ACS URLs can send assertions to an attacker.
- `ForceAuthn="true"` requires the IdP to authenticate the user directly rather than rely on a previous security context (default false); `IsPassive="true"` forbids the IdP and user agent from visibly taking over the UI (default false), and an IdP that cannot comply answers with status `NoPassive`.
- `Issuer` identifies the requester. `NameIDPolicy` and `Scoping` are optional.

Gotchas:
- ForceAuthn only forces direct authentication; it does not say how strong it must be. Use RequestedAuthnContext for that.
- If both ForceAuthn and IsPassive are true, the IdP must not freshly authenticate the user unless the IsPassive constraints can be met.
- SP metadata `AuthnRequestsSigned="true"` declares that the SP signs its requests (false if omitted).

Verify: capture the request and confirm the ACS URL is in metadata.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Converted SAML V2.0 Core to text and read the AuthnRequest definition (Destination, ForceAuthn, IsPassive, AssertionConsumerServiceIndex/URL, ProtocolBinding, NameIDPolicy, Scoping) and the NoPassive status; read SAML Metadata for AuthnRequestsSigned. Reworded the ForceAuthn/IsPassive and ACS claims to match the spec.
