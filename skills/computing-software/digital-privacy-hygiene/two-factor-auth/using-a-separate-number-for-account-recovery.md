---
id: computing-software.digital-privacy-hygiene.two-factor-auth.using-a-separate-number-for-account-recovery
name: using-a-separate-number-for-account-recovery
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, secondary-phone-number, phone-number-security, sim-swap, recovery-phone, voip-number, google-voice, prepaid-sim, number-compartmentalization]
level: practitioner
status: draft
description: "Use an unpublished second number for SMS-only accounts so your public number can't be targeted for SIM swaps; know which services reject VoIP numbers."
sources:
  - "https://www.fcc.gov/sim-swap-port-out-fraud"
  - "https://support.google.com/voice/answer/115061"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A separate number for account recovery

**Goal:** an attacker first finds your number (data brokers, social profiles, every
shop you gave it to). If your 2FA/recovery number isn't the one they know, a SIM swap
on your public number gains them nothing.

## Options
| Option | Pros | Cons |
|---|---|---|
| Second carrier line / eSIM on a dual-SIM phone | Real mobile number, accepted everywhere | Monthly cost; still swappable if found |
| Prepaid SIM in a drawer phone | Cheap, never published | Must top up to keep active; number recycling if lapses |
| VoIP number (Google Voice, others) | No SIM to swap; protected by that account's MFA | Many banks/exchanges reject VoIP numbers; tied to that account's security |

## Procedure
1. Get the number; never give it to shops, friends, or social profiles.
2. Lock it at the carrier (port-out PIN, number lock) or secure the VoIP account with a
   security key.
3. Move SMS-only 2FA and recovery for important accounts to it.
4. Keep the public number for everything else.
5. Calendar reminder: keep prepaid lines active (number recycling hands your number to
   a stranger, who then receives your codes).

## Gotchas
- Google Voice numbers can be reclaimed after inactivity; use them periodically.
- If the VoIP account recovers via your public number, you've created a loop; check.
- This reduces targeting; it doesn't make SMS phishing-resistant. Prefer removing SMS
  where possible.

## Verify
- [ ] Number doesn't appear in a search of your name or on data broker results.
- [ ] Important SMS-only accounts point to it; activity reminder set.
