---
id: computing-software.game-programming.unreal-engine.enhanced-input-actions-and-mapping-contexts
name: enhanced-input-actions-and-mapping-contexts
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, enhanced-input, input-mapping-context, input-action, value-types, context-priority, game-programming]
level: practitioner
status: docs-checked
description: "Set up Enhanced Input: Input Action value types, trigger states, Input Mapping Contexts with priorities via the local player subsystem, WASD modifiers and debug commands."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced Input actions and mapping contexts

**Goal:** input defined as data, with context switching (walk, sprint, vehicle) by swapping mapping contexts.

## Assets (Enhanced Input page)
- Enhanced Input is enabled by default. Create assets in the Content Browser with Add(+) > Input.
- **Input Action**: a data asset, the link between the input system and your code; one per thing the user can do ("Crouch",
  "Fire Weapon"). Value type sets the value: bool (on/off), Axis1D (float), Axis2D (`FVector2D`, e.g. thumbstick), Axis3D
  (`FVector`, e.g. motion controller).
- **Trigger states** you can bind to in C++ or Blueprint: Started, Ongoing, Triggered, Completed, Canceled. "Triggered" is
  the one most often used.
- **Input Mapping Context**: hierarchy of Input Actions, then the keys/buttons/axes that can drive each, then the Triggers
  and Modifiers for each input. Create via Content Browser right-click > Input > Input Mapping Context.

## Bind and add contexts in C++ (page samples)
```cpp
void AFooBar::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    UEnhancedInputComponent* Input = Cast<UEnhancedInputComponent>(PlayerInputComponent);
    Input->BindAction(AimingInputAction, ETriggerEvent::Triggered, this, &AFooBar::SomeCallbackFunc);
}
// callback takes const FInputActionInstance& Instance; Instance.GetValue().Get<float>() (or bool, FVector2D, FVector)

// UPROPERTY(EditAnywhere, Category="Input") TSoftObjectPtr<UInputMappingContext> InputMapping;
if (ULocalPlayer* LocalPlayer = Cast<ULocalPlayer>(Player))
{
    if (UEnhancedInputLocalPlayerSubsystem* InputSystem = LocalPlayer->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
    {
        if (!InputMapping.IsNull())
        {
            InputSystem->AddMappingContext(InputMapping.LoadSynchronous(), Priority);
        }
    }
}
```
- Contexts are applied per local player through the Enhanced Input Local Player Subsystem and can be added, removed and
  prioritised dynamically. The page's example is a vehicle context added on entering and removed on exiting.
- Priority: if several contexts map the same Input Action, the context with the highest priority is considered and the
  others are ignored.
- Mutually exclusive contexts per mode (common actions in one context, one per travel mode) avoid input collisions.
- The page's sample does not show removal or any other `Subsystem` calls; check the API before using them.

## WASD into one Axis2D action (page table)
Each key reports 0 or 1 on the X axis. W/Up: Swizzle Input Axis Values (YXZ or ZXY). A/Left: Negate. S/Down: Negate then
Swizzle (YXZ or ZXY). D/Right: no modifier.

## Debug
`showdebug enhancedinput` displays the available input action and axis mappings; `showdebug devices` is also listed.

## Checked
Date: 2026-11-07. Read in full: the Enhanced Input page (all sections), unversioned en-us page; the code samples are the
page's own and one lacks the surrounding function. The second source (UInputMappingContext API page) returned no text and
was dropped.
Removed as not on the page: Action flags `Consume Input` and `Trigger when paused`, Project Settings default input class
names and the "UE 5.1+" default claim, `FModifyContextOptions`, `ClearAllMappings`, `RemoveMappingContext`, the
controller `BeginPlay`/`PawnClientRestart`/`OnPossess` guidance, Input Mode UI Only note, duplicate-add behaviour, the
Developer Settings "Enable default mapping contexts" item, the claim that a higher-priority context hides keys from lower
ones when consumed (the page says the others are "ignored" for the same Input Action only), and the Verify checklist.
Method: documentation only; no commands were run.
