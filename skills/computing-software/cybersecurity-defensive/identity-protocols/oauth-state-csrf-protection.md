---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-state-csrf-protection
name: oauth-state-csrf-protection
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-state-csrf-protection, oauth-authorization-code-security, state, csrf, callback, login-csrf, session-binding, identity-protocols]
level: practitioner
status: docs-checked
description: "Prevent login and authorization CSRF with unguessable state bound to the user agent, or PKCE-as-CSRF, and validate it before using the code."
sources:
  - https://www.rfc-editor.org/rfc/rfc6749
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State parameter and CSRF on the callback

Goal: only accept authorization responses for requests this browser started.

Method: clients MUST prevent CSRF on the redirection endpoint. Use a one-time `state` value that is unpredictable and securely bound to the user agent, and verify it on callback before the token request. RFC 9700 allows clients that have ensured the AS supports PKCE to rely on PKCE for CSRF protection, and OpenID Connect flows to use the `nonce`.

Gotchas:
- Without CSRF protection, a request to the redirection endpoint can originate from a malicious third party instead of the AS (RFC 9700 section 2.1).
- `state` is returned unchanged in the authorization response and a mismatch means abort (RFC 6749 section 4.1.2).

Verify: replay a callback URL in a different browser session.

## Checked

2026-11-02. Confirmed against RFC 9700 section 2.1 (CSRF prevention, PKCE and nonce alternatives, one-time user-agent-bound tokens) and RFC 6749 sections 4.1.1 and 4.1.2 (`state` semantics). Removed: the 128-bit figure, cookie storage, signed-state and multi-tab advice (not in either RFC).
Method: documentation only; no commands were run.
