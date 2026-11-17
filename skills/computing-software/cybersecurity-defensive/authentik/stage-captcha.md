---
id: computing-software.cybersecurity-defensive.authentik.stage-captcha
name: stage-captcha
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, captcha-stage, recaptcha, hcaptcha, turnstile, cap]
level: practitioner
status: docs-checked
description: "Configure the authentik Captcha stage with reCAPTCHA, hCaptcha, Cap or Cloudflare Turnstile: keys, interactive mode, score thresholds, script and verification URLs."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/captcha/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: require a human-check before a flow continues. Bind it in a flow or embed it in the Identification stage (then configure the provider for invisible or background use). It does not run for passkey logins through Identification.

## Options
**Public Key** (site key), **Private Key** (secret), **Interactive**, **Score Minimum/Maximum Threshold**, **Error on Invalid Score** (if off, the flow continues and policies can inspect the result in context), **JavaScript URL**, **API Verification URL**, **Request Content Type**.

## Provider values
- reCAPTCHA (Enterprise, v2, v3): keys from google.com/recaptcha/admin; Interactive off for score-based; thresholds 0.5 and 1.0; JS `https://www.recaptcha.net/recaptcha/api.js`; verify `https://www.recaptcha.net/recaptcha/api/siteverify`.
- hCaptcha: Interactive on; JS `https://js.hcaptcha.com/1/api.js`; verify `https://api.hcaptcha.com/siteverify`; score thresholds only for hCaptcha Enterprise.
- Cloudflare Turnstile: Public Key = Site Key, Private Key = Secret Key; enable Interactive if the widget is Invisible or Managed; JS `https://challenges.cloudflare.com/turnstile/v0/api.js`; verify `https://challenges.cloudflare.com/turnstile/v0/siteverify`; no score thresholds.
- Cap (self-hosted proof of work): default widget only, floating widget unsupported; Public Key like `https://cap.example.com/site-key/`; Interactive on; JS `https://cap.example.com/assets/widget.js` (if using a CDN pin a reviewed version, not the unversioned package); verify `https://cap.example.com/site-key/siteverify`; Request Content Type JSON; no scores.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/captcha/.
Removed as not confirmed by that page: captcha context dictionary detail.
Method: documentation only; no commands were run.
