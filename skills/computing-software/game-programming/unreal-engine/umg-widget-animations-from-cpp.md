---
id: computing-software.game-programming.unreal-engine.umg-widget-animations-from-cpp
name: umg-widget-animations-from-cpp
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, widget-animation, umg, cpp, ui-animation, game-programming]
level: practitioner
status: draft
description: "Play UMG widget animations from C++: BindWidgetAnim, PlayAnimation options, finished events, reverse and looping, and avoiding animation costs on hidden widgets."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/animating-umg-widgets-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/UMG/Blueprint/UUserWidget/PlayAnimation/", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/UMG/Animation/UWidgetAnimation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Widget animations from C++

**Goal:** UI animations authored in the UMG designer, triggered and chained from C++.

## Bind
Author animations in the widget Blueprint's Animations panel (`FadeIn`, `Pulse`). In the C++ parent:
```cpp
UPROPERTY(Transient, meta = (BindWidgetAnim)) TObjectPtr<UWidgetAnimation> FadeIn;
UPROPERTY(Transient, meta = (BindWidgetAnimOptional)) TObjectPtr<UWidgetAnimation> Pulse;
```
Names must match; `Transient` is required. Missing required bindings fail Blueprint compile.

## Play
```cpp
PlayAnimation(FadeIn);                                         // forward once
PlayAnimation(Pulse, 0.f, /*NumLoops*/0);                      // 0 = loop forever
PlayAnimationReverse(FadeIn);
PlayAnimation(FadeIn, 0.f, 1, EUMGSequencePlayMode::Forward, /*Speed*/2.f);
StopAnimation(Pulse);
bool bPlaying = IsAnimationPlaying(FadeIn);
```

## Finished events
```cpp
FWidgetAnimationDynamicEvent OnDone;
OnDone.BindDynamic(this, &UMyMenu::HandleFadeInFinished);   // UFUNCTION
BindToAnimationFinished(FadeIn, OnDone);
```
Or override `OnAnimationFinished_Implementation(const UWidgetAnimation*)`. Use for "fade out then
RemoveFromParent".

## Performance
- Animations tick on the game thread through the widget's Sequencer player. Stop looping animations
  when widgets are collapsed; collapsed widgets with looping animations still evaluate.
- Animating layout properties (size, padding) invalidates layout; animate render transform and opacity
  instead. Works with Invalidation Boxes (render transform is volatile-friendly).
- Many simultaneous animated list entries: prefer material-driven animation (time parameter).

## Gotchas
- Calling PlayAnimation in `NativeConstruct` before the widget is added can be skipped; trigger after
  AddToViewport or from `NativeOnActivated` (CommonUI).
- Restarting an animation already playing restarts from start time; use `PlayAnimationTimeRange` or
  check state first.

## Verify
- [ ] Animations play correctly at different speeds; no looping animation runs on hidden widgets.
