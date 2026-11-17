---
id: computing-software.it-support-helpdesk.desktop-support.mobile-connectivity-updates-and-touchscreen
name: mobile-connectivity-updates-and-touchscreen
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, bluetooth-troubleshooting, mobile-hotspot, esim, mobile-os-update, touchscreen-troubleshooting, cellular-data]
level: practitioner
status: draft
description: "Fix phone and tablet problems: Bluetooth pairing, cellular data, APN and hotspot, eSIM transfers, failed OS updates, and unresponsive or damaged touchscreens."
sources:
  - "https://support.apple.com/en-us/118259"
  - "https://support.google.com/android/answer/9075847"
  - "https://support.apple.com/en-us/118669"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mobile-connectivity-updates-and-touchscreen

## Bluetooth pairing
1. Toggle Bluetooth off/on on both devices; check the accessory's battery and that it's
   in pairing mode (often a long press until the LED flashes).
2. Forget the device on the phone and any other phone/laptop it auto-connects to (most
   headsets connect to the last device).
3. Restart the phone. Reset the accessory to factory (vendor-specific button combo).
4. Car kits: delete the phone from the car's list too; check permissions for contacts
   and messages.
5. Corporate: MDM may restrict Bluetooth or file transfer via Bluetooth.

## Cellular data, APN and hotspot
- No data but calls work: mobile data toggle per app (iOS Settings > Cellular lists apps),
  data roaming off abroad, data limit reached, APN wrong.
- APN: iOS sets it from the carrier profile (Settings > Cellular > Cellular Data Network
  if exposed); Android Settings > Network > SIM > Access Point Names. Corporate APNs
  (private APN) are pushed by MDM.
- Hotspot missing: carrier plan doesn't include tethering, or MDM blocks Personal
  Hotspot (supervised restriction). Laptop can't connect: change hotspot band to
  2.4 GHz/"maximise compatibility", rename hotspot without special characters.
- Reset network settings as a later step (forgets Wi-Fi passwords and VPN profiles).

## eSIM transfer
- iPhone to iPhone: during setup or Settings > Cellular > Add eSIM > Transfer from nearby
  iPhone (carrier must support Quick Transfer). Otherwise the carrier issues a QR code.
- Android: Settings > Network > SIMs > transfer, or carrier QR/app; cross-platform
  transfers usually need the carrier.
- Corporate lines: the telecom admin (carrier portal) issues the eSIM; wiping a phone
  may delete the eSIM, so choose "keep eSIM" when erasing if the line moves with the
  user.

## OS update failures
- Not enough storage (iOS needs several GB free); low battery (connect power); MDM
  deferral or enforced version (supervised devices); unstable Wi-Fi.
- iOS: delete the downloaded update (Settings > General > iPhone Storage > the update)
  and retry; update via computer (Finder/Apple Devices app) if OTA fails.
- Android: OEM/carrier controls availability; Settings > System > Software update;
  clear storage of the update app; Google Play system update is separate.

## Touchscreen unresponsive
- Remove case and screen protector, clean screen, dry hands.
- Force restart (iPhone: volume up, volume down, hold side button).
- Partial dead zones after a drop or touch "ghosting": hardware; arrange repair/swap.
- Cracked screens on corporate devices: repair via vendor or insurance; back up first,
  check Activation Lock is managed before sending away.
- Swollen battery lifting the screen: stop using, don't charge, dispose correctly.

## Verify
The user confirms the accessory, data or hotspot works in their real scenario, the device
reports the current supported OS, and repairs are tracked against the asset.
