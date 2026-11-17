---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-iss-response-parameter
name: oauth-iss-response-parameter
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-iss-response-parameter, oauth-metadata-issuer, rfc9207, iss-parameter, mix-up, authorization-response, issuer-identification, identity-protocols]
level: advanced
status: docs-checked
description: "Return and check the iss parameter in authorization responses to defeat mix-up attacks, with the metadata flag authorization_response_iss_parameter_supported."
sources:
  - https://www.rfc-editor.org/rfc/rfc8414
  - https://www.rfc-editor.org/rfc/rfc9207
  - https://www.rfc-editor.org/rfc/rfc9728
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Issuer identification in authorization responses (RFC 9207)

Goal: let the client know which AS answered.

Method: the AS adds `iss=<issuer identifier>` to the authorization response (success and error) and advertises `authorization_response_iss_parameter_supported: true`. The client compares it by simple string comparison to the issuer of the AS the request was sent to (the `issuer` in its metadata); if the AS advertises support and `iss` is absent or does not match, reject the response. Alternatives are an `iss` claim in an ID Token or JARM response, or a distinct redirect URI per AS (RFC 9700).

Gotchas:
- The comparison is simple string comparison (RFC 3986 section 6.2.1) after decoding the form encoding.
- Mix-up attacks matter only to clients that use more than one AS; accepted `iss` values must be unique per AS.
- A client using servers with and without support must remember which AS supports it; whether to accept an `iss` from a server that does not advertise support is local policy.

Verify: swap the iss value in a test callback and confirm the client rejects.

## Checked

2026-11-02. Confirmed against RFC 9207 sections 2 to 4 (`iss` in success and error responses, metadata flag with default false, simple string comparison, rejection rules, uniqueness of issuers) and RFC 9700 sections 2.1 and 4.4.2 (alternatives). Removed: the claim that a client must not require `iss` from non-advertising servers.
Method: documentation only; no commands were run.
