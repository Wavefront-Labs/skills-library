---
id: computing-software.digital-privacy-hygiene.password-managers.sharing-wifi-by-qr-code
name: sharing-wifi-by-qr-code
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, wifi-qr-sharing, password-sharing, guest-network]
level: practitioner
status: draft
description: "Share Wi-Fi credentials by QR code or nearby-share instead of reading the password aloud, and generate a printable guest QR safely."
sources:
  - "https://support.apple.com/en-us/102349"
  - "https://support.google.com/android/answer/9075847"
  - "https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sharing Wi-Fi by QR code

**Goal:** guests join without seeing or retyping the password, and the main network password isn't spread around.

## Phones
- **Android:** Settings > Network & internet > Internet > gear next to the network > **Share** (unlock) >
  QR code shown. The other phone scans with the camera.
- **iPhone:** bring a nearby iPhone (in your contacts) to the join screen; your phone pops up "Share
  Password". Or Settings > Wi-Fi > (i) > Password (Face ID) to copy.
- **Windows 11:** Settings > Network & internet > Wi-Fi > network properties > Share (shows QR).

## Printable guest QR
Format (WPA/WPA2/WPA3 personal):
```
WIFI:T:WPA;S:GuestNet;P:correct-horse-battery;;
```
Escape `\ ; , : "` in SSID/password with a backslash. Generate offline:
```
qrencode -o guest-wifi.png 'WIFI:T:WPA;S:GuestNet;P:correct-horse-battery;;'
```
Avoid online QR generators: you'd be sending the password to a website.

## Hygiene
- Put the QR on the **guest** network only; keep the main/IoT network password private.
- Rotate the guest password when you change tenants/Airbnb guests; reprint.
- Store the Wi-Fi password in the vault as a Wi-Fi item.

## Gotchas
- WPA3-only networks need `T:SAE` for some scanners; WPA works on most phones.
- A photo of the QR is a photo of the password.
