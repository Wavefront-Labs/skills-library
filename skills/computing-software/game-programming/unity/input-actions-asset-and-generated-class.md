---
id: computing-software.game-programming.unity.input-actions-asset-and-generated-class
name: input-actions-asset-and-generated-class
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-input-system, input-actions-asset, input-action-map, generated-csharp-class, csharp, game-programming]
level: practitioner
status: docs-checked
description: "Create an .inputactions asset, generate its C# wrapper class, enable actions and action maps, and know what the Input System does with project-wide actions (package 1.11)."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/ActionAssets.html", "https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Actions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input Actions asset and generated C# class

**Goal:** define actions once in an `.inputactions` asset and have gameplay code use a typed wrapper instead of reading
devices directly.

## The asset
An Input Action Asset holds Input Action definitions with their Bindings and Control Schemes. It has the `.inputactions`
extension and is stored as plain JSON. For most projects one asset is enough; the page says it is usually simpler to
configure the project-wide action definition in Project Settings.
- Create: right-click in the Project window, or Assets > Create > Input Actions.
- Edit: double-click the asset, or use the Edit Asset button in its Inspector. You can have several editor windows open,
  but not two for the same asset. The editor matches the one in Project Settings.
- Runtime edits made in Play mode do not persist in the asset after you exit Play mode.

## Generate the C# class
Tick **Generate C# Class** in the importer properties in the asset's Inspector, then Apply. You can choose a path, class
name and namespace or keep the defaults. To regenerate the `.cs` file, right-click the asset and choose Reimport. The
"Generate Interfaces" checkbox produces an interface per action map (the page's example calls the map "gameplay" and gets
`IGameplayActions`).

```csharp
public class MyPlayerScript : MonoBehaviour, IGameplayActions
{
    MyPlayerControls controls;

    public void OnEnable()
    {
        if (controls == null)
        {
            controls = new MyPlayerControls();
            controls.gameplay.SetCallbacks(this);
        }
        controls.gameplay.Enable();
    }

    public void OnDisable() { controls.gameplay.Disable(); }

    public void OnUse(InputAction.CallbackContext context) { /* 'Use' code here. */ }
    public void OnMove(InputAction.CallbackContext context) { /* 'Move' code here. */ }
}
```
(Names `MyPlayerControls`, `gameplay`, `OnUse`, `OnMove` come from the page's example asset.)

## Enabling actions
- Actions in the asset assigned as project-wide are enabled by default.
- Actions elsewhere (another asset, actions created in code, serialized `InputAction` fields in a MonoBehaviour) start
  disabled and must be enabled with `Enable()` on the action or on its action map.
- You cannot change certain configuration, such as bindings, while an action is enabled; call `Disable`.
- While enabled, an action monitors its bound controls during the Input System update, once per frame, once per fixed
  update, or manually, depending on the update mode in the input settings.

## Other API facts (Actions page)
- Scripting API: `InputSystem.actions` (the project-wide actions), `InputActionMap`, `InputAction`, `InputBinding`.
- Action names must be unique within their action map; map names must be unique too. Each also has a stable ID
  (`InputAction.id`, `InputActionMap.id`) that survives renames.
- Order in the editor is visual only; if several actions fire in one frame their reported order is undefined.
- Actions are a runtime-only feature: not usable in Editor window code.
- Other creation routes: serialized `InputAction` fields on a MonoBehaviour, `InputActionMap.FromJson` /
  `InputActionAsset.FromJson`, or building actions in code (`new InputAction("look", binding: "<Gamepad>/leftStick")`,
  `AddBinding`, `AddCompositeBinding("Dpad").With("Up", "<Keyboard>/w")`).
- The Player Input component can take an Action Asset and handle activating action maps and selecting control schemes.
- `DefaultInputActions` (asset `DefaultInputActions.inputactions`) is a legacy asset kept for compatibility, separate from
  the project-wide actions.

## Checked
Date: 2026-11-07.
Read in full: Input System 1.11 "Input Action Assets" and "Actions" manual pages including every code block. The
"Using Input Action Assets" heading on the first page has no body text in the fetched page.
Removed as unconfirmed by those pages: action types (Value/Button/Pass-Through), control types, composite names such as
"2D Vector", control scheme details, `IInputActionCollection2`/`IDisposable` and `Dispose` advice, callback phases
and the `ctx.performed` double-fire claim, polling vs events advice, `WasPressedThisFrame` in `FixedUpdate`,
`InputSystem.actions.FindAction`, Active Input Handling, Unity 6 project-wide asset menu path, and the invented Verify
checklist. The Actions Workflow, Action Bindings and binding-resolution pages were not opened.
Method: documentation only; no commands were run.
