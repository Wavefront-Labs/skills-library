---
id: computing-software.game-programming.unreal-engine.umg-viewmodel-mvvm
name: umg-viewmodel-mvvm
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, umg, umg-mvvm, viewmodel, field-notify, mvvmviewmodelbase, data-binding, ui-architecture, game-programming]
level: advanced
status: draft
description: "Use Unreal's UMG Viewmodel (MVVM) plugin: UMVVMViewModelBase with FieldNotify properties, binding widgets in the View Bindings panel, creation types and when MVVM pays off."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-viewmodel-for-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/ModelViewViewModel/UMVVMViewModelBase"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UMG Viewmodel (MVVM)

**Goal:** UI that updates from data changes via declarative bindings, with gameplay code never
touching widgets directly. Plugin: **UMG Viewmodel** (`ModelViewViewModel`), UE 5.1+ (beta/
experimental status varies by version: check before shipping).

## Viewmodel in C++
```cpp
// Build.cs: "ModelViewViewModel", "FieldNotification"
#include "MVVMViewModelBase.h"

UCLASS(BlueprintType)
class UHealthViewModel : public UMVVMViewModelBase
{
    GENERATED_BODY()
    UPROPERTY(BlueprintReadWrite, FieldNotify, Setter, Getter, meta=(AllowPrivateAccess))
    float CurrentHealth = 0.f;
    UPROPERTY(BlueprintReadWrite, FieldNotify, Setter, Getter, meta=(AllowPrivateAccess))
    float MaxHealth = 100.f;
public:
    void SetCurrentHealth(float V)
    {
        if (UE_MVVM_SET_PROPERTY_VALUE(CurrentHealth, V))
            UE_MVVM_BROADCAST_FIELD_VALUE_CHANGED(GetHealthPercent);   // derived value
    }
    float GetCurrentHealth() const { return CurrentHealth; }
    void SetMaxHealth(float V) { if (UE_MVVM_SET_PROPERTY_VALUE(MaxHealth, V)) UE_MVVM_BROADCAST_FIELD_VALUE_CHANGED(GetHealthPercent); }
    float GetMaxHealth() const { return MaxHealth; }

    UFUNCTION(BlueprintPure, FieldNotify)
    float GetHealthPercent() const { return MaxHealth > 0 ? CurrentHealth / MaxHealth : 0; }
};
```
`UE_MVVM_SET_PROPERTY_VALUE` sets and broadcasts only when the value changed.

## Binding in the widget
In the Widget Blueprint: Window > Viewmodels > add `UHealthViewModel` with a **creation type**:
- *Create Instance* (widget owns a new one),
- *Manual* (code assigns it: `SetViewModel` on the widget's MVVM extension),
- *Global Viewmodel Collection* (shared, registered via `UMVVMGameSubsystem`),
- *Property Path* / *Resolver* (fetched from another object).
Then Window > View Bindings: bind `HealthBar.Percent` <- `HealthViewModel.GetHealthPercent`,
one-way to widget. Conversion functions handle formatting (float -> FText).

## Feeding it from gameplay
The model (e.g. health component) updates the viewmodel on change:
`HealthVM->SetCurrentHealth(NewHealth);` The widget updates through field notifications, no tick, no
bindings polling.

## When it pays off
- Many screens showing the same data, designers binding without code, testable UI logic.
- For a small HUD, plain event-driven setters are simpler. CommonUI and MVVM combine well (Lyra-style
  projects use both patterns).

## Verify
- [ ] Changing the viewmodel value updates the widget once (no per-frame binding cost in Insights).
- [ ] Derived fields (percent) update when either source changes.
- [ ] Widget works with a viewmodel assigned at runtime (Manual creation) and handles null.
