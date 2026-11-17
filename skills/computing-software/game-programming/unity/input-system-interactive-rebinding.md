---
id: computing-software.game-programming.unity.input-system-interactive-rebinding
name: input-system-interactive-rebinding
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-input-system, unity-interactive-rebinding, performinteractiverebinding, binding-overrides, key-rebinding, game-programming]
level: practitioner
status: docs-checked
description: "Implement in-game control rebinding with PerformInteractiveRebinding, its defaults, disposing the operation, and saving and restoring binding overrides as JSON."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/ActionBindings.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/api/UnityEngine.InputSystem.InputActionRebindingExtensions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input System interactive rebinding

**Goal:** a "press a control" rebinding screen whose result persists across restarts. Package version 1.11 docs.

## The rebind operation
Call `PerformInteractiveRebinding()` on an `InputAction`. The operation waits for input from any Device matching the
action's expected Control type, then assigns that Control's path through `InputBinding.overridePath`. If several Controls
are actuated it picks the one with the highest magnitude.

```csharp
void RemapButtonClicked(InputAction actionToRebind)
{
    var rebindOperation = actionToRebind.PerformInteractiveRebinding()
        .WithControlsExcluding("Mouse")   // avoid accidental input from mouse motion
        .OnMatchWaitForAnother(0.1f)
        .Start();
}
```
- **Dispose** every `RebindingOperation` with `Dispose()` (for example inside `OnComplete`), or it leaks unmanaged memory.
- Configurable: `WithExpectedControlType`, `WithControlsExcluding`, `WithCancelingThrough`, and for actions with several
  bindings `WithTargetBinding`, `WithBindingGroup`, `WithBindingMask`.
- `PerformInteractiveRebinding(int bindingIndex = -1)` targets one binding; the index must not be a composite binding
  (ArgumentOutOfRangeException if not a valid index). Find an index with
  `action.GetBindingIndex(InputBinding.MaskByGroup("Gamepad"))`.
- Defaults applied automatically: `WithAction`, a 0.05 s `OnMatchWaitForAnother`, pointer and touch position/delta
  excluded, matching events suppressed so they are not picked up elsewhere, and (unless the rebind looks for a button)
  the Escape key cancels via `WithCancelingThrough`.

```csharp
var bindingIndex = myAction.GetBindingIndex(InputBinding.MaskByGroup("Gamepad"));
var rebind = myAction.PerformInteractiveRebinding(bindingIndex);
rebind.OnComplete(operation =>
{
    Debug.Log($"Rebound '{myAction}' to '{operation.selectedControl}'");
    operation.Dispose();
});
rebind.Start();
```

## Persist and restore
```csharp
var rebinds = playerInput.actions.SaveBindingOverridesAsJson();
PlayerPrefs.SetString("rebinds", rebinds);

var rebinds = PlayerPrefs.GetString("rebinds");
playerInput.actions.LoadBindingOverridesFromJson(rebinds);
```
- Override values are not saved with the actions (for example by `InputActionAsset.ToJson()`).
- `LoadBindingOverridesFromJson` removes all existing overrides first; pass `false` as the second argument
  (`removeExisting`) to keep them.
- Restore defaults: `playerInput.actions["fire"].RemoveBindingOverride(0)`, `...["fire"].RemoveAllBindingOverrides()`, or
  `playerInput.actions.RemoveAllBindingOverrides()`.
- An empty-string `overridePath` effectively disables the binding.

## Labels
`InputBinding.effectivePath` is `overridePath` if set, otherwise `path`. `action.GetBindingDisplayString()` returns text for
the action as a whole, `action.GetBindingDisplayString(1)` for a binding index. The package sample "Rebinding UI"
(Package Manager) shows a full setup; the API page names a "Tanks Demo" sample as another example.

## Checked
Date: 2026-11-07.
Read: Input System 1.11 ActionBindings page (Interactive rebinding, Saving and loading rebinds, Restoring original
Bindings, Displaying Bindings, plus the override-property table) and, from the InputActionRebindingExtensions API page, the
class remarks and example, the `PerformInteractiveRebinding` entry with its remarks and example, and the
`LoadBindingOverridesFromJson` entries. The rest of that 62K-character API page (each `With...` method and
`RebindingOperation` member entry) was not read in full.
Removed as unconfirmed: the "action must be disabled while rebinding" requirement, the cancel-then-restart duplicate
check and swap policy, the `WithBindingGroup("Keyboard&Mouse")` usage, `OnCancel` wiring, composite handling
(`index + 1`, `isPartOfComposite` loop), "load before enabling / PlayerInput copies the asset" advice, the keyboard
physical-layout gotcha, the `deviceLayout`/`controlPath` icon mapping for this skill, and the invented Verify checklist.
Method: documentation only; no commands were run.
