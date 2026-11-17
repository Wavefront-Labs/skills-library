---
id: computing-software.digital-privacy-hygiene.two-factor-auth.recognising-otp-relay-scams
name: recognising-otp-relay-scams
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, otp-relay-scam, mfa-fatigue, vishing, one-time-code, otp-bot, account-takeover, whatsapp-code-scam, social-engineering]
level: intro
status: draft
description: "Recognise the scams that get you to read out or forward a one-time code (fake bank calls, OTP bots, 'sent to you by mistake' messages) and the one rule that beats them."
sources:
  - "https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams"
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recognising OTP relay scams

**Goal:** 2FA codes are only defeated when you hand them over. Learn the scripts.

## The rule
**A code you didn't request, or a request to read out any code, is an attack.**
Real companies never ask you to tell them a code they sent; the message itself usually
says "Never share this code".

## Common scripts
1. **Bank/fraud "verification" call**: "We've stopped a suspicious payment; to cancel it
   we'll send a code to verify you." The code actually authorises their login or payment.
   Often driven by automated **OTP bots** sold to criminals, with a realistic IVR voice.
2. **"Sent to you by mistake"** (WhatsApp/Instagram/Telegram): a friend's hijacked
   account says they accidentally sent a code to your number; it's your account's
   registration/reset code.
3. **Marketplace buyer**: "Verify you're a real seller, read me the Google Voice code."
   They register a number in your name.
4. **Fake support** on social media or a search-ad support number asking for the code to
   "unlock" your account.
5. **Delivery/parcel**: "Confirm redelivery with the code we texted".

## What to do
- Hang up / don't reply. Call the company on the number on your card or website.
- If you already gave a code: change that account's password, sign out sessions, and call
  the real provider's fraud line; for WhatsApp re-register your number and set 2-step PIN.

## Defence in depth
Passkeys and security keys produce no code to read out; prefer them where offered.

## Verify
- [ ] Family has heard the rule and the "sent by mistake" script.
