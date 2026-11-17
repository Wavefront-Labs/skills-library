---
id: computing-software.game-programming.unreal-engine.ahud-canvas-debug-drawing
name: ahud-canvas-debug-drawing
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, ahud, canvas, drawhud, debug-drawing, showdebug, gameplay-framework, game-programming]
level: practitioner
status: draft
description: "Use Unreal's AHUD for canvas drawing: DrawHUD overrides, text/rect/texture drawing, projecting world points, ShowDebug hooks, and when to use UMG instead."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/GameFramework/AHUD", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/UCanvas", "https://dev.epicgames.com/documentation/en-us/unreal-engine/hud-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AHUD and canvas debug drawing

**Goal:** draw immediate-mode overlays (debug info, crosshairs, nameplates for testing) per local player.

- One `AHUD` per `APlayerController`, spawned from the GameMode's `HUDClass`; only on clients/local
  players (never on a dedicated server). Get it with `PC->GetHUD<AMyHUD>()`.
- Production UI belongs in UMG; AHUD is ideal for debug overlays and owning/creating widgets.

```cpp
void AMyHUD::DrawHUD() {
    Super::DrawHUD();                                   // keeps ShowDebug and hitbox drawing working
    if (!Canvas) return;
    const FVector2D C(Canvas->ClipX * 0.5f, Canvas->ClipY * 0.5f);
    DrawRect(FLinearColor::White, C.X - 2, C.Y - 2, 4, 4);                  // crosshair dot
    DrawText(FString::Printf(TEXT("FPS %.0f"), 1.f / GetWorld()->GetDeltaSeconds()),
             FLinearColor::Green, 20, 20, nullptr, 1.2f);
    for (AActor* E : TrackedEnemies) {
        const FVector S = Project(E->GetActorLocation() + FVector(0, 0, 100), true);
        if (S.Z > 0) DrawText(E->GetName(), FLinearColor::Red, S.X, S.Y);  // Z<=0: behind camera
    }
}
```
Other draws: `DrawLine`, `DrawTexture`, `DrawMaterial`, `DrawTextureSimple`; `GetTextSize` for layout.
`Canvas->ClipX/ClipY` are the viewport size in pixels (split-screen aware).

## ShowDebug integration
`showdebug <Category>` (console) calls `DisplayDebug` on the view target and its components.
Override `AActor::DisplayDebug(UCanvas*, const FDebugDisplayInfo&, float& YL, float& YPos)` and check
`DebugDisplay.IsDisplayOn(TEXT("MyCategory"))` to add your own page. `showdebug` alone toggles.

## Hit boxes
`AddHitBox(Pos, Size, Name, bConsumesInput)` + override `NotifyHitBoxClick` for clickable debug UI
(requires the PC to enable click events).

## Gotchas
- Draw calls only valid inside `DrawHUD` (Canvas is null elsewhere).
- Text scale does not follow DPI; multiply by `GetDefault<UUserInterfaceSettings>()->GetDPIScaleBasedOnSize(...)` if needed.
- Wrap debug-only drawing in `#if !UE_BUILD_SHIPPING`.
- `Project` returns screen space for this HUD's viewport; for UMG positions use
  `UGameplayStatics::ProjectWorldToScreen` + viewport scale.

## Verify
- [ ] Split-screen: each player's HUD draws in its own viewport.
- [ ] `showdebug MyCategory` shows the custom page; Shipping build has no debug text.
