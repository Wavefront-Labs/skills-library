---
id: computing-software.game-programming.unreal-engine.enhanced-input-platform-settings-and-context-swaps
name: enhanced-input-platform-settings-and-context-swaps
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, input-platform-settings, enhanced-input, mapping-context, platform-input, game-programming]
level: practitioner
status: draft
description: "Configure Unreal Enhanced Input per platform: platform-specific mapping contexts and settings, swapping contexts by device or game state, and redirecting contexts per platform."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Plugins/EnhancedInput/UEnhancedInputPlatformSettings/", "https://docs.unrealengine.com/5.3/en-US/API/Plugins/EnhancedInput/UEnhancedInputLocalPlayerSubsystem/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enhanced Input platform settings and context swaps

**Goal:** console, PC and mobile get the right bindings, and gameplay/menus/vehicles switch contexts
cleanly.

## Platform settings
Project Settings > Engine > Enhanced Input > **Platform Settings** (per platform tab, UE5.1+):
- **Context Redirects**: map a base mapping context to a platform one (`IMC_Default` ->
  `IMC_Default_Switch` with face buttons swapped). Code keeps adding `IMC_Default`.
- Input data assets per platform (via `UEnhancedInputPlatformData`).
- Other per-platform options: whether to show debug, user settings class.

## Context management
```cpp
auto* Sub = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PC->GetLocalPlayer());
Sub->AddMappingContext(IMC_OnFoot, /*Priority*/0);
// entering a vehicle
Sub->RemoveMappingContext(IMC_OnFoot);
Sub->AddMappingContext(IMC_Vehicle, 0);
// menu overlay that must win conflicts
Sub->AddMappingContext(IMC_Menu, 100);
```
- Higher priority wins when contexts map the same key; lower ones still receive unconflicted keys.
- `FModifyContextOptions{ bIgnoreAllPressedKeysUntilRelease = true }` (default) prevents a held key
  firing in the new context.
- Use `ClearAllMappings` sparingly; it also removes contexts other systems added.

## Device-based swaps
Detect last input device via `UCommonInputSubsystem::OnInputMethodChangedNative` (CommonUI) or
`IPlatformInputDeviceMapper`, then swap UI glyphs; keep both KBM and gamepad keys in one context
where possible rather than swapping contexts per device.

## Gotchas
- Contexts are per local player; split-screen requires adding to each player's subsystem.
- Adding contexts in BeginPlay before the PlayerController possesses the pawn fails on clients;
  use `PawnClientRestart`/`SetupPlayerInputComponent` or possession events.
- Player Mappable settings (remaps) are keyed by context; redirects must keep mapping names stable.

## Verify
- [ ] `showdebug enhancedinput` lists the expected contexts and priorities in each game state.
- [ ] A platform build uses its redirected context without code changes.
