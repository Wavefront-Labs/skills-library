---
id: computing-software.general-digital-literacy.basic-troubleshooting.finding-a-saved-wifi-password
name: finding-a-saved-wifi-password
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-connectivity, wifi-password, saved-networks, share-wifi]
level: intro
status: draft
description: "See the password of a Wi-Fi network you are connected to or saved on Windows, Mac, iPhone and Android, or find it on the router, to connect a new device."
sources:
  - https://support.microsoft.com/en-us/windows/find-your-wi-fi-network-password-in-windows-2ec74b2e-d9ac-4d6e-ad9c-0fa4e3b7aeb5
  - https://support.apple.com/en-us/108049
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Find a saved Wi-Fi password

## Windows 11
- Settings › Network & internet › Wi-Fi › **Manage known networks** › network › **View Wi-Fi security key** (recent builds).
- Older: Control Panel › Network and Sharing Center › your Wi-Fi › **Wireless Properties** › Security › *Show characters*.
- Any saved network: `netsh wlan show profiles` then `netsh wlan show profile name="HomeWiFi" key=clear` › *Key Content*.

## Mac
- System Settings › Wi-Fi › ⋯ next to the network (or *Advanced…* › known networks) › **Copy Password**. Or the **Passwords** app (macOS 15+) › Wi-Fi; older: Keychain Access › search the network name › Show password (needs your Mac password).

## iPhone / iPad (iOS 16+)
- Settings › Wi-Fi › ⓘ next to the network › tap **Password** (Face ID). Or share to a nearby Apple device in your contacts: it offers *Share Password* automatically.

## Android (10+)
- Settings › Network & internet › Internet › gear next to the network › **Share** › shows a QR code and (on many phones) the password in text.

## Still unknown
- Router sticker: *WiFi Key/WPA Key* — valid only if nobody changed it.
- Router admin page/app (address on the sticker, e.g. 192.168.1.1) › Wireless settings.
- Guests: a separate guest network keeps your main password private.

## Verify
- [ ] The new device connects with the password you found.
