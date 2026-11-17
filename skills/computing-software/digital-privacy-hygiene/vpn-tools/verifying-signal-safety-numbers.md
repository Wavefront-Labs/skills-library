---
id: computing-software.digital-privacy-hygiene.vpn-tools.verifying-signal-safety-numbers
name: verifying-signal-safety-numbers
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, safety-number, key-verification, signal, signal-messenger, end-to-end-encryption, mitm, safety-number-change]
level: practitioner
status: docs-checked
description: "Verify a contact's Signal safety number in person or over a trusted channel, and decide what to do when the contact's keys change."
sources:
  - "https://ssd.eff.org/module/key-verification"
  - "https://ssd.eff.org/module/how-to-use-signal"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying Signal safety numbers

**Goal:** confirm you're encrypting to your contact's real key and not to an impostor's, for conversations where that matters.

## Why
Someone claiming to be your friend can send a chat request, and the key your app uses may belong to a different
person, who could then read your future messages. Key verification checks that the key is the one your friend
actually holds. EFF says it may not be necessary for everyone, but is useful when discussing private information.

## What it is
Apps show a "fingerprint" or "safety number" derived from the key, short enough to compare, often with a QR code.
Signal shows a string of 60 numbers and a QR code.

## Verify
1. Open the chat, tap the contact's name at the top, then View safety number (same on Android and iPhone).
2. Match the colour cards with the person you are verifying with.
3. In person (best): scan the QR code. Otherwise read the numbers aloud to compare them, or copy the numbers and
   share them over a secondary secure channel.
4. Out of band: use a channel other than the one you are verifying, such as a phone call, video chat or another
   end-to-end encrypted app. A fake contact would have to impersonate your friend on both services at once.
5. Tap Mark as verified.

## When keys change
When someone changes phones they often change keys, and they may hold a key for each device. Apps indicate when
keys change. Confirm with the person that the change is expected, then re-verify their new keys in person or over
another medium.

## Verify
- [ ] Key contacts are marked verified.
- [ ] Everyone you chat with sensitively knows to re-verify after a change notice.

## Checked
Method: docs-checked 2026-11-09 against the EFF Surveillance Self-Defense pages "Key verification" (why, in-person and out-of-band sections read via targeted search of the downloaded page) and "How to use Signal" (Verify Safety Numbers section read in full). Dropped as unconfirmed: causes of a change other than phone changes, the "verified contacts become unverified" behaviour, per-pair group verification, the usernames note, and the screenshot gotcha. support.signal.org could not be read and was removed from sources.
