---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-redirect-uri-matching
name: oauth-redirect-uri-matching
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-redirect-uri-matching, oauth-authorization-code-security, redirect_uri, exact-match, wildcard, open-redirect, registration, identity-protocols]
level: practitioner
status: docs-checked
description: "Register full redirect URIs and match them as exact strings (except loopback port), banning wildcards and open redirectors that leak codes."
sources:
  - https://www.rfc-editor.org/rfc/rfc9700
  - https://www.rfc-editor.org/rfc/rfc6749
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redirect URI registration and exact matching

Goal: ensure codes and tokens go only to the intended client.

Method (RFC 9700 Section 2.1):
- The AS MUST compare the received `redirect_uri` against the registered values with exact string matching (RFC 3986 Section 6.2.1, simple string comparison). The one exception is native apps using a localhost redirect, where the port number may vary.
- Authorization responses MUST NOT go over unencrypted connections, so the AS MUST NOT allow `http` redirect URIs except for native clients using loopback interface redirection (RFC 8252 Section 7.3).
- Do not use pattern registrations: RFC 9700 Section 4.1.1 shows that wildcard patterns such as `https://*.somesite.example/*` lead to vulnerabilities, including when the AS handles the wildcard correctly, and Section 4.1.3 requires exact matching instead. Register each exact URL.

Gotchas:
- An open redirector at the client, or any attacker-controlled page under a registered pattern, lets an attacker capture the authorization response (RFC 9700 Sections 2.1, 4.1.3 and 4.11).
- With a registered wildcard pattern, an attacker who can establish any host matching it can receive the code (Section 4.1.1).

Verify: test with a trailing slash, a different case and an added query; each must be rejected by exact matching.

## Checked

Date: 2026-11-02. Confirmed in RFC 9700 Sections 2.1, 4.1.3, 4.11 and RFC 6749 (redirection endpoint). Removed as not stated there: "reject fragments" rule, "dangling subdomain" wording, "https only" generalisation beyond the loopback exception, the normalisation advice.

Method: documentation only; no commands were run.
