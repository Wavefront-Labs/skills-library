---
id: creative-arts.music.ableton-live.mapping-midi-controllers-and-control-surfaces
name: mapping-midi-controllers-and-control-surfaces
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-performance, midi-mapping, control-surface, key-mapping, midi-map-mode, takeover-mode, remote-scripts, mapping-browser, min-max-ranges, controller-setup]
level: practitioner
status: docs-checked
description: "Map controllers in Live: Control Surface chooser, Remote ports, MIDI and Key Map modes, Min/Max ranges and inversion, and takeover modes."
sources:
  - https://www.ableton.com/en/live-manual/12/midi-and-key-remote-control/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Mapping MIDI controllers and control surfaces (Live)

**Goal:** physical controls that do exactly what you want in Live, reliably.

## 1. Control Surface or manual setup
- In the Link, Tempo & MIDI settings, pick a natively supported controller from the Control
  Surface chooser, or set the controller up manually. Up to six control surfaces can be
  used at once. Some controllers need a preset dump (the Dump button).
- Manual setup: set the **Remote** switch On for each MIDI input port used for remote
  control. Also enable Remote on the output port if the controller has motorised faders or
  LEDs that need feedback.
- MIDI keys that become part of remote control assignments can no longer be used as input
  for MIDI tracks.

## 2. MIDI Map mode (custom)
1. Click the **MIDI** switch in the upper right; assignable elements turn blue.
2. Click a parameter, then send a MIDI message from the controller. The mapping appears in
   the **Mapping Browser**.
3. The Mapping Browser lists each control, its parameter path and name, and Min and Max
   values. Edit Min and Max at any time; invert from the context menu.
- Absolute controllers (0-127) map onto the parameter's range. For switches, values inside
  the Min-Max range turn the switch on; if Min is higher than Max the behaviour reverses.

## 3. Key Map mode
- Click the **KEY** switch; assignable elements get a red overlay (only those can be
  mapped). Click a parameter, press a computer key, and the mapping appears in the
  Mapping Browser.

## 4. Takeover mode
For controls that are not motorised:
- **None**: the new value is sent immediately and may jump.
- **Pick-Up**: the control has no effect until it reaches the parameter's current value.
- **Value Scaling**: control and parameter converge smoothly before tracking 1:1.

## Verify
- Move each control: the intended parameter moves within the set range, no jumps with Pick-Up.
- Re-open the Mapping Browser and check Min/Max for each entry.

## Checked
2026-11-01. Confirmed against the Live 12 manual chapter "MIDI and Key Remote Control": control surface chooser and six-surface limit, Dump, Remote toggle on input and output ports, MIDI and KEY switches and colours, Mapping Browser Min/Max and inversion, switch range behaviour, three Takeover modes. Removed (not on that page): keyboard shortcuts, list of supported controllers, Track-port wording, mapping-storage claims, rack-macro advice and the gotchas section.
Method: documentation only; no commands were run.
