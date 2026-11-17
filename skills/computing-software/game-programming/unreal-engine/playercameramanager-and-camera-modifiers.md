---
id: computing-software.game-programming.unreal-engine.playercameramanager-and-camera-modifiers
name: playercameramanager-and-camera-modifiers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, playercameramanager, camera-modifiers, camera-shake, view-target, setviewtargetwithblend, game-programming]
level: practitioner
status: draft
description: "Control Unreal cameras through APlayerCameraManager: view targets and blends, UpdateViewTarget overrides, pitch limits, camera modifiers and camera shakes."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Camera/APlayerCameraManager", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Camera/UCameraModifier", "https://dev.epicgames.com/documentation/en-us/unreal-engine/camera-framework-essentials-for-games-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PlayerCameraManager and camera modifiers

**Pipeline each frame:** the PlayerController's `PlayerCameraManager` asks the **view target**
(usually the possessed pawn) for its view (`CalcCamera`, which uses an active `UCameraComponent`),
blends view targets, applies **camera modifiers** (including shakes), then post-process.

## Switch view targets
```cpp
PC->SetViewTargetWithBlend(CinematicCameraActor, 1.0f, VTBlend_Cubic);   // blend 1 s
PC->SetViewTargetWithBlend(PC->GetPawn(), 0.5f);                           // back to the pawn
```
`bAutoManageActiveCameraTarget` on the PC auto-switches to the possessed pawn; disable it if you
manage view targets manually.

## Custom manager
```cpp
UCLASS() class AMyCameraManager : public APlayerCameraManager {
    GENERATED_BODY()
    AMyCameraManager() { ViewPitchMin = -70.f; ViewPitchMax = 60.f; }   // clamps control rotation pitch
protected:
    virtual void UpdateViewTarget(FTViewTarget& OutVT, float DeltaTime) override {
        Super::UpdateViewTarget(OutVT, DeltaTime);
        OutVT.POV.FOV = FMath::FInterpTo(OutVT.POV.FOV, bAiming ? 60.f : 90.f, DeltaTime, 10.f);
    }
};
// in your PlayerController constructor:
PlayerCameraManagerClass = AMyCameraManager::StaticClass();
```

## Camera modifiers
```cpp
UCLASS() class UHitFovPunch : public UCameraModifier {
    GENERATED_BODY()
    virtual bool ModifyCamera(float DeltaTime, FMinimalViewInfo& InOutPOV) override {
        Super::ModifyCamera(DeltaTime, InOutPOV);
        InOutPOV.FOV += 5.f * Alpha;           // Alpha blends with AlphaInTime/AlphaOutTime
        return false;                          // true would stop later modifiers
    }
};
PC->PlayerCameraManager->AddNewCameraModifier(UHitFovPunch::StaticClass());
```
Priority orders modifiers; `DisableModifier`/`EnableModifier` toggle with blend.

## Shakes
`PC->ClientStartCameraShake(UMyShake::StaticClass(), Scale)` (local) or
`UGameplayStatics::PlayWorldCameraShake` (radius falloff, all nearby players). Shake classes derive
from `UCameraShakeBase` with a pattern (Perlin noise, wave oscillator, sequence).

## Gotchas
- Camera code runs on the owning client only; the server's view of a client camera is approximate
  (`GetPlayerViewPoint` on server uses replicated control rotation).
- Pitch clamping belongs in `ViewPitchMin/Max`, not in input code, or it fights the controller.
- Spring arm lag + modifiers can double-smooth; tune one place.

## Verify
- [ ] Blending to a cinematic camera and back has no snap.
- [ ] Shake and FOV punch stack and fade out; accessibility option scales shakes to zero.
