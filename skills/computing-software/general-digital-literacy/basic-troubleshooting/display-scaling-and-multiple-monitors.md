---
id: computing-software.general-digital-literacy.basic-troubleshooting.display-scaling-and-multiple-monitors
name: display-scaling-and-multiple-monitors
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, system-settings, display-scaling, multiple-monitors, screen-resolution, extend-displays, win-p, arrange-displays]
level: intro
status: docs-checked
description: "Fix a tiny or blurry screen and set up a second monitor on Windows 11 and Mac: recommended resolution and scale, extend or duplicate, identify, detect and arrange displays."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/display-graphics/change-your-screen-resolution-and-layout-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/display-graphics/how-to-use-multiple-monitors-in-windows
  - https://support.apple.com/guide/mac-help/change-your-displays-resolution-mchl86d72b76/mac
  - https://support.apple.com/guide/mac-help/connect-an-external-display-mchl7c7ebe08/mac
  - https://support.apple.com/guide/mac-help/extend-mirror-mac-desktop-multiple-displays-mchlb5f905a1/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Display scaling, resolution and multiple monitors

**Goal:** a comfortable, sharp screen and a second monitor that behaves.

## Size and sharpness (Windows 11: Settings > System > Display)
With external displays connected, first select the display you want to change.
- **Scale** (Scale & layout section): typically choose the option marked *(Recommended)*.
- **Display resolution:** usually stick with the one marked *(Recommended)*. Monitors accept lower resolutions, but text is less sharp and the picture may be small, centred, edged with black, or stretched.
- Unexpected resolution changes: the graphics driver may need updating (Settings > Windows Update > Check for updates).
- **Display orientation** is in the same section; if you rotate a monitor in software, you must also physically rotate it.

## Mac (System Settings > Displays)
By default the Mac uses the best resolution for the display; Apple recommends keeping it. To change it, select a resolution from the thumbnails (Control-click and choose *Show List* for a list; *Advanced > Show resolutions as list* keeps the list). With several displays, select the display first.
- Black screen after changing resolution: wait 15 seconds, then press **Esc** to revert. If that fails, start in safe mode and click **Default** in Displays.

## Second monitor
1. Check cables are firmly connected to the PC or dock, and check for Windows updates.
2. **Windows:** press `Win+P` and choose *PC screen only*, *Duplicate* (same on all), *Extend* (one desktop across screens), or *Second screen only*.
3. Settings > System > Display: **Identify** shows each display's number; **Multiple displays > Detect** finds a display that is missing; drag the numbered displays to match how they sit on your desk and select **Apply**.
4. Windows 11 Display > **Multiple displays** has the checkboxes *Remember window locations based on monitor connection* and *Minimize windows when a monitor is disconnected*.
5. **Mac:** Displays > select the display > the *Use as* pop-up menu sets extend or mirror. Hold **Option** to turn the Night Shift button into **Detect Displays**.
6. Mac with an unrecognised display: unplug and replug it, check it is on, check the cable, adapter and port, then sleep and wake the Mac. Check your Mac supports that many displays (Help > your Mac's Specifications > Display Support).

## Verify
- [ ] Text is crisp at the recommended resolution and the pointer crosses between screens where you expect.

## Checked
Checked 2026-10-27 against Microsoft Support "Change your screen resolution and layout in Windows" and "How to use multiple monitors in Windows" (Windows 11 sections) and the Apple Mac User Guide pages for resolution, external displays and extend or mirror. Confirmed: menu paths, Recommended wording and lower-resolution effects, Win+P options, Identify, Detect, Apply, window-location checkboxes, Esc revert after 15 seconds, Option for Detect Displays, Use as menu. Removed unconfirmed claims (percentage scale advice, high DPI compatibility option, "Make this my main display", Win+Shift+arrow window moves, Mac Larger Text option names, USB-C alternate mode detail).
Method: documentation only; no commands were run.
