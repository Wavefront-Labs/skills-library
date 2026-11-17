---
id: computing-software.game-programming.unreal-engine.gameplay-debugger-for-ai
name: gameplay-debugger-for-ai
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, gameplay-debugger, ai-debugging, behavior-trees, eqs, game-programming]
level: practitioner
status: draft
description: "Debug Unreal AI live with the Gameplay Debugger: categories for BT, EQS, perception, navmesh, selecting actors, in builds, and custom categories in C++."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-gameplay-debugger-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/create-custom-gameplay-debugger-categories-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/GameplayDebugger/FGameplayDebuggerCategory/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gameplay Debugger for AI

**Goal:** see what an AI thinks (its BT branch, perception, EQS scores, path) while the game runs.

## Use it
- Press **apostrophe ( ' )** in PIE or a development build (`EnableGDT` console command); remap in
  Project Settings > Gameplay Debugger.
- Look at an AI pawn to select it (or use `gdt.Select`/cycle with numpad).
- Numpad keys toggle categories: 0 Navmesh, 1 AI (controller, pawn, current path), 2 Behavior Tree
  (active branch, blackboard values), 3 EQS (query items and scores drawn in world), 4 Perception
  (sight cones, stimuli), plus Abilities (GAS), Mass, and project categories.
- Tab toggles spectator free camera while keeping the selection.
- Works in multiplayer: data is replicated from the server for the selected actor.

## Custom category
```cpp
class FGameplayDebuggerCategory_Squad : public FGameplayDebuggerCategory {
public:
    static TSharedRef<FGameplayDebuggerCategory> MakeInstance() { return MakeShareable(new FGameplayDebuggerCategory_Squad()); }
    void CollectData(APlayerController* OwnerPC, AActor* DebugActor) override {
        if (const ASquadAI* S = Cast<ASquadAI>(DebugActor)) { Role = S->GetRoleName(); }
    }
    void DrawData(APlayerController* OwnerPC, FGameplayDebuggerCanvasContext& Ctx) override {
        Ctx.Printf(TEXT("Squad role: {yellow}%s"), *Role);
    }
    FString Role;
};
// in module StartupModule (WITH_GAMEPLAY_DEBUGGER)
IGameplayDebugger& GD = IGameplayDebugger::Get();
GD.RegisterCategory("Squad", IGameplayDebugger::FOnGetCategory::CreateStatic(&FGameplayDebuggerCategory_Squad::MakeInstance),
    EGameplayDebuggerCategoryState::EnabledInGameAndSimulate, 6);
GD.NotifyCategoriesChanged();
```
Replicate collected data with `SetDataPackReplication` for networked debugging. Module needs the
`GameplayDebugger` dependency, guarded by `WITH_GAMEPLAY_DEBUGGER`.

## Related tools
Visual Logger (Tools > Debug > Visual Logger, `vislog`) records AI history over time for later
scrubbing; use it for bugs that happen once.

## Verify
- [ ] Bug reports for AI include a Gameplay Debugger screenshot or a Visual Logger recording.
