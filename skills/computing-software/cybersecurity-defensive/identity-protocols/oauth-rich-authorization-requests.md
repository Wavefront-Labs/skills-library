---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-rich-authorization-requests
name: oauth-rich-authorization-requests
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-rich-authorization-requests, oauth-par-jar-rar, rar, rfc9396, authorization_details, fine-grained, payments, identity-protocols]
level: sme
status: docs-checked
description: "Request fine-grained permissions with authorization_details JSON (type, actions, locations, datatypes) and handle consent and token presentation."
sources:
  - https://www.rfc-editor.org/rfc/rfc9396
  - https://www.rfc-editor.org/rfc/rfc9126
  - https://www.rfc-editor.org/rfc/rfc9101
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rich Authorization Requests (authorization_details)

Goal: express more than scope strings.

Method (RFC 9396): send an `authorization_details` parameter, a JSON array of objects, each with a required `type` field that identifies the authorization details type; the type defines the allowed contents of the object. Common fields defined by the RFC, usable across APIs, are `locations`, `actions`, `datatypes`, `identifier` and `privileges`. Example from the RFC's pattern: `authorization_details=[{"type":"payment_initiation","actions":["initiate"],"locations":["https://bank.example/payments"]}]`. In an authorization request the parameter is encoded with `application/x-www-form-urlencoded` of the serialised JSON; it can also be carried in a PAR request (RFC 9126) or in a JAR Request Object (RFC 9101). The AS uses the details to ask for consent. In the token response the AS MUST also return the `authorization_details` as granted by the resource owner and assigned to the access token. Server metadata: `authorization_details_types_supported`.

Gotchas:
- The `type` determines each object's contents, so the AS and RS must agree on the schema for every type they use; the RS enforces the details it receives.
- A token request can ask for "fewer permissions" on refresh; the AS checks the request against the underlying grant, so do not let a refresh or exchange widen the granted details.
- Consent rendering is the AS's job; the RFC notes that extension modules may render the consent for each type.

Verify: check the token response lists `authorization_details` exactly as the user consented to.

## Checked

Date: 2026-11-02. Confirmed in RFC 9396 (type, common fields, encoding, token response, token request and refresh handling, metadata), RFC 9126 and RFC 9101 (carriers). Removed as not stated there: the payment example's `instructedAmount` and `creditorName` values, the claim that details are returned in JWT access tokens, "truncated amounts are a vulnerability", and "consent screens must render details accurately".

Method: documentation only; no commands were run.
