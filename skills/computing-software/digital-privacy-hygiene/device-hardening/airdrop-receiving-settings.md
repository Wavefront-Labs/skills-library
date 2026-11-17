---
id: computing-software.digital-privacy-hygiene.device-hardening.airdrop-receiving-settings
name: airdrop-receiving-settings
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, airdrop-settings, ios, unsolicited-images, namedrop]
level: practitioner
status: docs-checked
description: "Control who can send you AirDrop items: Receiving Off, Contacts Only, the temporary Everyone for 10 Minutes mode, and the AirDrop code for people not in your contacts."
sources:
  - "https://support.apple.com/en-us/119857"
  - "https://support.apple.com/guide/personal-safety/welcome/web"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# AirDrop receiving settings

**Goal:** strangers can't push images to you, and any exception expires on its own.

## Receiving options
- **Receiving Off**: nobody can send to you.
- **Contacts Only**: only people in your contacts.
- **Everyone for 10 Minutes**: a temporary mode. In iOS 16.2 and later it changes after 10 minutes: to Contacts Only if you are
  signed in to your Apple Account, to Receiving Off if you are not.
- A sender who is not in your contacts asks you to open Control Center, touch and hold the connectivity controls, tap
  AirDrop and choose Everyone for 10 Minutes.
- If both devices use iOS 26.2 or later, a person not in your contacts is prompted to use an AirDrop code. They must tap
  Get AirDrop Code on their device and tell you the code. They are then added to the Other Known List in your contacts for
  30 days; you can mark them as unknown in the Contacts app before then.

## Holding devices together
If both devices are on iOS 17 or later, holding them together starts AirDrop sharing. Apple's page names this only as a
way to share; it does not list a setting to turn it off, so check Apple's iPhone User Guide for that.

## Children
Communication Safety can warn a child, blur the content and offer resources if sensitive content is received or sent via
AirDrop.

## Verify
- [ ] Receiving is Contacts Only or Receiving Off when you are not actively receiving.
- [ ] After using Everyone for 10 Minutes, confirm it has reverted.

## Checked
2026-10-28. Confirmed on Apple Support 119857: the three receiving options, the 10-minute revert rule (iOS 16.2+),
Control Center route, iOS 17 hold-together, iOS 26.2 AirDrop code and 30-day Other Known List, Communication Safety.
Removed (not on the fetched pages): Settings > General > AirDrop path, Mac Finder steps, device-name advice, hashed
identifier claims, NameDrop toggle, Sensitive Content Warning path, Contacts Only iCloud requirement, AirDrop over internet.
Method: documentation only; no commands were run.
