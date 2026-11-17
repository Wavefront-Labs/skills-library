---
id: computing-software.general-digital-literacy.basic-troubleshooting.webcam-not-working
name: webcam-not-working
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, audio-problems, webcam-not-working, camera-privacy, camera-permissions, camera-shutter, camera-in-use, video-call-camera]
level: intro
status: docs-checked
description: "Fix a webcam that shows black or isn't found on Windows 11 or Mac: camera switch or shutter, Windows camera privacy access, Camera app test, other apps, drivers."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/camera/camera-doesn-t-work-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/camera/manage-cameras-with-camera-settings-in-windows-11
  - https://support.apple.com/guide/mac-help/use-the-camera-mchlp2980/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webcam not working

**Goal:** your video appears in the call.

## Windows 11 (in Microsoft's order)
1. **Connection:** an external camera must be firmly in its USB port; test it on another device to rule out hardware.
2. **Camera switch or button:** some laptops have an on/off switch or button. It may be a key used with `Fn`, a dedicated camera key, a sliding switch on the side, or a small shutter slider on the camera. When off, Windows may not see the camera, or may show a camera icon with a slash.
3. **App access:** Settings > Privacy & security > **Camera**. Turn on **Camera access** (if it is greyed out an administrator must turn it on), **Let apps access your camera**, and **Let desktop apps access your camera** (browsers such as Edge and apps such as Teams are desktop apps; access for individual desktop apps cannot be turned off).
4. **Test in another app:** Start > **Camera**. If it works there, the problem is the app's own settings. Another app may be using the camera; close it.
5. **Camera settings:** Settings > Bluetooth & devices > **Cameras** lists connected cameras; open one to see its settings, including whether it has been disabled (disabled cameras are listed separately with an Enable option).
6. **Updates and restart:** Settings > Windows Update > Check for updates (and Advanced options > Optional updates for camera drivers), then restart (waking from sleep is not a restart).
7. **Drivers:** Device Manager > **Cameras**: update or roll back the driver, or **Uninstall device**, restart, or use **Scan for hardware changes**. Then test in the Camera app.

## Mac
The camera turns on when an app such as FaceTime or Photo Booth uses it, and a green light beside it glows; it turns off when all apps that use it are closed. Test in Photo Booth. You can decide which apps may use the camera (the Mac User Guide's "Control access to the camera"). Wipe the lens with a soft, lint-free cloth.

## Verify
- [ ] The Camera app (Windows) or Photo Booth (Mac) shows your picture, then the calling app does too.

## Checked
Checked 2026-10-27 against Microsoft Support "Camera doesn't work in Windows" and "Manage cameras with Camera settings in Windows 11" and the Apple Mac User Guide "Use the camera on Mac". Confirmed: switch and shutter wording, privacy setting names, Camera app test, Cameras settings page and disable/enable, optional updates, Device Manager steps, Mac green light and Photo Booth. Removed unconfirmed claims (F8 or F10 keys, hub advice, IT policy, malware scan advice, Mac Privacy & Security path).
Method: documentation only; no commands were run.
