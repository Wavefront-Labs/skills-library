---
id: computing-software.digital-privacy-hygiene.privacy-configuration.tokenised-mobile-wallet-payments
name: tokenised-mobile-wallet-payments
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, mobile-wallet-tokenization, apple-pay, google-wallet, payment-privacy]
level: practitioner
status: draft
description: "Understand how Apple Pay and Google Wallet tokens hide your card number from merchants, what each company still sees, and what to do if a device is lost."
sources:
  - "https://support.apple.com/guide/security/welcome/web"
  - "https://support.google.com/wallet"
  - "https://www.emvco.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Tokenised mobile wallet payments

**Goal:** know why paying with a phone is safer than a card and where privacy limits remain.

## How tokenisation works
When you add a card, the network issues a **device token** (Apple: Device Account Number) stored in the phone's secure
element or as a cloud token. Each payment uses the token plus a one-time cryptogram. The merchant never receives your
real card number, so a breach at the shop can't leak it, and skimmers get nothing reusable.

## What's still visible
| Party | Sees |
|---|---|
| Merchant | Token, amount, time; often the last four digits; online orders still see name and address you give |
| Card issuer/bank | Full transaction as usual |
| Apple | Apple says it doesn't keep transaction information that can be tied back to you for Apple Pay purchases |
| Google | Google Wallet may store transaction details in your Google account depending on settings; check Wallet privacy settings and activity |

## Settings
- Require Face ID/fingerprint for every payment; avoid express transit modes on cards you care about (express mode pays
  without authentication).
- Google: review Wallet > settings > privacy, and payment activity in your Google account.

## Lost or stolen device
Use Find My / Find My Device to mark it lost or erase; this suspends Wallet cards. You can also remove cards at
appleid.apple.com or wallet.google.com. The bank can suspend the token without cancelling your physical card.

## Gotchas
- Refunds sometimes need the same device; the token differs from your plastic card number.
- Replacing a card usually updates the token automatically; check after reissue.
