---
id: computing-software.web-development.frontend-development.form-spam-protection
name: form-spam-protection
category: computing-software
field: web-development
product: frontend-development
tags: [honeypot-field, form-spam-protection, turnstile, captcha, rate-limiting, bot-protection]
level: practitioner
status: docs-checked
description: "Layered spam protection for public forms: accessible honeypot fields, time traps, rate limits and Cloudflare Turnstile with server-side token verification."
sources:
  - https://developers.cloudflare.com/turnstile/get-started/server-side-validation/
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/429
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form spam protection

Layer cheap invisible checks first; add a challenge only where spam persists.

## 1. Honeypot (accessible)
```html
<div class="hp" aria-hidden="true">
  <label for="website">Leave this field empty</label>
  <input id="website" name="website" type="text" tabindex="-1" autocomplete="off">
</div>
```
```css
.hp { position: absolute; left: -10000px; }
```
Reject (or silently accept and drop) submissions where `website` is non-empty. Do not use `type="hidden"` or `display:none` (bots skip those); do not name it `email` (password managers autofill it).

## 2. Time trap
Embed a signed timestamp (HMAC) at render; reject submissions that arrive implausibly fast or older than the session lifetime.

## 3. Rate limit
Per IP and per target account/email, at the edge or in the app. Return 429; a `Retry-After` header may tell clients how long to wait.

## 4. Turnstile (privacy-friendly challenge)
```html
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<div class="cf-turnstile" data-sitekey="SITE_KEY"></div>
```
```js
const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
  method: "POST",
  body: new URLSearchParams({ secret: process.env.TURNSTILE_SECRET, response: token, remoteip: ip }),
});
const { success, "error-codes": errs } = await r.json();
if (!success) return res.status(400).send("Verification failed");
```
Tokens are single-use and valid for 300 seconds; a replayed token is rejected (`timeout-or-duplicate`). The client widget alone does not protect the form: always call Siteverify.

## 5. Content checks
Reject links in name fields, Cyrillic/URL spam patterns, or route to Akismet/moderation queue instead of hard-blocking.

## Gotchas
- Client-only checks are bypassed by POSTing directly; every check must run server-side.
- Challenges hurt accessibility and conversion; skip them for authenticated users.

## Checked

2026-11-01. Confirmed in Cloudflare Turnstile server-side validation docs: Siteverify endpoint and `remoteip` parameter, 300-second validity, single use, `timeout-or-duplicate`, widget alone not sufficient; MDN: 429 with optional `Retry-After`. Removed: reCAPTCHA score claims, CSP directive claim, example thresholds and library names.

Method: documentation only; no commands were run.

## Verify
- [ ] curl POST with honeypot filled is rejected; POST without a token is rejected.
- [ ] Screen reader users never land on the honeypot (aria-hidden, tabindex -1).
