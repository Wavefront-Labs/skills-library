---
id: computing-software.game-programming.unreal-engine.umg-cpp-widgets-with-bindwidget
name: umg-cpp-widgets-with-bindwidget
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, umg, uuserwidget, bindwidget, bindwidgetoptional, bindwidgetanim, nativeconstruct, createwidget, widget-blueprint, game-programming]
level: practitioner
status: draft
description: "Write UMG widget logic in C++ while designers lay out in the Widget Blueprint: UUserWidget subclass, meta=(BindWidget), animations, NativeConstruct and event-driven updates."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-ui-designer-for-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/UMG/Blueprint/UUserWidget"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UMG C++ widgets with BindWidget

**Goal:** UI logic in C++ (testable, reviewable, fast), visual layout in the Widget Blueprint
designer, with compile-time checks that required widgets exist.

## C++ base
```cpp
// Build.cs: PrivateDependencyModuleNames += { "UMG", "Slate", "SlateCore" }
#include "Blueprint/UserWidget.h"
#include "Components/TextBlock.h"
#include "Components/ProgressBar.h"
#include "Components/Button.h"

UCLASS(Abstract)
class UHealthHUD : public UUserWidget
{
    GENERATED_BODY()
protected:
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UProgressBar> HealthBar;     // must exist in the WBP
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UTextBlock> HealthText;
    UPROPERTY(meta=(BindWidgetOptional)) TObjectPtr<UButton> MenuButton; // may be absent
    UPROPERTY(Transient, meta=(BindWidgetAnim)) TObjectPtr<UWidgetAnimation> DamageFlash;

    virtual void NativeConstruct() override
    {
        Super::NativeConstruct();
        if (MenuButton) MenuButton->OnClicked.AddDynamic(this, &UHealthHUD::OnMenuClicked);
    }
public:
    void SetHealth(float Current, float Max)
    {
        HealthBar->SetPercent(Max > 0 ? Current / Max : 0);
        HealthText->SetText(FText::AsNumber(FMath::RoundToInt(Current)));
        PlayAnimation(DamageFlash);
    }
private:
    UFUNCTION() void OnMenuClicked();
};
```
Create a Widget Blueprint, reparent to `UHealthHUD` (Graph > Class Settings > Parent Class). The
designer must add widgets with **exactly** the names `HealthBar`, `HealthText` (with "Is Variable"
checked); missing BindWidget members are compile errors in the WBP, a clear contract between code
and layout.

## Creating and showing
```cpp
UPROPERTY(EditDefaultsOnly) TSubclassOf<UHealthHUD> HUDClass;   // set to the WBP in a Blueprint/config
...
HUD = CreateWidget<UHealthHUD>(PlayerController, HUDClass);
HUD->AddToViewport(/*ZOrder*/ 0);
```
Own the widget from the PlayerController or HUD class (UPROPERTY so it is not GC'd).

## Event-driven, not bound
Avoid UMG **property bindings** (the Bind dropdown on text/percent): they evaluate every frame.
Push updates from gameplay events (health changed delegate -> `SetHealth`). In CommonUI/MVVM
setups, field notifications serve the same role.

## Input and focus
`SetInputMode(FInputModeUIOnly / GameAndUI)` and `bShowMouseCursor` on the PlayerController when
opening menus; restore on close. `SetIsFocusable(true)` + `SetKeyboardFocus()` for gamepad navigation.

## Verify
- [ ] Removing `HealthText` from the WBP produces a compile error naming it.
- [ ] No property bindings in the WBP (Widget Reflector/Insights show no per-frame binding cost).
- [ ] Widget survives GC (stable after `obj gc`).
