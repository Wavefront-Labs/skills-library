---
id: computing-software.cybersecurity-defensive.application-security.referrer-policy
name: referrer-policy
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [referrer-policy, security-headers, information-leakage, privacy, url-tokens]
level: practitioner
status: docs-checked
description: "Choose and set a Referrer-Policy so URLs with tokens, IDs or search terms are not leaked to third parties, with per-link overrides and verification."
sources: ["https://www.w3.org/TR/referrer-policy/", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Referrer-Policy

When a page loads a resource or the user follows a link, the browser sends a `Referer` header with the current
URL. If URLs contain password reset tokens, session IDs, document IDs, email addresses or search terms, those
leak to analytics, CDNs, ad networks and any linked site.

## Values
| Value | Same-origin requests | Cross-origin requests | HTTPS to HTTP |
|---|---|---|---|
| `no-referrer` | nothing | nothing | nothing |
| `same-origin` | full URL | nothing | nothing |
| `strict-origin` | origin only | origin only | nothing |
| `strict-origin-when-cross-origin` | full URL | origin only | nothing |
| `no-referrer-when-downgrade` | full | full | nothing |
| `unsafe-url` | full | full | full (never use) |

Modern browsers default to `strict-origin-when-cross-origin` if no policy is set. Set it explicitly anyway
(older clients, and to document intent).

## Choosing
- General sites: `strict-origin-when-cross-origin`.
- Apps with sensitive data in paths (healthcare, document portals) or tokens in URLs: `same-origin` or
  `no-referrer`.
- Password reset and magic-link landing pages: `no-referrer` on that response, and redirect to a token-free
  URL immediately after consuming the token.

## Setting it
- Header: `Referrer-Policy: strict-origin-when-cross-origin` (at reverse proxy/CDN or framework middleware).
- Meta tag: `<meta name="referrer" content="no-referrer">`.
- Per element: `<a href="..." referrerpolicy="no-referrer">`, `rel="noreferrer"` (no dash in the link relation).

## The real fix
Do not put secrets in URLs. Referrer-Policy reduces one leak path, but URLs also land in browser history,
proxy logs and server logs.

## Verify
`curl -sI` shows the header; in DevTools Network, a request from a sensitive page to a third-party resource
shows `Referer` as origin-only or absent.

## Checked
2026-10-28. Confirmed against official pages: policy values and per-element referrerpolicy and rel=noreferrer (MDN Referrer-Policy; OWASP HTTP Headers Cheat Sheet).
Removed or rewritten: the Helmet default claim and the noreferrer-implies-noopener claim.
Method: documentation only; no commands were run.
