---
id: computing-software.general-digital-literacy.basic-troubleshooting.no-sound-from-speakers-or-headphones
name: no-sound-from-speakers-or-headphones
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, audio-problems, no-sound, sound-settings, output-device, volume-mixer, audio-troubleshooter, hdmi-audio, mute]
level: intro
status: docs-checked
description: "Fix no sound on Windows 11 or Mac: check mute and the volume mixer, pick the right output (HDMI monitor, headphones), turn off enhancements, run the troubleshooter."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/audio/fix-audio-issues-when-no-sound-plays-from-speakers-or-headphones-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/audio/fix-sound-or-audio-problems-in-windows
  - https://support.apple.com/guide/mac-help/connect-a-wireless-accessory-blth1004/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# No sound from speakers or headphones

**Goal:** get audio back, starting with the simplest causes.

## Windows 11
1. **Output device:** Settings > System > **Sound**; under **Output** select the right device, and make sure the volume is not muted and the slider is up. Selecting a device there also makes it the default.
2. **Taskbar flyout:** right-click the speaker icon, or select the arrow to the right of the volume slider (tooltip *Select a sound output*) to see the connected devices. The settings icon beside the volume mixer slider (tooltip *More mixer settings*) opens the volume mixer; an "x" next to a control means it is muted.
3. **Disabled device:** Settings > System > Sound > Advanced > **More sound settings** > Playback (or Recording) tab > select the device > Properties > *Device usage* should be **Use this device (enable)**. Right-click a device on the Playback tab > **Set as default** if needed.
4. **Audio enhancements:** Settings > System > Sound > Output > select your device > Advanced settings > set **Audio enhancements** to Off.
5. **Troubleshooter:** run the audio troubleshooter in the **Get Help** app, or Settings > System > Troubleshoot > Other troubleshooters > Audio > Run.
6. **Drivers:** Start search "device manager" > expand **Sound, video and game controllers** > right-click the device > **Update driver** > Search automatically. If that fails, **Uninstall device**, tick *Attempt to remove the driver for this device*, Uninstall, then restart (Windows reinstalls the driver).
7. **Updates and restart:** Settings > Windows Update > Check for updates, then restart.

## Mac
System Settings > **Sound**, click **Output** (or **Input** for a microphone), and select the device you want. Bluetooth audio devices are connected first in System Settings > Bluetooth (hold the pointer over the device > Connect).

## Gotchas
- HDMI or USB audio: set that device as the output. A monitor with no speakers selected as the output gives no sound, so choose another device.
- Wireless headphones still connected to another device may be the active output.

## Verify
- [ ] Sound plays through the device selected under Output.

## Checked
Checked 2026-10-27 against Microsoft Support "Fix audio issues when no sound plays from speakers or headphones in Windows" and "Fix sound or audio problems in Windows" (Windows 11 and 10 sections), and the Apple Mac User Guide "Connect a Bluetooth device with your Mac". Confirmed: Windows 11 menu paths, flyout and mixer wording, Device usage setting, enhancement setting, troubleshooter path, driver update and uninstall steps, Mac Sound Output and Input. Removed unconfirmed claims (Troubleshoot common sound problems in Sound for output, front-panel jack, Mac balance and core audio restart).
Method: documentation only; no commands were run.
