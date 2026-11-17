---
id: computing-software.cybersecurity-defensive.application-security.clickjacking-defence
name: clickjacking-defence
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [security-headers, clickjacking, frame-ancestors, x-frame-options, ui-redressing, cwe-1021]
level: practitioner
status: docs-checked
description: "Stop clickjacking with CSP frame-ancestors and X-Frame-Options: choosing values, legitimate embedding allowlists, SameSite cookies as backup, and verification."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors", "https://cwe.mitre.org/data/definitions/1021.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clickjacking defence

An attacker frames your page invisibly and tricks the user into clicking (transfer money, change settings,
grant OAuth consent). Defence: tell browsers who may frame you.

## Headers
Preferred (CSP Level 2+):
```
Content-Security-Policy: frame-ancestors 'none'
Content-Security-Policy: frame-ancestors 'self'
Content-Security-Policy: frame-ancestors 'self' https://portal.partner.example
```
Legacy fallback (still send for older clients):
```
X-Frame-Options: DENY          # or SAMEORIGIN
```
`ALLOW-FROM` in X-Frame-Options is obsolete and ignored by modern browsers; use frame-ancestors for allowlists.
When both are present, browsers that support frame-ancestors use it.

## Where to set
- At the edge/proxy or framework middleware for all HTML responses.
- frame-ancestors only works as an HTTP header, not in a `<meta>` CSP tag.
- Apply to every page, especially state-changing ones and login/consent pages; APIs returning JSON do not need it.

## Legitimate embedding
Inventory where your app is embedded (Teams/Slack tabs, partner portals, your own other domains) and list
exactly those origins. Avoid wildcards like `https:`.

## Defence in depth
- `SameSite=Lax`/`Strict` session cookies: cross-site frames do not carry the session, which defeats many clickjacking attacks even if headers are missing.
- Re-authentication or confirmation dialogs for high-risk actions.
- JavaScript frame-busting is unreliable (sandboxed iframes disable it); do not rely on it.

## Gotchas
- Headers set on the app but stripped or overridden by a CDN/proxy; test the real public response.
- Error pages and static HTML served by a different server often lack the header.

## Verify
`curl -sI https://app.example.com/settings | grep -i -E 'frame-ancestors|x-frame-options'` shows the
policy; a test page on another origin embedding the URL in an iframe renders blank with a console error.

## Checked
2026-10-28. Confirmed against official pages: X-Frame-Options values, ALLOW-FROM obsolete, meta tags do not work for X-Frame-Options, frame-ancestors, SameSite and frame-busting caveats (OWASP Clickjacking Defense Cheat Sheet; MDN frame-ancestors).
Removed or rewritten: framework-specific settings and the SameSite Lax parenthetical.
Method: documentation only; no commands were run.
