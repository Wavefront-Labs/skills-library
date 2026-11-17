---
id: computing-software.digital-privacy-hygiene.two-factor-auth.voip-numbers-for-two-factor
name: voip-numbers-for-two-factor
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, voip-number-2fa, secondary-phone-number, sms-2fa]
level: practitioner
status: draft
description: "Decide whether a VoIP number like Google Voice should receive 2FA codes, why some banks reject it, and how to lock the VoIP account and number."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://support.google.com/voice/answer/1065667"
  - "https://support.google.com/voice/answer/9182120"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# VoIP numbers for two-factor

**Goal:** use a VoIP number to keep your real carrier number out of SMS 2FA and recovery, where sites allow it.

## Trade-offs
| Pro | Con |
|---|---|
| Not vulnerable to carrier SIM swap | Security equals the VoIP account (Google account for Google Voice) |
| Number can be kept private/separate | Many banks and some services reject VoIP numbers (line-type checks) |
| Works abroad on Wi-Fi | NIST: VoIP doesn't prove device possession for out-of-band |

## Setup (Google Voice example)
- Choose a number tied to a Google account protected by a security key.
- Settings: forward codes nowhere you don't control; turn off linked numbers you don't need.
- **Number lock:** Google Voice requires an unlock step (and fee) before porting out; keep it locked.

## Where to use it
- Sites that insist on a phone number for account recovery when you can't avoid it.
- Marketplace/sign-up numbers to keep the real number private.
Not for: your Google account's own recovery (circular), banks that reject it.

## Prefer
TOTP, passkeys or security keys over any phone number where offered.

## Gotchas
- Inactive Google Voice numbers can be reclaimed after months without activity; make a call/text periodically.
- Free VoIP apps that recycle numbers are dangerous for recovery: the next owner gets your codes.
