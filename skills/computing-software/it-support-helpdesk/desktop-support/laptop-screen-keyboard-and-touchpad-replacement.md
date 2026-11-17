---
id: computing-software.it-support-helpdesk.desktop-support.laptop-screen-keyboard-and-touchpad-replacement
name: laptop-screen-keyboard-and-touchpad-replacement
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, laptop-hardware, hardware-replacement, laptop-screen-replacement, lcd-panel, edp-cable, keyboard-replacement, touchpad, palmrest, digitizer, comptia-a-plus]
level: practitioner
status: draft
description: "Isolate and replace failed laptop displays, keyboards and touchpads: external-monitor test, panel vs cable vs GPU, matching panel part numbers, and palmrest-integrated keyboards."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.dell.com/support/manuals/"
  - "https://support.hp.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# laptop-screen-keyboard-and-touchpad-replacement

Goal: replace the part that's actually faulty, sourced to the exact
sub-model.

## Display: isolate first
| Test | Result → cause |
|---|---|
| External monitor shows image | GPU fine → panel, eDP cable or backlight |
| Torch on dark screen shows faint image | backlight/inverter (or brightness 0 / key toggle) |
| Image changes when lid angle changes | eDP cable/hinge routing |
| Lines in BIOS screen too | panel or cable, not driver |
| Lines only in Windows | driver — roll back/update GPU driver |
| Vendor built-in LCD test (Dell: hold D + power; HP/Lenovo diagnostics) | fails = panel hardware |
Physical damage (cracked glass) = panel, possibly digitizer (touch) too.

## Panel replacement
- Part number from the service tag lookup — same size differs by
  resolution, touch/non-touch, refresh rate, connector pin count (30 vs 40
  pin eDP), privacy screen.
- Bezel clips or adhesive; on many modern laptops the panel is glued and
  sold as a full lid assembly — order the assembly.
- Disconnect battery first; reseat the eDP connector fully and re-tape it.
- Touch panels: run calibration (Tablet PC Settings) if touch misaligns.

## Keyboard
- External USB keyboard works → laptop keyboard hardware (or Filter Keys /
  layout issue — check Settings first).
- Liquid spill: power off immediately, don't power-test wet; corrosion
  appears days later.
- Many models: keyboard is riveted to the palmrest/top cover → order the
  palmrest assembly (includes touchpad/fingerprint sometimes); Lenovo
  ThinkPads often screw-in from below.

## Touchpad
- Enable check: Fn key toggle, Settings → Bluetooth & devices → Touchpad
  on, precision touchpad driver present.
- Not clicking or raised: swollen battery underneath — treat as battery
  incident, not touchpad fault.
- Ribbon cable reseat after any palmrest work.

## Gotchas
- On-site warranty (Dell ProSupport, HP Care Pack) usually covers these with
  next-business-day techs — fitting it yourself may void it.
- Accidental damage cover vs standard warranty: spills/cracks are only
  covered with ADP.

## Verify
Built-in diagnostics pass (LCD test, keyboard key-by-key test), touch and
brightness controls work, lid opens/closes across full hinge range without
flicker.
