---
id: computing-software.game-programming.unreal-engine.input-modes-game-ui-and-mouse-cursor
name: input-modes-game-ui-and-mouse-cursor
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, enhanced-input, setinputmode, mouse-cursor, input-mode-ui, game-programming]
level: practitioner
status: draft
description: "Switch Unreal input modes between game, UI and game-and-UI correctly: SetInputMode variants, cursor visibility, widget focus, mouse lock and CommonUI's alternative."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/GameFramework/APlayerController/SetInputMode", "https://dev.epicgames.com/documentation/en-us/unreal-engine/common-ui-quickstart-guide-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input modes: game vs UI and the mouse cursor

**Goal:** opening a menu frees the cursor and blocks gameplay input; closing it restores mouse look —
on every platform, without stuck states.

## The three modes (APlayerController::SetInputMode)
```cpp
// Gameplay
FInputModeGameOnly GameOnly;
PC->SetInputMode(GameOnly); PC->SetShowMouseCursor(false);

// Pause menu
FInputModeUIOnly UIOnly;
UIOnly.SetWidgetToFocus(Menu->TakeWidget());
UIOnly.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
PC->SetInputMode(UIOnly); PC->SetShowMouseCursor(true);

// Inventory over live game (camera still rotates with right mouse, etc.)
FInputModeGameAndUI Both;
Both.SetWidgetToFocus(Inv->TakeWidget()); Both.SetHideCursorDuringCapture(false);
PC->SetInputMode(Both); PC->SetShowMouseCursor(true);
```
Blueprint: Set Input Mode Game Only / UI Only / Game And UI + Show Mouse Cursor.

## Behaviour notes
- UI Only: viewport doesn't receive input; Enhanced Input game actions stop. Escape to close the menu
  must be handled by the widget (`NativeOnKeyDown`) or a UI action.
- Game And UI: clicking the viewport captures the mouse (with `HideCursorDuringCapture` default true it
  hides). Mouse capture mode settings in Project Settings > Input (Default Viewport Mouse Capture Mode).
- Gamepad: focus must be on a widget for navigation; set focus explicitly after opening.

## Stuck-state prevention
- Centralise: one UI manager owns the mode based on a stack of open screens; never call
  SetInputMode from random widgets.
- Restore on menu close *and* on menu destruction (level change while open).
- Also pause/unpause (`SetPause`) in the same place if the menu pauses.

## CommonUI alternative
With CommonUI, activatable widgets declare `GetDesiredInputConfig()` (Game, Menu, All) and the
action router applies input mode and cursor automatically as the stack changes — avoid mixing with
manual SetInputMode calls.

## Gotchas
- PIE: the first click focuses the viewport; test mouse lock in standalone too.
- `bShowMouseCursor` true with Game Only leaves a visible but useless cursor.
- Multiple local players: input mode is per PlayerController.

## Verify
- [ ] Open/close the menu 20 times with mouse and with gamepad: no stuck cursor or dead input.
- [ ] Level travel with menu open restores game mode on arrival.
