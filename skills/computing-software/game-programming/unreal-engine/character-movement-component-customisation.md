---
id: computing-software.game-programming.unreal-engine.character-movement-component-customisation
name: character-movement-component-customisation
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, gameplay-framework, charactermovementcomponent, cmc, custom-movement-mode, saved-move, network-prediction, root-motion-source, game-programming]
level: advanced
status: docs-checked
description: "Extend CharacterMovementComponent safely online: prediction and correction flow, MOVE_Custom, root motion sources and FSavedMove_Character with FCharacterNetworkMoveData."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-networked-movement-in-the-character-movement-component-for-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CharacterMovementComponent customisation

**Goal:** change how ACharacter moves without breaking client prediction and server correction.

## How prediction works (Networked Movement page)
- `UCharacterMovementComponent` is pre-attached to `ACharacter`; `TickComponent` calls `PerformMovement`, which applies
  external physics and root motion, then `StartNewPhysics` selects a `Phys*` function (`PhysWalking`, `PhysFalling`...).
  `MaxSimulationIterations` bounds the recursion.
- Autonomous proxy (owning client): `ReplicateMoveToServer` wraps `PerformMovement`, records an `FSavedMove_Character`
  into the `SavedMoves` queue, combines similar moves, and sends a `ServerMove` (unreliable RPC; lost moves are resubmitted
  by the buffer). Authority (server): `ServerMove_Implementation` replays the move via `MoveAutonomous`/`PerformMovement`
  from its own copy's location, using server timestamps for delta time. If positions match it ACKs (`ClientAckGoodMove`),
  otherwise sends `ClientAdjustPosition`; the client then replays its `SavedMoves`. Simulated proxies apply
  `ReplicatedMovement` (`FRepMovement`) and smooth with `SmoothClientPosition` per `NetworkSmoothingMode`.
- Correction tuning: `ClientErrorUpdateRateLimit` and `MAXPOSITIONERRORSQUARED` under `[/Script/Engine.GameNetworkManager]`
  in `BaseGame.ini` (override in project `DefaultGame.ini`).
- Page warning: manual `SetLocation`/`SetRotation` in a network game is not captured by this replication, so the server sees
  an error and corrects. Teleport on the server (SetLocation with `bTeleport` true, or the Teleport node).

## Custom movement modes
`MOVE_Custom` suspends all other movement physics. In Blueprint, UCharacterMovementComponent is not normally Blueprintable,
so implement custom movement in the Character through the `UpdateCustomMovement` event (called from `PhysCustom`), with the
Custom Movement Mode byte as sub-mode. `StartNewPhysics`, `PhysCustom` and the other physics functions are virtual for
C++ subclasses.

## Root motion for ability-style movement
Root motion overrides normal physics in any movement mode (gravity still applies to Z while falling). Anim montage root
motion is captured in `FSavedMove_Character`, but the server and owning client do not verify they play the same montage, so
trigger it correctly on all machines. For programmatic movement use an `FRootMotionSource` (page names `_MoveToForce`,
`_JumpForce`): `ApplyRootMotionSource` returns a handle, apply it on the autonomous proxy so it enters `SavedRootMotion`, and
call `RemoveRootMotionSource` with the handle when done. Gameplay Ability System tasks such as
`AbilityTask_ApplyRootMotionMoveToForce` are the page's example.

## Extending saved move data
- The page describes the packed-move system: extend `FSavedMove_Character`; extend `FCharacterNetworkMoveData` (override
  `ClientFillNetworkMoveData` and `Serialize`); extend `FCharacterNetworkMoveDataContainer` and register it with
  `SetNetworkMoveDataContainer` (typically a member constructed in the CMC constructor); likewise the response types
  `FCharacterMoveResponseData`, `FCharacterMoveResponseDataContainer` via `SetMoveResponseDataContainer`.
- Read custom data while processing or replaying a move with `GetCurrentMoveData`, cast to your subclass.
- Legacy API: define `SUPPORT_DEPRECATED_CHARACTER_MOVEMENT_RPCS` non-zero in build files and set console variable
  `p.NetUsePackedMovementRPCs` to 0. `CallServerMovePacked` replaces `CallServerMove`.

## Checked
Date: 2026-11-07. Read in full: the Networked Movement in the Character Movement Component page (all sections),
unversioned en-us, no engine version stated. The second source, the UCharacterMovementComponent API page, returns empty text
and was dropped.
Removed as not on the page: the settings table (`MaxWalkSpeed`, `GroundFriction`, `AirControl`, etc.), the compressed-flag
sprint example (`GetCompressedFlags`, `FLAG_Custom_0..3`, `UpdateFromCompressedFlags`), the subclass-via-`SetDefaultSubobjectClass`
snippet, `SafeMoveUpdatedComponent`/`SlideAlongSurface`, the "UE 4.26+" claim, `p.NetShowCorrections`, `Net PktLag`,
`showdebug charactermovement`, and the Verify checklist.
Method: documentation only; no commands were run.
