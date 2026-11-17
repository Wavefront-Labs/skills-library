---
id: computing-software.game-programming.unreal-engine.slate-widgets-in-cpp
name: slate-widgets-in-cpp
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, slate, slate-widgets, cpp, editor-ui, umg, game-programming]
level: practitioner
status: draft
description: "Write Slate widgets in C++: SNew/SAssignNew declarative syntax, SLATE_BEGIN_ARGS, attributes and TAttribute bindings, wrapping in a UWidget for UMG and editor tabs."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/slate-user-interface-programming-framework-for-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-slate-ui-architecture-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/slate-editor-window-quickstart-guide-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slate widgets in C++

**Goal:** custom widgets for editor tools or engine-level UI that UMG cannot express.

## A compound widget
```cpp
class SHealthBar : public SCompoundWidget {
public:
    SLATE_BEGIN_ARGS(SHealthBar) : _Percent(1.f) {}
        SLATE_ATTRIBUTE(float, Percent)
        SLATE_EVENT(FSimpleDelegate, OnClicked)
    SLATE_END_ARGS()
    void Construct(const FArguments& InArgs) {
        Percent = InArgs._Percent;
        ChildSlot[
            SNew(SVerticalBox)
            + SVerticalBox::Slot().AutoHeight()[ SNew(STextBlock).Text(this, &SHealthBar::GetLabel) ]
            + SVerticalBox::Slot().AutoHeight()[ SNew(SProgressBar).Percent(Percent) ]
            + SVerticalBox::Slot().AutoHeight()[ SNew(SButton).Text(INVTEXT("Heal")).OnClicked_Lambda(
                [Cb = InArgs._OnClicked]() { Cb.ExecuteIfBound(); return FReply::Handled(); }) ]
        ];
    }
private:
    TAttribute<float> Percent;
    FText GetLabel() const { return FText::AsPercent(Percent.Get()); }
};
```
- `SNew(T)` creates, `SAssignNew(Ptr, T)` also stores a `TSharedPtr`.
- `TAttribute` binds values to functions/lambdas evaluated each paint: live updates with no polling
  code, but bound attributes are re-evaluated every frame (cost).
- Return `FReply::Handled()` from input events to stop bubbling.

## Using in UMG
Wrap in a `UWidget` subclass: override `RebuildWidget()` to `SNew` the Slate widget, `SynchronizeProperties()`
to push UPROPERTY values, and `ReleaseSlateResources()` to reset the shared pointer.

## Editor tabs
Register a nomad tab in a module: `FGlobalTabmanager::Get()->RegisterNomadTabSpawner("MyTool",
FOnSpawnTab::CreateRaw(this, &FMyModule::SpawnTab))` returning `SNew(SDockTab)[ SNew(SMyToolWidget) ]`.
Widget Reflector (Tools > Debug > Widget Reflector) inspects any Slate hierarchy.

## Gotchas
- Slate widgets are not UObjects: holding UObject pointers needs `TWeakObjectPtr` or FGCObject.
- Invalidation: for SLeafWidget custom paint, call `Invalidate(EInvalidateWidgetReason::Paint)` when
  state changes if under an invalidation panel.
- Module needs `Slate`, `SlateCore` (and `UMG` for wrappers) dependencies.

## Verify
- [ ] Widget Reflector shows the expected hierarchy; no per-frame attribute functions doing heavy work.
