---
id: computing-software.game-programming.unreal-engine.latent-actions-and-async-blueprint-nodes
name: latent-actions-and-async-blueprint-nodes
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, blueprints, latent-action, ublueprintasyncactionbase, async-blueprint-node, game-programming]
level: practitioner
status: draft
description: "Write async Blueprint nodes in C++: UBlueprintAsyncActionBase with multiple output pins, FLatentActionManager latent functions, and their lifetime and cancellation rules."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Kismet/UBlueprintAsyncActionBase", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/Engine/FLatentActionManager"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Latent actions and async Blueprint nodes

**Goal:** expose long-running C++ work (HTTP calls, loading, waiting for conditions) as Blueprint
nodes with clock-icon or multi-exec outputs.

## Option 1: UBlueprintAsyncActionBase (preferred)
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FFetchDone, const FString&, Body);
UCLASS()
class UFetchProfile : public UBlueprintAsyncActionBase {
    GENERATED_BODY()
public:
    UPROPERTY(BlueprintAssignable) FFetchDone OnSuccess;
    UPROPERTY(BlueprintAssignable) FFetchDone OnFailure;
    UFUNCTION(BlueprintCallable, meta=(BlueprintInternalUseOnly="true", WorldContext="WorldContext"))
    static UFetchProfile* FetchProfile(UObject* WorldContext, FString UserId) {
        auto* A = NewObject<UFetchProfile>(); A->UserId = UserId;
        A->RegisterWithGameInstance(WorldContext);   // keeps it alive
        return A;
    }
    virtual void Activate() override { /* start request; on finish: */ }
private:
    void Finish(bool bOk, const FString& Body) {
        (bOk ? OnSuccess : OnFailure).Broadcast(Body);
        SetReadyToDestroy();                          // allow GC
    }
    FString UserId;
};
```
Each `BlueprintAssignable` delegate becomes an exec output pin with its params. The node also has an
immediate "then" pin.

## Option 2: latent function (FPendingLatentAction)
`UFUNCTION(BlueprintCallable, meta=(Latent, LatentInfo="LatentInfo", WorldContext="WorldContext"))`
with `FLatentActionInfo LatentInfo`; add a `FPendingLatentAction` subclass via
`World->GetLatentActionManager().AddNewAction(LatentInfo.CallbackTarget, LatentInfo.UUID, Action)`.
`UpdateOperation` is polled every frame; call `Response.FinishAndTriggerIf(bDone, ...)`. Good for
"wait until condition" nodes, single output only.

## Rules
- Async/latent nodes only work in event graphs, not in functions (functions must complete
  synchronously).
- Lifetime: without `RegisterWithGameInstance` (or an outer holding a reference) the action can be
  GC'd mid-flight.
- Calling the same latent node again while pending is ignored for the same UUID (standard `Delay`
  behaviour) — document this.

## Gotchas
- Broadcasting after the owning Blueprint actor died: bound delegate targets are weak; still guard
  your own captured pointers.
- HTTP callbacks arrive on the game thread for `FHttpModule` requests; other async APIs may not —
  marshal with `AsyncTask(ENamedThreads::GameThread, ...)`.

## Verify
- [ ] Node shows success/failure pins and fires exactly once.
- [ ] Force GC (`obj gc`) during a pending request; it still completes.
