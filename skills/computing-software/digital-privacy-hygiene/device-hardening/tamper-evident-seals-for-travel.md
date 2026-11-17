---
id: computing-software.digital-privacy-hygiene.device-hardening.tamper-evident-seals-for-travel
name: tamper-evident-seals-for-travel
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, tamper-evident, travel-security, evil-maid, physical-security]
level: practitioner
status: draft
description: "Use tamper-evident seals, glitter nail polish on screws and reference photos to detect physical tampering with laptops and bags while travelling."
sources:
  - "https://ssd.eff.org/module/things-consider-when-crossing-us-border"
  - "https://www.qubes-os.org/doc/anti-evil-maid/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Tamper-evident seals for travel

**Goal:** know whether someone opened your laptop or bag while it was out of sight; seals detect, they don't prevent.

## Methods
| Method | How | Notes |
|---|---|---|
| Glitter nail polish on screws | Paint a blob over each bottom-case screw, photograph close up | Random glitter pattern is hard to reproduce; compare photos on return |
| Numbered security tape/stickers | Over case seams and ports; record numbers | Visible "VOID" pattern if peeled |
| Tamper-evident bags | Seal the device in a numbered bag before leaving it | Good for hotel rooms and checked luggage |
| Reference photos | Device position, cable placement, bag contents | Cheap baseline for everything |

## Routine
1. Apply seals at home, photograph each one in good light, store the photos off the device (phone, cloud).
2. On return, compare under the same light; any difference means treat the device as compromised.
3. Also check firmware: Secure Boot still on, no new boot entries, no unknown USB devices in the log.

## Limits
- Skilled adversaries can defeat seals; they raise cost and catch opportunists.
- Detection only helps if you act: don't enter passwords on a device you suspect, use a clean device to change
  credentials.
- Anti-evil-maid tools (Heads, Qubes AEM, TPM-measured boot) provide cryptographic tamper detection for high-risk
  users.

## Pair with
Full-disk encryption, a firmware password, and powering off before leaving the device.
