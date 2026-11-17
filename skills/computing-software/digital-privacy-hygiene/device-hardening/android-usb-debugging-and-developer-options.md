---
id: computing-software.digital-privacy-hygiene.device-hardening.android-usb-debugging-and-developer-options
name: android-usb-debugging-and-developer-options
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, usb-debugging, android-security, verified-boot]
level: practitioner
status: draft
description: "Turn off Android developer options, USB and wireless debugging, revoke ADB authorisations, and keep OEM unlocking off unless you're flashing."
sources:
  - "https://developer.android.com/studio/debug/dev-options"
  - "https://developer.android.com/tools/adb"
  - "https://source.android.com/docs/core/architecture/bootloader/locking_unlocking"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Android USB debugging and developer options

**Goal:** someone with your phone for a minute (or a malicious charger/computer) can't use ADB to pull data or
install apps.

## Check and turn off
Settings > System > **Developer options** (appears only if enabled by tapping Build number 7 times):
- **USB debugging**: off.
- **Wireless debugging**: off.
- **Revoke USB debugging authorizations**: tap, clears every computer that was previously trusted.
- **OEM unlocking**: off (allows bootloader unlock; leave off unless installing another OS).
- Master toggle at top: **Use developer options** off when you're done.

## Why it matters
With USB debugging on and a computer authorised (or when you accept the RSA prompt), ADB can install apps, back up
some app data, read logs, take screenshots and control the screen. Stalkerware installs often use it.

## Safe practice
- Only enable when you need it; revoke authorisations after.
- Never accept "Allow USB debugging?" prompts on unknown chargers/computers.
- Use "Charging only" USB mode on public ports, or a data blocker.

## Verify
`adb devices` from a computer should show nothing (or "unauthorized") when debugging is off.

## Gotchas
- Some OEMs keep developer options enabled after updates; recheck after major upgrades.
- Android's Advanced Protection mode restricts USB data signalling on locked phones on supported devices.
