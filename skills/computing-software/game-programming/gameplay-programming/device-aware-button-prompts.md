---
id: computing-software.game-programming.gameplay-programming.device-aware-button-prompts
name: device-aware-button-prompts
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, input-glyphs, button-prompts, input-device-detection, game-programming]
level: practitioner
status: draft
description: "Show correct button glyphs per device: last-used-device detection, binding-driven prompt lookup, platform glyph rules and hot-swap without flicker."
sources: ["https://partner.steamgames.com/doc/features/steam_controller/getting_started_for_devs", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/manual/ActionBindings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Device-aware button prompts and glyphs

**Goal:** prompts always show the button the player actually has bound, on the device they are holding.

## Last-used device
Track the device that produced the most recent *meaningful* input (button press, stick beyond dead
zone, mouse move beyond a few pixels). Ignore analog noise or the prompts flicker between devices.
Add hysteresis: switch scheme only after input from the new device, not on connect.

## Lookup from bindings, not constants
```text
prompt("Interact") -> binding table for current scheme -> control path (e.g. buttonSouth)
                   -> glyph set for device family (Xbox A, PlayStation Cross, Switch B position) -> sprite
```
- Store glyphs by control path and device family. Generic gamepad paths (`buttonSouth`) map to
  different labels per family.
- Steam Input: query the origin for an action with `GetDigitalActionOrigins` and use
  `GetGlyphPNGForActionOrigin` so remaps done in the Steam overlay show correctly.
- Rebuild visible prompts on scheme change and on rebind events.

## Platform rules
- Console certification requires the platform's own glyphs and terminology; Switch swaps confirm
  and cancel positions relative to Xbox. Japanese PlayStation titles historically swapped
  Circle/Cross confirm.
- Keyboard prompts show key names via the OS keyboard layout (AZERTY "A" sits where QWERTY "Q" is);
  query the layout-aware display name instead of hard-coding.

## Text with inline glyphs
Use rich-text tags like `Press <action=Interact> to open` and substitute at render time, so
localisation does not have to embed device-specific glyphs.

## Verify
- Swap from pad to keyboard mid-sentence; prompt updates within one frame, no flicker on idle.
- Remap Interact and confirm every tutorial and HUD prompt follows.
