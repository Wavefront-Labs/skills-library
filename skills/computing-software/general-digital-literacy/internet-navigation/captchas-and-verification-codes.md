---
id: computing-software.general-digital-literacy.internet-navigation.captchas-and-verification-codes
name: captchas-and-verification-codes
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, online-forms, captcha, verification-codes, one-time-passcode, accessibility]
level: intro
status: draft
description: "Get past CAPTCHAs and one-time verification codes by SMS, email or app, fix codes that never arrive, use accessible alternatives, and spot code-sharing scams."
sources:
  - https://www.w3.org/TR/turingtest/
  - https://support.google.com/accounts/answer/185839
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CAPTCHAs and verification codes

**Goal:** finish sign-ups and log-ins without getting stuck, and never hand a code to a scammer.

## CAPTCHAs
- Types: tick box ("I'm not a robot"), picture grids (traffic lights, buses), distorted text, puzzle sliders, or invisible checks.
- If you keep failing: slow down, select all partial squares, use the **refresh** icon for a new puzzle; disable VPN and strict tracker blocking for that site, which make you look like a bot; sign in to your browser account.
- **Accessibility:** use the headphone/audio option; contact the organisation for another route. W3C recognises CAPTCHAs as an accessibility barrier; organisations should offer alternatives.

## One-time codes (OTP)
- Arrive by SMS, email, voice call or authenticator app; usually valid 5-10 minutes; only the newest code works.
- **Code didn't arrive:**
  - Wait 1-2 minutes, then *Resend* once (repeated resends can lock you out).
  - Check phone signal; SMS may be delayed abroad or blocked by spam filters; try a voice call option.
  - Email codes: check Spam/Promotions; search the sender name.
  - Check the phone number/email on file is correct.
- Phones auto-fill codes from SMS (iPhone *From Messages* suggestion, Android autofill).

## Scam alert
**Never read out or forward a verification code.** Banks, delivery firms, WhatsApp and Google will never call to ask for one. "I sent you a code by mistake, please send it back" is an account takeover attempt.

## Gotchas
- Codes go to the old number after you change phone numbers; update numbers on important accounts first.
- Shared family numbers mean someone else might receive your codes.
- Prefer authenticator apps or passkeys over SMS for important accounts (SIM-swap risk).

## Verify
- [ ] Contact details on key accounts are current; backup method set up for when codes fail.
