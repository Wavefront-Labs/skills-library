---
id: computing-software.game-programming.unreal-engine.player-mappable-key-settings-and-remapping
name: player-mappable-key-settings-and-remapping
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, enhanced-input, player-mappable-keys, key-remapping, enhanced-input-user-settings, input-settings-ui, game-programming]
level: practitioner
status: draft
description: "Let players remap keys with Enhanced Input User Settings: Player Mappable Key Settings on actions, MapPlayerKey, key profiles, saving, and building the remap UI."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/EnhancedInput/UEnhancedInputUserSettings"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Player mappable key settings and remapping

**Goal:** a controls menu where players rebind keys per action, saved per user, using the UE 5.3+
Enhanced Input User Settings system.

## Enable
- Project Settings > Engine > Enhanced Input > **User Settings > Enable User Settings** (and optionally a
  custom `UEnhancedInputUserSettings` subclass / key profile class).
- On each **Input Action** (or per mapping in the IMC), set **Player Mappable Key Settings**:
  `Name` (unique, stable: `Jump`), `Display Name`, `Display Category`. Mappings with "Is Player Mappable"
  are exposed.
- Register contexts so their mappings appear in settings: `UserSettings->RegisterInputMappingContext(IMC)`
  (contexts added via the subsystem can register automatically, per the "Register with settings" option).

## Remap
```cpp
UEnhancedInputLocalPlayerSubsystem* S = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(LP);
UEnhancedInputUserSettings* Settings = S->GetUserSettings();

FMapPlayerKeyArgs Args;
Args.MappingName = TEXT("Jump");
Args.Slot = EPlayerMappableKeySlot::First;      // primary / secondary binding
Args.NewKey = EKeys::SpaceBar;
FGameplayTagContainer Failure;
Settings->MapPlayerKey(Args, Failure);
Settings->ApplySettings();
Settings->AsyncSaveSettings();                    // persists to the user's save slot
```
- `UnMapPlayerKey`, `ResetAllPlayerKeysInRow`, key profiles (`CreateNewKeyProfile`, `SetKeyProfile`) for
  presets (default, left-handed).
- Query for UI: `Settings->GetCurrentKeyProfile()->GetPlayerMappingRows()` gives rows of
  `FKeyMappingRow` with `Mappings` (key, slot, display name, category).
- Capturing a key in UMG: CommonUI / `UInputKeySelector` widget returns an `FInputChord`; feed its key into
  `MapPlayerKey`.

## Conflicts
Detect duplicates yourself: before mapping, scan rows for the same key in contexts that are active
together (on-foot vs vehicle can share keys). Offer swap or reject.

## Older approach
UE 5.0-5.2: `PlayerMappableInputConfig` assets + `AddPlayerMappedKey` on the subsystem (deprecated in 5.3+).
Lyra predates parts of the new system; check which API your engine version expects.

## Gotchas
- `Name` in Player Mappable Key Settings is the save key; renaming it orphans players' saved bindings.
- Modifiers/triggers on the mapping stay; remapping W to Up Arrow keeps the Swizzle modifier.
- Display strings: `Key.GetDisplayName()`; map gamepad keys to icon brushes for UI.

## Verify
- [ ] Rebound key works immediately and after restarting the game.
- [ ] Reset to defaults restores the original IMC keys.
