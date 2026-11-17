---
id: computing-software.game-programming.unreal-engine.aicontroller-moveto-and-path-following
name: aicontroller-moveto-and-path-following
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ai-moveto, aicontroller, path-following, navigation, game-programming]
level: practitioner
status: draft
description: "Move Unreal AI with AAIController MoveToActor/MoveToLocation and FAIMoveRequest: acceptance radius, filters, partial paths, OnMoveCompleted results and debugging."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/navigation-system-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/AIModule/AAIController/MoveToLocation/", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/AIModule/Navigation/UPathFollowingComponent/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AIController MoveTo and path following

**Goal:** AI pawns move to targets reliably and code knows whether they arrived.

## Calls
```cpp
EPathFollowingRequestResult::Type R = AIController->MoveToActor(Target, /*AcceptanceRadius*/50.f,
    /*bStopOnOverlap*/true, /*bUsePathfinding*/true, /*bCanStrafe*/false, /*FilterClass*/nullptr,
    /*bAllowPartialPath*/true);

FAIMoveRequest Req(TargetLocation);
Req.SetAcceptanceRadius(30.f);
Req.SetNavigationFilter(UNavFilter_AvoidWater::StaticClass());
Req.SetAllowPartialPath(false);
FNavPathSharedPtr Path;
FPathFollowingRequestResult Res = AIController->MoveTo(Req, &Path);
```
`MoveToActor` keeps updating the goal as the actor moves; `MoveToLocation` is a fixed point.
Result: `Failed`, `AlreadyAtGoal`, `RequestSuccessful`.

## Completion
```cpp
void AMyAIController::OnMoveCompleted(FAIRequestID RequestID, const FPathFollowingResult& Result) {
    Super::OnMoveCompleted(RequestID, Result);
    if (Result.IsSuccess()) {...} else if (Result.Code == EPathFollowingResult::Blocked) {...}
}
```
Codes: Success, Blocked, OffPath, Aborted, Invalid. Or bind `ReceiveMoveCompleted` (Blueprint) /
`GetPathFollowingComponent()->OnRequestFinished`.

## Blueprint and BT
`AI MoveTo` (async node with On Success/On Fail) and BT `Move To` task wrap the same request. BT
Move To has Observe Blackboard Value to repath when the key changes.

## Movement requirements
- Pawn needs a movement component supporting nav (CharacterMovement with `bUseControllerDesiredRotation`
  or Orient Rotation To Movement for facing).
- NavMesh covering start and goal (show with `P` in editor / `show Navigation`).
- Nav agent properties (radius/height) matching a supported agent.

## Debugging
- Gameplay Debugger (apostrophe key) Navmesh and Path categories show current path and status.
- `log LogPathFollowing Verbose`, `log LogNavigation Verbose`.
- Failed with no path: goal off navmesh. Use `ProjectPointToNavigation` before moving.

## Gotchas
- Acceptance radius counts from agent and goal collision when stop-on-overlap is true; tiny radii
  may never succeed for big agents.
- New MoveTo aborts the previous request (OnMoveCompleted with Aborted fires); do not treat as failure.
- Crowd avoidance: use `ADetourCrowdAIController` or RVO on CharacterMovement.

## Verify
- [ ] Gameplay Debugger shows path status for each AI; failures log a reason code.
