---
id: creative-arts.music.ableton-live.max-for-live-devices
name: max-for-live-devices
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, max-for-live, m4l, lfo-device, envelope-follower, shaper, expression-control, amxd, device-editing, freeze-device]
level: practitioner
status: docs-checked
description: "Use Max for Live in Live: where it is included, the bundled LFO, Shaper, Envelope Follower and MIDI devices, editing devices in Max, AMXD files and freezing devices."
sources:
  - https://www.ableton.com/en/live-manual/12/max-for-live/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Max for Live devices

**Goal:** extend Live with modulators, utilities and custom devices.

## 1. Availability
- Max for Live is bundled with **Live Suite**, and with **Standard** when you use the Max for Live add-on.
- Max for Live devices are found under the Max for Live label in the browser, including devices from installed third-party Packs. Built-in devices also appear under Instruments, Audio Effects, MIDI Effects and Modulators.

## 2. Bundled devices
- Audio Effects: **LFO**, **Shaper**, **Envelope Follower**.
- MIDI Effects: **Envelope MIDI**, **Expression Control**, **Note Echo**, **Shaper MIDI**.
- See each device's section in the Max for Live chapter of the manual for its controls.

## 3. Editing devices
- Use **Edit in Max** from the device's context menu or the title bar's Show Options menu to open the Max editor (before Live 12.2 a dedicated Edit button was used).
- Saving a device automatically updates all instances of it.
- A Max device is saved as an **AMXD** file separately from the Live Set, in the User Library folder matching its device type.

## 4. External dependencies
- The file path to Max can be set in Live's File & Folder Settings.
- **Freeze** a Max device so it contains all the files needed to use it.

## Gotchas
- Because devices live outside the Set, a Set opened on another computer needs the same devices there; freezing a device helps.

## Verify
- Open the device with Edit in Max, save, and confirm other instances update.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Max for Live chapter (first 100,000 characters): bundling with Suite and Standard add-on, browser location, device names, Edit in Max and pre-12.2 button, save updating instances, AMXD files and User Library, File & Folder Settings path, freezing. Removed: Map-button workflows, modulation indicator, Random, Collect All and Save, live.* objects, CPU and latency claims, maxforlive.com and Cycling '74 links (not stated on the page).
Method: documentation only; no commands were run.
