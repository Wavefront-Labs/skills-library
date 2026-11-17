---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-sector-and-software-statement
name: oidc-sector-and-software-statement
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-sector-and-software-statement, oidc-client-registration, software_statement, sector_identifier_uri, metadata-trust, jwt, identity-protocols]
level: sme
status: docs-checked
description: "Decide which registration metadata to trust: signed software_statement JWTs, sector_identifier_uri validation and per-field policy."
sources:
  - https://openid.net/specs/openid-connect-registration-1_0.html
  - https://www.rfc-editor.org/rfc/rfc7591.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Software statements and trust of registration metadata

Goal: accept dynamic clients with care about self-asserted metadata.

Method:
- A `software_statement` (RFC 7591) is a JWT issued by a party that vouches for client metadata such as `software_id` or `redirect_uris`; if it is valid and signed by an acceptable authority, its values take precedence over the plain JSON values. The statement is still self-asserted by the client, so it is not sufficient on its own to identify the software: consider the whole registration request, including any initial access token.
- For `sector_identifier_uri`, the OP fetches it at registration and fails the registration unless every registered `redirect_uri` appears in the returned JSON array. It need not retain or revalidate the file later.
- `client_name`, `logo_uri`, `client_uri`, `policy_uri` and `tos_uri` are client-supplied; human-readable values without language tags must be used as-is and no assumption made about their language or script.

Gotchas:
- The authorization server may reject with `invalid_software_statement` or `unapproved_software_statement`.
- Only validate statements from issuers you trust (the signing authority is a deployment decision).

Verify: submit a statement signed by an unknown key and confirm it is rejected.

## Checked
2026-11-02. Confirmed against OpenID Connect Dynamic Client Registration 1.0 (client metadata, section 5) and RFC 7591 (software statement precedence, error codes). Removed: SSRF-egress advice for `jwks_uri`, `logo_uri` fetches, the `client_uri` phishing signal and "sanitise display fields", which these documents do not state.
Method: documentation only; no commands were run.
