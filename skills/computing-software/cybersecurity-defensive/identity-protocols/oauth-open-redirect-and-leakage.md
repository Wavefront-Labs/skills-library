---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-open-redirect-and-leakage
name: oauth-open-redirect-and-leakage
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-open-redirect-and-leakage, oauth-security-bcp, referer-leakage, open-redirect, browser-history, logs, postmessage, referrer-policy, identity-protocols]
level: advanced
status: docs-checked
description: "Prevent code and token leakage through open redirectors, Referer headers, browser history, proxy logs and posted messages."
sources:
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token leakage via redirects, Referer and logs

Goal: close the places credentials leak.

Controls (RFC 9700, "OAuth 2.0 Security Best Current Practice"):
- Clients and authorization servers MUST NOT expose open redirectors, endpoints that forward the browser to an arbitrary URI taken from a query parameter (Sections 2.1 and 4.11). Open redirectors can enable exfiltration of authorization codes and access tokens.
- Referer leakage (Section 4.2): codes and `state` can leak through the Referer header when the page that receives the authorization response, or the AS authorization page, contains links to attacker pages or third-party content (ads in iframes, images, user-generated content). Keep such content off those pages.
- Browser history (Section 4.3): a code in a redirect URL can end up in history; one countermeasure RFC 9700 names is the form post response mode instead of a redirect for the authorization response, alongside authorization code replay prevention.
- If the authorization response is sent with `postMessage` instead of a redirect, both initiator and receiver of the message MUST be strictly verified (Sections 2.1 and 4.17).

Gotchas:
- HTTP 307 redirects make the user agent send the user's credentials in the POST body to the new location (Section 4.12); RFC 6749 allows any redirect method, so choose the status code deliberately.
- URLs are also stored and logged by browsers (history), proxy servers and operating systems (RFC 9700 introduction to credential-leakage attacks), so assume a code in a URL is logged.

Verify: search proxy and application logs for `code=` and `access_token=` in URLs.

## Checked

Date: 2026-11-02. Confirmed in RFC 9700 as cited. Removed as not stated there: the `Referrer-Policy: no-referrer` header and `history.replaceState`, the JARM recommendation, the log-redaction list (including `id_token_hint`), the 308 status code claim, and the "AS error pages that reflect the redirect URI" claim.

Method: documentation only; no commands were run.
