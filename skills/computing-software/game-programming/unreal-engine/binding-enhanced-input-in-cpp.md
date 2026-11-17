---
id: computing-software.game-programming.unreal-engine.binding-enhanced-input-in-cpp
name: binding-enhanced-input-in-cpp
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, cpp, enhanced-input, enhancedinputcomponent, bindaction, setupplayerinputcomponent, game-programming]
level: practitioner
status: docs-checked
description: "Bind Enhanced Input actions in C++: UEnhancedInputComponent::BindAction and ETriggerEvent, FInputActionValue handlers, adding mapping contexts via the local player subsystem."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/EnhancedInput/UEnhancedInputComponent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binding Enhanced Input in C++

**Goal:** bind designer-editable Input Action assets to C++ handlers and activate Input Mapping Contexts.

## Concepts (Enhanced Input page)
- Enhanced Input is enabled by default in UE5. Four concepts: Input Actions, Input Mapping Contexts, Input Modifiers,
  Input Triggers.
- An Input Action's value type decides the C++ type: boolean is `bool`, Axis1D is `float`, Axis2D is `FVector2D`,
  Axis3D is `FVector`.
- Trigger states (`ETriggerEvent`): Started, Ongoing, Triggered, Completed, Canceled. "Often, you will use the
  Triggered state."

## Binding (page's snippet, abridged)
```cpp
void AFooBar::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    UEnhancedInputComponent* Input = Cast<UEnhancedInputComponent>(PlayerInputComponent);
    Input->BindAction(AimingInputAction, ETriggerEvent::Triggered, this, &AFooBar::SomeCallbackFunc);
}
void AFooBar::SomeCallbackFunc(const FInputActionInstance& Instance)
{
    bool BoolValue = Instance.GetValue().Get<bool>();   // also Get<float>(), Get<FVector2D>(), Get<FVector>()
}
```
The API page lists `BindAction` overloads taking `const UInputAction*`, `ETriggerEvent`, an object and either an
`FName` UFUNCTION name or a method pointer whose signature is one of the plain, value
(`FEnhancedInputActionHandlerValueSignature`) or instance (`FEnhancedInputActionHandlerInstanceSignature`) forms, and
each returns `FEnhancedInputActionEventBinding&`. Other documented members: `BindActionValue(Action)` with
`GetBoundActionValue(Action)`, `BindActionValueLambda`, `BindActionInstanceLambda`, `RemoveBindingByHandle(uint32)`
("Binding handles are unique across all bindings"), `RemoveActionEventBinding(int32)`, `ClearActionEventBindings()`,
`ClearBindingsForObject(UObject*)`.

## Mapping contexts
Add and remove Input Mapping Contexts at runtime per local player. Page snippet: get
`UEnhancedInputLocalPlayerSubsystem` from the `ULocalPlayer`, then
`InputSystem->AddMappingContext(InputMapping.LoadSynchronous(), Priority)` with the context held as a
`TSoftObjectPtr<UInputMappingContext>`. If several contexts map the same Input Action, the highest-priority context
wins and the others are ignored.

## Input component behaviour (API page)
`UEnhancedInputComponent` is a transient component derived from `UInputComponent`; input components are processed
from a stack managed by the PlayerController and processed by the PlayerInput. Bindings do not consume input events;
the page says that can be replicated with `UInputMappingContext::Priority`.

## Checked
Date: 2026-11-07. Read in full: the Enhanced Input page (all sections, code blocks included) and the
`UEnhancedInputComponent` API page (member tables, class description). Unversioned pages that state no engine version.
Removed as not on either page: `Build.cs` module line, `CastChecked`, the Move/Look/Jump example with
`AddMovementInput` and `PawnClientRestart`, "Pawn vs controller" binding guidance, the legacy-component crash gotcha,
the "5.x" lambda note, null-action error behaviour, and the Verify checklist.
Method: documentation only; no commands were run.
