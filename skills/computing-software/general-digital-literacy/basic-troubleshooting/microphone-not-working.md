---
id: computing-software.general-digital-literacy.basic-troubleshooting.microphone-not-working
name: microphone-not-working
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, audio-problems, microphone-not-working, mic-permissions, input-device, privacy-microphone, mute-switch]
level: intro
status: docs-checked
description: "Fix a microphone others can't hear on Windows 11 or Mac: headset mute, input device, Windows microphone privacy access, input level test, driver reinstall."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/drivers/fix-microphone-problems
  - https://support.apple.com/guide/mac-help/connect-a-wireless-accessory-blth1004/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microphone not working

**Goal:** people on the call can hear you.

## Windows 11
1. **Headset mute:** make sure a Mute button on the headset is not active, and that the microphone or headset is connected properly (a Bluetooth headset must be paired and connected).
2. **App access:** Settings > Privacy & security > **Microphone**. Turn on **Microphone access** and **Let apps access your microphone**, then choose which apps have access. Desktop apps are not listed there; turn on **Let desktop apps access your microphone** for them (you cannot turn off access for individual desktop apps). If the microphone is in a webcam, also check Settings > Privacy & security > **Camera**.
3. **Default input:** Settings > System > **Sound** > *Input* > *Choose a device for speaking or recording* and select the headset or microphone.
4. **Test and level:** open the device's properties (the > to its right), under *Microphone test* select **Start test**, speak, **Stop test**, and play the recorded sample. Adjust the **Input volume** slider if needed.
5. **Troubleshoot:** Settings > System > Sound > Advanced > under *Troubleshoot common sound problems* choose **Input devices**.
6. **Not detected at all:** Device Manager > **Sound, video and game controllers** > right-click the audio device > **Uninstall device**, tick *Attempt to remove the driver for this device*, Uninstall; repeat for other audio devices, restart (Windows reinstalls them); if needed right-click the section > **Scan for hardware changes**, then right-click the audio driver > **Update driver**.

## Mac
System Settings > **Sound** > **Input**, then select the microphone or headset from the list. A Bluetooth headset is connected in System Settings > Bluetooth.

## Verify
- [ ] The Start test in Windows (or the app's own mic test) shows the level moving, and the recorded sample sounds right.

## Checked
Checked 2026-10-27 against Microsoft Support "Fix microphone problems in Windows" (Windows 11 section) and the Apple Mac User Guide "Connect a Bluetooth device with your Mac". Confirmed: privacy setting names and order, desktop-app toggle, default input and test steps, troubleshooter location, driver reinstall steps, Mac Sound Input. Removed unconfirmed claims (Zoom, Teams and Meet menu paths, 80 percent input level, Mac Privacy & Security microphone path, browser prompts, Bluetooth hands-free quality, physical mic-mute keys).
Method: documentation only; no commands were run.
