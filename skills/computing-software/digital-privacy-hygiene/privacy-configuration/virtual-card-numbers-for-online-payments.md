---
id: computing-software.digital-privacy-hygiene.privacy-configuration.virtual-card-numbers-for-online-payments
name: virtual-card-numbers-for-online-payments
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, virtual-card-numbers, private-payments, merchant-locked-cards, privacy-com, apple-pay, tokenization, subscription-control, card-fraud]
level: intro
status: draft
description: "Use virtual or merchant-locked card numbers (bank virtual cards, Privacy.com, Apple Pay/Google Pay tokens) so a merchant breach or unwanted subscription can't touch your real card."
sources:
  - "https://www.privacyguides.org/en/financial-services/"
  - "https://www.privacyguides.org/en/advanced/payments/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtual card numbers

**Goal:** give each merchant a different card number you can pause or cancel, limiting
breach fallout, cross-merchant tracking, and subscription traps.

## Options
| Option | How it helps |
|---|---|
| **Bank/issuer virtual cards** (Capital One Eno, Citi virtual numbers, many EU neobanks: Revolut, etc.) | Per-merchant numbers, freezable |
| **Privacy.com** (US) / similar services | Merchant-locked cards, spending limits, custom billing name in some plans |
| **Apple Pay / Google Pay** | Device-specific token per card; merchant never sees your real number in tap or in-app payments |
| **Prepaid/gift cards** | Unlinkable to your identity for small purchases |

## Workflow
1. New merchant or trial subscription: create a **merchant-locked** virtual card with a
   monthly limit slightly above the price.
2. Save it in the password manager item for that merchant.
3. Cancel subscription = pause the card (also contact the merchant; pausing doesn't cancel
   your contractual obligation).
4. Breach notification from a merchant: close that card only.

## Privacy limits
- Your bank/issuer still sees all transactions; merchants still get your name and shipping
  address. Virtual cards aren't anonymity.
- Billing name/address must usually match for verification.

## Verify
- [ ] Recurring subscriptions each on their own virtual card with a limit.
- [ ] Phone wallet set up for in-person payments.
