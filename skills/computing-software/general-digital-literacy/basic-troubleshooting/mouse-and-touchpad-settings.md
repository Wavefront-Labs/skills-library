---
id: computing-software.general-digital-literacy.basic-troubleshooting.mouse-and-touchpad-settings
name: mouse-and-touchpad-settings
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-os-settings, touchpad-settings, mouse-settings, gestures]
level: intro
status: draft
description: "Adjust pointer speed, scrolling direction, tap-to-click, gestures and button swap for mice and touchpads on Windows, Mac and Chromebook, and fix a touchpad that stops working."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://support.google.com/chromebook
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mouse and touchpad settings

## Windows 11
- Settings > Bluetooth & devices > **Mouse**: primary button (left/right for left-handed users), pointer speed, scroll lines, *Scroll inactive windows*.
- **Touchpad**: sensitivity, *Taps* (tap to click, two-finger tap for right-click), *Scroll & zoom* direction ("Down motion scrolls down"), three/four-finger gestures (switch apps, show desktop).
- *Additional mouse settings* opens the classic dialog: double-click speed, pointer trails, *Enhance pointer precision*.
- Pointer size and colour: Accessibility > **Mouse pointer and touch**.

## Mac
- System Settings > **Trackpad**: *Point & Click* (tap to click, secondary click, tracking speed, Force Click), *Scroll & Zoom* (Natural scrolling), *More Gestures*.
- **Mouse**: tracking speed, natural scrolling, secondary click side.

## Chromebook
- Settings > Device > **Touchpad** / **Mouse**: tap-to-click, speed, reverse scrolling, acceleration.

## Touchpad stopped working
1. Check the touchpad toggle key (Fn + a key with a touchpad icon) or Settings > Touchpad *on*.
2. *Disable touchpad when a mouse is connected*: unplug the mouse.
3. Restart; then update or reinstall the driver (Device Manager > *Mice and other pointing devices* or *Human Interface Devices*).
4. Mac: reset NVRAM on Intel or check Accessibility > Pointer Control (*Ignore built-in trackpad when mouse is present*).

## Verify
- [ ] Pointer speed comfortable, scroll direction as expected, gestures work.
