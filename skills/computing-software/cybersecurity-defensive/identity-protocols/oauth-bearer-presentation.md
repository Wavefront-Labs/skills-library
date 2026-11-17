---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-bearer-presentation
name: oauth-bearer-presentation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-bearer-presentation, oauth-bearer-tokens, bearer, authorization-header, rfc6750, access_token, query-parameter, identity-protocols]
level: practitioner
status: docs-checked
description: "Send access tokens in the Authorization Bearer header, why form-body and query methods are discouraged, and what to log or redact."
sources:
  - https://www.rfc-editor.org/rfc/rfc6750
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Presenting bearer tokens

Goal: transmit tokens safely.

Method: `Authorization: Bearer <token>` (the `b64token` syntax of RFC 6750; clients SHOULD use this header and resource servers MUST support it). RFC 6750 also defines `access_token` in a form-encoded body (not GET, `application/x-www-form-urlencoded`, single-part; SHOULD NOT be used unless the header is unavailable) and in the URL query (SHOULD NOT be used unless the header and body are impossible, because the URL is likely to be logged).

Gotchas:
- Bearer means possession is enough: use TLS, issue short-lived tokens (RFC 6750 section 5.2), and prefer sender-constrained tokens (RFC 9700).
- Clients using the query form SHOULD also send `Cache-Control: no-store`.

Verify: grep access logs for "access_token=".

## Checked

2026-11-02. Confirmed against RFC 6750 sections 2.1 to 2.3, 5.2 and 5.3 (header, form body and query methods and their conditions, `b64token`, `Cache-Control: no-store`, TLS, short-lived tokens, tokens not in page URLs) and RFC 9700 (sender-constrained tokens). Removed: case-insensitive scheme name, the OAuth 2.1 statement, log stripping and token forwarding advice, and the blanket no-store rule.
Method: documentation only; no commands were run.
