---
id: computing-software.cybersecurity-defensive.application-security.permissions-policy
name: permissions-policy
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [permissions-policy, feature-policy, security-headers, browser-security, iframe-allow]
level: practitioner
status: docs-checked
description: "Set a Permissions-Policy header to disable powerful browser features (camera, geolocation, payment, USB) for your pages and embedded iframes, and verify it."
sources: ["https://www.w3.org/TR/permissions-policy/", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Permissions-Policy

`Permissions-Policy` (formerly `Feature-Policy`) controls which origins may use powerful browser features in
a document and its frames. It limits damage from XSS and from third-party iframes or scripts trying to access
camera, microphone, location or payment APIs.

## Syntax (structured header)
```
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(self "https://pay.example.com"),
  usb=(), serial=(), hid=(), bluetooth=(), magnetometer=(), gyroscope=(), accelerometer=(),
  fullscreen=(self), display-capture=()
```
- `()` = disabled for everyone, including your own page.
- `(self)` = your origin only; add quoted origins to allow specific embeds.
- `*` = all origins (avoid).
Note the old `Feature-Policy` syntax was different (`camera 'none'`); do not mix them.

## Iframes
Delegation to an iframe needs both the header allowing that origin and the `allow` attribute:
```html
<iframe src="https://pay.example.com/widget" allow="payment"></iframe>
```
Third-party iframes get nothing unless delegated, so a restrictive header plus explicit `allow` is the model.

## Rollout
1. Inventory features actually used (video calls need camera/microphone, maps need geolocation).
2. Start with a deny list of everything unused; allow `self` only where needed.
3. Test in staging before enforcing.
4. Set at the CDN/reverse proxy for all responses, or per route for the few pages needing features.

## Gotchas
- Browser support varies by feature; check the MDN compatibility data.
- The header applies per document; set it on HTML responses (setting on API JSON does nothing harmful but
  adds bytes).

## Verify
`curl -sI https://site | grep -i permissions-policy` shows the header; a feature the policy disables is refused by
the browser when a script tries to use it.

## Checked
2026-10-28. Confirmed against official pages: header syntax with empty list, self and quoted origins, the iframe allow attribute, and the Feature-Policy predecessor (MDN Permissions-Policy).
Removed or rewritten: interest-cohort, the Report-Only rollout claim, the console-warning claim and the DevTools menu path.
Method: documentation only; no commands were run.
