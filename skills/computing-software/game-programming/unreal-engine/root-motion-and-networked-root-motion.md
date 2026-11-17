---
id: computing-software.game-programming.unreal-engine.root-motion-and-networked-root-motion
name: root-motion-and-networked-root-motion
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue-root-motion, root-motion, character-movement, montages, networking, game-programming]
level: practitioner
status: draft
description: "Use Unreal root motion: enabling it per sequence, Root Motion Mode on the Anim BP, montage-only networked root motion, and Root Motion Sources for procedural moves."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/root-motion-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-networked-movement-in-the-character-movement-component-for-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/Engine/GameFramework/FRootMotionSource/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root motion and networked root motion

**Goal:** animation-driven movement for attacks, dodges and vaults that works in multiplayer.

## Enable
1. Animation Sequence > Asset Details > **Enable Root Motion**; Root Motion Root Lock (Ref Pose,
   Anim First Frame, Zero). Force Root Lock for in-place clips.
2. Anim Blueprint Class Defaults > **Root Motion Mode**:
   - `Root Motion from Montages Only` (default): supported by Character Movement networking.
   - `Root Motion from Everything`: any blended pose contributes; fine for single player/AI, not
     replicated well for players.
   - `Ignore Root Motion`, `No Root Motion Extraction`.

## Character Movement integration
CMC consumes extracted root motion as velocity during the movement tick. In Walking mode Z is
ignored unless you switch to Flying mode (vaults, climbs) or use Root Motion Sources. Gravity and
collision still apply.

## Networked root motion (montages)
- The autonomous client plays the montage locally; CMC saves root motion in saved moves and the server
  replays the same montage position, so corrections are rare.
- Start montages through a predicted path (GAS `PlayMontageAndWait` with prediction) or a server RPC
  plus local play; both sides must play the same montage at the same time.
- Simulated proxies receive `RepRootMotion` (montage, position, location) and follow.

## Root Motion Sources
For procedural motion without animation (dashes, knockbacks, jump-to-location):
`FRootMotionSource_ConstantForce`, `_MoveToForce`, `_JumpForce`, `_RadialForce`. Applied via
`CharacterMovement->ApplyRootMotionSource(Source)` or GAS ability tasks
(`ApplyRootMotionConstantForce`); they are predicted and replicated by CMC.

## Gotchas
- Root bone must be the actual motion carrier; DCC exports with motion on the pelvis need fixing.
- Montage blend out returns control abruptly; tune blend times and Enable Auto Blend Out.
- Scaling actors scales root motion; check vault distance on scaled characters.

## Verify
- [ ] At 150 ms emulated lag, root motion attacks show no rubber-banding for the owning client.
