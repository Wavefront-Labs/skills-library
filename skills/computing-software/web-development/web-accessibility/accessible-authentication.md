---
id: computing-software.web-development.web-accessibility.accessible-authentication
name: accessible-authentication
category: computing-software
field: web-development
product: web-accessibility
tags: [input-assistance, accessible-forms, accessible-authentication, wcag-3-3-8, wcag-2-2, cognitive-function-test, paste-passwords, captcha-alternatives, passkeys]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.2 SC 3.3.8 Accessible Authentication: no memory or puzzle tests without alternatives; allow paste and password managers, passkeys, email links."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html
  - https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-enhanced.html
  - https://www.w3.org/TR/turingtest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessible authentication (WCAG 3.3.8)

**Goal:** logging in doesn't require remembering, transcribing or solving something (new AA criterion in WCAG 2.2).

## 1. The rule
A cognitive function test (remember a password, transcribe a code, solve a puzzle) is not required in any authentication step **unless** there is:
- an alternative method without one, or
- a mechanism to assist (password manager autofill, **copy-paste allowed**), or
- the test is object recognition (pick the photos with cars) or identifying non-text content the user provided (their own photo). Those two exceptions exist at AA (3.3.8) but not in the AAA Enhanced criterion (3.3.9).

## 2. What passes
- Username/password fields with correct `autocomplete` (`username`, `current-password`) and **paste allowed** - password managers do the remembering.
- Passkeys / WebAuthn, "magic link" email login, OAuth/SSO.
- One-time codes with `autocomplete="one-time-code"` and paste allowed (copy and paste is a named mechanism in the SC; retyping passcodes is called out in the Understanding page).
- Biometrics via the device.

## 3. What fails
- Blocking paste in password or code fields (`onpaste="return false"`).
- Login forms that break autofill (fields rendered by JS without labels/autocomplete, username and password on different domains/iframes without proper markup).
- Text/arithmetic CAPTCHAs without an alternative; "type the characters you see".
- "Enter the 3rd, 5th and 8th characters of your password" (memorable-word schemes) - requires transcription managers can't do.
- Security questions as a required step.

## 4. CAPTCHAs
Prefer risk-based checks and rate limiting over puzzle CAPTCHAs. If a cognitive challenge is shown, offer an alternative path (email verification, support contact).

## Verify
- [ ] A password manager fills and submits the login without manual typing.
- [ ] Pasting into password and OTP fields works.
- [ ] At least one login path involves no memorisation/transcription (passkey, magic link, SSO).

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text of 3.3.8 (Level AA: alternative, mechanism, object recognition, personal content) and 3.3.9 (Level AAA, only alternative and mechanism); the Understanding page names password-manager fill and copy-paste as mechanisms and says blocking them fails the SC. MDN confirms the username, current-password and one-time-code autocomplete tokens. Removed the CAPTCHA vendor list and the split-OTP requirement.

Method: documentation only; no commands were run.
