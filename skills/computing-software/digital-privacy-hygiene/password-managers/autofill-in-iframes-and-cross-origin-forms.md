---
id: computing-software.digital-privacy-hygiene.password-managers.autofill-in-iframes-and-cross-origin-forms
name: autofill-in-iframes-and-cross-origin-forms
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, iframe-autofill, autofill, autofill-clickjacking]
level: practitioner
status: draft
description: "Handle password manager autofill prompts inside iframes and embedded payment or login widgets, and decide when to trust a cross-origin frame."
sources:
  - "https://bitwarden.com/help/auto-fill-browser/"
  - "https://bitwarden.com/help/uri-match-detection/"
  - "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Autofill inside iframes and cross-origin forms

**Goal:** fill embedded login and card forms that legitimately live on another domain without letting a
malicious embedded frame harvest your credentials.

## What is happening
Many sites embed forms from other origins: card fields from Stripe/Adyen, SSO login boxes, help-desk widgets.
The page URL is `shop.example`, but the field belongs to `js.stripe.com`. Password managers match the **frame's**
origin or the top page, depending on settings, and modern versions ask before filling across origins.

## Bitwarden behaviour
- When autofilling into a frame whose origin differs from the top-level page or the saved URI, the extension
  warns ("this site may not be trusted / iframe") and asks for confirmation. Accept only if you recognise the
  frame's host (payment processor you expect, the company's own SSO domain).
- Card autofill into payment iframes is common and usually expected.

## Decide
| Frame origin | Action |
|---|---|
| Known payment processor on a checkout page you navigated to | Fill card |
| Company's own auth domain (login.example.com on www.example.com) | Fill, consider adding URI to the item |
| Unknown domain, ad-like box, or a login box on an unrelated page | Do not fill |

## Find the frame origin
Right-click the field > Inspect: look for the enclosing `<iframe src=...>`. Or use the manager's prompt text,
which names the domain.

## Gotchas
- Autofill-on-page-load into iframes is how 2024-era clickjacking/iframe attacks harvested data; keep page-load
  fill off and use the shortcut.
- If a legit embedded login never fills, add the frame's domain as an extra URI on that item rather than loosening
  match detection globally.
