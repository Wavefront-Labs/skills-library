---
id: computing-software.general-digital-literacy.internet-navigation.sms-codes-and-sim-swap-risk
name: sms-codes-and-sim-swap-risk
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, in-authentication, sim-swap, sms-2fa, port-out-protection]
level: intro
status: docs-checked
description: "Understand why text-message codes are the weakest 2-step option, recognise a SIM swap in progress, add carrier port-out protection and move key accounts to stronger methods."
sources:
  - https://consumer.ftc.gov/consumer-alerts/2019/10/sim-swap-scams-how-protect-yourself
  - https://www.ncsc.gov.uk/guidance/setting-2-step-verification-2sv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SMS codes and SIM swap risk

## The risk
In a **SIM swap**, a criminal contacts your mobile carrier, for example claiming your phone was lost or damaged, and has your number activated on a SIM they control. They then receive your text codes and password resets. Port-out fraud (moving your number to another carrier) works the same way.

NCSC says text-message codes are not the most secure option but still add real protection over no 2-step verification. The FTC says text verification may not stop a SIM swap and suggests an authentication app or a security key for sensitive accounts.

## Warning signs
- Your phone suddenly loses service (no data, texts or calls) in a normal-coverage area.
- An unexpected notification from your carrier that your SIM was activated on a new device, or a port request you didn't make; emails about password resets.
-> Contact your carrier immediately (from another phone) to take back your number; then change passwords and check bank, card and other accounts for unauthorised changes.

## Protect the number
- Set a **PIN or password on your carrier account** (FTC advice; it lowers the risk but some carriers have still made SIM changes despite one) and ask the carrier what SIM-change or port-out protection it offers.
- Keep your phone number and carrier account details private.

## Move important accounts off SMS
- Email, Apple/Google/Microsoft, banking where possible, crypto exchanges, password manager → **passkeys**, **authenticator app**, or **security keys**.
- Remove the phone number as a recovery or 2FA method once a stronger one and backup codes are in place (some banks insist on SMS; keep those protected by the carrier PIN).

## Verify
- [ ] Carrier account has a PIN and SIM-change protection; email account uses a passkey or authenticator app, not SMS alone.

## Checked

Checked 2026-10-27 against the FTC consumer alert on SIM swap scams, NCSC 2-step verification guidance and FCC port-out advice (search-confirmed). Confirmed: how the scam works, PIN or password advice and its limits, text verification may not stop a swap, signs of a swap, authenticator app or security key advice.

Method: documentation only; no commands were run.
