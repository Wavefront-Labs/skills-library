---
id: computing-software.digital-privacy-hygiene.two-factor-auth.responding-to-a-suspected-sim-swap
name: responding-to-a-suspected-sim-swap
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, sim-swap-response, sim-swap, phone-number-security, port-out-fraud, account-takeover, incident-response, carrier-fraud]
level: practitioner
status: draft
description: "When your phone suddenly shows 'No Service'/'SOS only' and you get SIM-change notices, act within minutes: carrier fraud line, email and bank lockdown, evidence."
sources:
  - "https://www.fcc.gov/sim-swap-port-out-fraud"
  - "https://www.ic3.gov/"
  - "https://www.identitytheft.gov/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Responding to a suspected SIM swap

**Goal:** minutes matter. Attackers who swap your SIM usually reset email, then bank and
crypto accounts within the hour.

## Signs
- Phone shows **No Service / SOS only** in a place it normally works, not fixed by reboot.
- Email or text: "Your SIM was changed", "port-out request", "new eSIM activated".
- Password reset emails you didn't request.

## First 15 minutes (from another phone or Wi-Fi)
1. **Call the carrier's fraud line** (from a different phone, or chat via Wi-Fi).
   Say "unauthorised SIM change/port-out", ask them to **reverse it and freeze the
   account**; get a reference number. US carriers must notify and verify SIM changes
   under FCC rules, so ask what verification was used.
2. **Secure email** (from a trusted computer): change password, sign out all sessions,
   check forwarding rules and recovery phone/email, remove the phone as a recovery method.
3. **Banks and crypto exchanges**: call fraud lines; freeze transfers and withdrawals.
4. **Password manager account**: confirm no new device sessions.

## Next hours
- Go through accounts that used SMS 2FA; switch them to authenticator/keys.
- Set carrier **port-out PIN / number lock** once restored.
- Check for new devices on Apple/Google accounts.
- Credit freeze if identity data may be exposed.

## Evidence and reporting
Screenshot notifications, note times; file with the carrier, police report if money
was lost, FBI IC3 (US) and identitytheft.gov for a recovery plan.

## Gotchas
- The attacker may call you pretending to be the carrier "fixing" the issue and ask for
  a code. Hang up; call the number on your bill.
- Don't wait to "see if service comes back".

## Verify
- [ ] Service restored on your SIM, account frozen/flagged, reference numbers recorded.
- [ ] No account still uses SMS as sole 2FA.
