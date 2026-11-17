---
id: computing-software.general-digital-literacy.basic-troubleshooting.bluetooth-headphones-pairing-and-switching
name: bluetooth-headphones-pairing-and-switching
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, audio-video, bluetooth-headphones, bluetooth-pairing, airpods, audio-output-switching]
level: intro
status: docs-checked
description: "Pair Bluetooth headphones and earbuds with Windows 11 and Mac, choose them as audio output, and fix ones that will not connect by removing and re-adding them."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/bluetooth/pair-a-bluetooth-device-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/bluetooth/troubleshoot-bluetooth-not-connecting-in-windows
  - https://support.apple.com/guide/mac-help/connect-a-wireless-accessory-blth1004/mac
  - https://support.apple.com/guide/mac-help/connect-airpods-to-your-mac-mchld2f124d1/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bluetooth headphones: pairing and switching

**Goal:** headphones connect to the right device and play through it.

## Pairing mode
Turn the headphones on and make them discoverable; how depends on the device, so check its manual or the maker's site.

## Windows 11
- Turn Bluetooth on: Settings > Bluetooth & devices, or the Bluetooth tile in quick settings (select the Network, Sound or Battery icon by the clock).
- Pair: in quick settings select the **Manage Bluetooth devices** chevron on the Bluetooth tile, then pick the device under **New devices**, follow any prompts and select **Done**. If the device supports **Swift Pair**, a notification appears when it is nearby and discoverable; select **Connect**.
- Once paired, it connects automatically whenever it is in range with Bluetooth on.
- **Output:** Settings > System > Sound > Output, select the headphones.

## Mac
- System Settings > **Bluetooth**; hold the pointer over the device in the list and click **Connect**, then Accept if asked. You can also use Control Center.
- **Output or input:** System Settings > **Sound** > Output (headphones) or Input (headset) and pick the device.
- **AirPods:** with the AirPods in the case, open the lid and press and hold the setup button on the back of the case (the noise control button on AirPods Max) until the light flashes white, then Connect in System Settings > Bluetooth. Their settings let them connect automatically or only when last connected to this Mac.
- Disconnect: hover over the device > **Disconnect**. To stop it reconnecting, Control-click its name > **Forget**.

## Will not connect
Microsoft's order for Windows 11:
1. Run the Bluetooth troubleshooter in the Get Help app.
2. Make sure Bluetooth is on and the device is in pairing mode and close to the PC.
3. Remove and re-add it: Settings > Bluetooth & devices > the device's ... menu > **Remove device**, then **Add device**.
4. Charge the headphones (low battery can stop pairing or connection) and switch them off and on; keep rechargeable ones plugged in while pairing.
5. Turn Bluetooth off, wait 10 seconds, turn it on, and pair again.
6. Check for Windows updates and restart the PC.

## Verify
- [ ] Audio plays through the headphones and the right output is selected.

## Checked
Checked 2026-10-27 against Microsoft Support "Pair a Bluetooth device in Windows" and "Troubleshoot Bluetooth not connecting in Windows" (Windows 11 sections) and the Apple Mac User Guide pages "Connect a Bluetooth device with your Mac" and "Use AirPods with your Mac". Confirmed: quick-settings pairing path, Swift Pair, remove and re-add, battery, 10-second off/on, Mac Connect, Forget, Sound Output and Input, AirPods pairing steps. Removed unconfirmed claims (iPhone and Android pairing paths, multipoint, 10 metre range, USB 3 interference, firmware updates, Hands-Free call quality advice, Apple Account switching).
Method: documentation only; no commands were run.
