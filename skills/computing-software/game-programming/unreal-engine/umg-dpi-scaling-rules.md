---
id: computing-software.game-programming.unreal-engine.umg-dpi-scaling-rules
name: umg-dpi-scaling-rules
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, dpi-scaling, umg, ui-scaling, resolution, game-programming]
level: practitioner
status: draft
description: "Configure Unreal UI DPI scaling: DPI curve by shortest side, design resolution, safe zones and custom DPI rules so UMG layouts work from 720p to 4K and ultrawide."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/dpi-scaling-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-safe-zones-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/Engine/Engine/UUserInterfaceSettings/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UMG DPI scaling rules

**Goal:** HUD and menus scale predictably across resolutions and aspect ratios.

## Settings (Project Settings > Engine > User Interface)
- **DPI Scale Rule**: Shortest Side (default, good for landscape games), Longest Side, Horizontal,
  Vertical, Scale to fit, Custom.
- **DPI Curve**: maps the measured side (pixels) to a scale. Default: 1080 -> 1.0, 720 -> 0.667,
  2160 -> 2.0. Author layouts at the reference (1920x1080) where scale is 1.
- **Application Scale**: global multiplier; expose to players as a UI size accessibility setting
  (`UUserInterfaceSettings::ApplicationScale` or `FSlateApplication::SetApplicationScale`).
- **Custom DPI rule**: subclass `UDPICustomScalingRule` and override `GetDPIScaleBasedOnSize` for cases
  like "scale by height but clamp for ultrawide".

## Layout practices
- Anchor elements to corners/edges; use Scale Box and Size Box for content that must keep aspect.
- Ultrawide: Shortest Side keeps vertical size; HUD anchored to edges spreads out. Consider a
  centred 16:9 Size Box for important HUD clusters.
- Text: use font sizes designed at 1080p; DPI scaling handles 4K. Avoid tiny fonts that become
  unreadable at 720p (0.667 scale).

## Safe zones
Wrap HUD roots in **Safe Zone** widgets for TV overscan and notches; test with
`r.DebugSafeZone.Mode 1` and `r.DebugSafeZone.TitleRatio 0.9`, plus device profiles for mobile.

## Preview
UMG designer: Screen Size dropdown and DPI preview show the scale; play-in-editor with
`r.SetRes 1280x720w` and `r.SetRes 3840x2160w` to check.

## Gotchas
- Mixing Scale Boxes with DPI scaling can double scale; know which one owns sizing.
- Render targets and Canvas HUD drawing do not use DPI scale; scale manually.

## Verify
- [ ] UI checked at 720p, 1080p, 1440p, 4K, 21:9 and with safe zone 90%; nothing clipped or tiny.
