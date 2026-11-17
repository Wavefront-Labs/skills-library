---
id: computing-software.digital-privacy-hygiene.device-hardening.iphone-usb-accessory-restrictions
name: iphone-usb-accessory-restrictions
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, usb-restricted-mode, ios, iphone-security, accessories-setting, forensic-extraction, juice-jacking, trust-this-computer, lockdown-mode]
level: practitioner
status: docs-checked
description: "Control which USB and other accessories can connect to an iPhone or iPad with the Wired Accessories setting, and what happens while it is locked."
sources:
  - "https://support.apple.com/en-us/111806"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# iPhone USB accessory restrictions

**Goal:** a locked iPhone or iPad does not exchange data with an unknown cable, accessory or computer.

## Default behaviour
By default you must unlock the device before it connects to an accessory or computer (USB or Thunderbolt devices, Smart
Connector accessories for iPad, a Mac or PC). After you unlock it, the accessory stays connected even if the device locks
again. If you do not unlock, it will not communicate with the accessory and might not charge, but it charges as usual from a
USB power adapter. A storage accessory always needs the device unlocked.

## The setting
Settings > Privacy & Security > Security > **Wired Accessories**. Options depend on the model:
- USB-C iPhone or iPad: **Always Ask** (approve every accessory every time), **Ask for New Accessories**,
  **Automatically Allow When Unlocked** (default), **Always Allow**.
- Lightning iPhone or iPad: **Automatically Allow When Unlocked** (default) or **Always Allow**.
For maximum protection on a USB-C model choose Always Ask. Administrators can control the setting on supervised devices
with Apple Configurator or mobile device management.

## Practical habits
- If an accessory is not recognised after unlocking: disconnect it, unlock the device, reconnect.
- Only approve accessories and computers you own; use your own charger and a wall adapter when travelling.

## Verify
- [ ] Wired Accessories is set to Always Ask or Ask for New Accessories (USB-C) and no unknown accessory is approved.

## Checked
2026-10-28. Confirmed on Apple Support 111806: default unlock behaviour, charging, storage accessories, the path and
option names per connector type, supervised-device control. Removed (not on the fetched page): the "locked for over an hour"
rule, the older Face ID & Passcode > Accessories path, the Lockdown Mode claim, the Trust This Computer reset path, and the
juice-jacking risk statements.
Method: documentation only; no commands were run.
