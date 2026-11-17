---
id: computing-software.digital-privacy-hygiene.device-hardening.apple-activation-lock
name: apple-activation-lock
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, activation-lock, find-my, secure-erase]
level: practitioner
status: docs-checked
description: "Understand Apple Activation Lock: what it protects, how to check a used device before buying, and what to do before selling or after giving a device away."
sources:
  - "https://support.apple.com/en-us/108794"
  - "https://support.apple.com/en-us/102542"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Apple Activation Lock

**Goal:** a lost or stolen device is useless to others, and a device you sell or buy isn't stuck.

## What it is
Activation Lock turns on automatically when you turn on Find My. Apple stores your Apple Account on its activation servers
and links it to the device. Your Apple Account password is required before anyone can turn off Find My, erase the device,
or reactivate and use it. Even after a remote erase it can keep deterring reactivation as long as Find My stays on.
It covers iPhone and iPad, Apple Watch (watchOS 2 and later), Mac with an Apple T2 Security Chip or Apple silicon
(macOS Catalina or later) and Apple Vision Pro.

## If the device is lost or stolen
Mark it as lost in the Find My app straight away. Lost Mode locks the screen with a passcode and shows a custom message
with your phone number; you can also erase remotely, and the message still shows after the erase.

## Before selling or giving away
Back up first, because erasing removes personal data from the device. Follow Apple's article for your device
("What to do before you sell, give away, or trade in"). For Apple Watch: unpair it from the Apple Watch app on the iPhone
(keep them close together), remove the cellular plan if present, and enter your Apple Account password to turn off
Activation Lock.

## Already gave it away without removing it
Apple Watch: on iCloud.com open Find My iPhone, select All Devices, click the watch, choose Erase Apple Watch, then
click the X next to it.

## Buying used
- On iOS or iPadOS 15 or later, an "iPhone Locked to Owner" screen means Activation Lock is on: don't take ownership.
- If the passcode screen or Home Screen appears, the device has not been erased: ask the seller to erase it.
- Begin setup; if it asks for the previous owner's Apple Account, hand it back. The device is ready when you see the
  Hello screen.

## Forgotten Apple Account or password
Without your Apple Account or its password you may be unable to reactivate the device, so keep your account details
current at your Apple Account page.

## Checked
2026-10-28. Confirmed on Apple Support 108794 (Activation Lock for iPhone and iPad) and 102542 (Apple Watch sell or
trade-in): everything above. Removed (not on the fetched pages): Settings menu paths for signing out and erasing an
iPhone, the appleid.apple.com device-list step, the proof-of-purchase unlock route, and the repair-time Find My claim.
Method: documentation only; no commands were run.
