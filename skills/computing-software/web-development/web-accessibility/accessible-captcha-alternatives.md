---
id: computing-software.web-development.web-accessibility.accessible-captcha-alternatives
name: accessible-captcha-alternatives
category: computing-software
field: web-development
product: web-accessibility
tags: [text-alternatives, accessible-captcha, bot-protection, wcag-1-1-1, wcag-3-3-8]
level: practitioner
status: docs-checked
description: "Handling CAPTCHAs accessibly: why image and audio puzzles fail users, WCAG 1.1.1 and 3.3.8 requirements, invisible risk-based options, and server-side bot defences."
sources:
  - https://www.w3.org/TR/turingtest/
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
  - https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html
  - https://developers.cloudflare.com/turnstile/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CAPTCHA and non-text controls

## 1. Requirements
- WCAG 1.1.1: a CAPTCHA must have a text alternative identifying its purpose, and **alternative forms in different modalities** (e.g. visual + audio) so one sensory disability doesn't block the user.
- WCAG 3.3.8 (AA, new in 2.2): no step of authentication may require a cognitive function test unless it offers an alternative method, a mechanism to assist, object recognition, or identifying the user's own content. An audio alternative that must be transcribed does not count as an alternative. 3.3.9 (AAA) drops the object recognition and personal content exceptions. Object recognition ("select all buses") can still fail many blind users.

## 2. Why traditional CAPTCHAs fail
Distorted text and image grids exclude blind and low-vision users; audio CAPTCHAs are hard for deaf-blind users, non-native speakers and in noisy places; puzzles burden cognitive disabilities; timeouts hit motor disabilities. Modern bots solve them anyway (ML, solver farms).

## 3. Better options, in order
1. **No user-facing challenge**: server-side signals - rate limiting per IP/account/device, honeypot fields (hidden with CSS and `tabindex="-1"` + `aria-hidden`, labelled "Leave blank"), minimum fill time, email verification, anomaly scoring.
2. **Invisible/managed challenges**: for example Cloudflare Turnstile, which offers managed (a checkbox only when risk warrants it), non-interactive and invisible widget types - escalate to a visible challenge only for high-risk visitors.
3. If a visible challenge is unavoidable: offer multiple modalities, make the widget keyboard and screen-reader operable, give a human fallback (support contact) and never time it out quickly.
4. For logins: passkeys, magic links, and MFA reduce reliance on CAPTCHA entirely.

## 4. Implementation notes
- Ensure the widget iframe has a `title` and the page announces failures in text.
- Don't block form submission silently when the score is low - show an accessible alternative path.
- Test that the honeypot is invisible to AT and keyboard users.

## Verify
Complete the protected flow with NVDA/VoiceOver, keyboard-only, and with images disabled; bot traffic metrics stay controlled with the user-facing challenge rate near zero.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 (1.1.1, 3.3.8, 3.3.9) success criterion text and Understanding page, Cloudflare Turnstile documentation.
- Confirmed: 1.1.1 CAPTCHA wording (text alternative identifying the purpose, plus alternative forms for different senses); 3.3.8 is AA with Alternative, Mechanism, Object Recognition and Personal Content exceptions; 3.3.9 is AAA with only Alternative and Mechanism; audio that must be transcribed cannot meet the Alternative exception; Turnstile widget types and WCAG 2.2 AA claim.
- Removed (no documentation found): the reCAPTCHA and hCaptcha statements.
Method: documentation only; no commands were run.