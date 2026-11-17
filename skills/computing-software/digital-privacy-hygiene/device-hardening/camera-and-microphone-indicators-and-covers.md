---
id: computing-software.digital-privacy-hygiene.device-hardening.camera-and-microphone-indicators-and-covers
name: camera-and-microphone-indicators-and-covers
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, camera-indicators, microphone-privacy, webcam-cover, privacy-indicators]
level: practitioner
status: draft
description: "Read camera and mic privacy indicators on iOS, Android, macOS and Windows, find which app used them, and use webcam covers without damaging laptops."
sources:
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://support.google.com/android"
  - "https://support.apple.com/guide/mac-help/welcome/mac"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Camera and microphone indicators and covers

**Goal:** know when your camera or mic is on, which app turned it on, and when to physically block it.

## Indicators
| Platform | Camera | Microphone | Which app? |
|---|---|---|---|
| iPhone/iPad | Green dot | Orange dot | Open Control Center: app name shown at top |
| Android 12+ | Green indicator, top right | Same indicator | Tap it to see the app; quick settings toggles block camera/mic access entirely |
| Mac | Green LED next to camera (hardware-linked) | Orange dot in menu bar | Control Center shows app |
| Windows | Camera LED on most laptops; taskbar camera/mic privacy icon | Taskbar mic icon | Settings > Privacy & security > Camera / Microphone > "Recent activity" |

If an app you didn't expect used them, revoke its permission and investigate it.

## Covers
- External webcams and desktops: a cover or unplugging works.
- **MacBooks**: Apple warns that covers thicker than 0.1 mm can damage the display when closed; rely on the green
  LED or use a very thin cover and remove it before closing.
- Phones: covers interfere with Face ID; use the indicators and permissions.

## Microphones
No cover blocks a mic well. Use Android/iOS permissions and Android's mic toggle; on laptops, disable the device in
system settings or use a hardware kill switch if present (some Linux laptops have them).

## Gotchas
- Smart speakers, TVs and doorbells have mics too; use their physical mute button.
- Malware with kernel access can, in rare cases, bypass software indicators; hardware LEDs tied to camera power are
  more trustworthy.
