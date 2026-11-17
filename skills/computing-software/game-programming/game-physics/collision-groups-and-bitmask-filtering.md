---
id: computing-software.game-programming.game-physics.collision-groups-and-bitmask-filtering
name: collision-groups-and-bitmask-filtering
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, collision-filtering, category-mask-bits, collision-groups, broad-phase, contact-filter, game-programming]
level: practitioner
status: verified
description: "Design physics collision filtering: category/mask bit pairs, group indices, custom contact filters, query filters, and a layer table that scales across a project."
sources: ["https://box2d.org/documentation/", "https://github.com/erincatto/box2d", "https://jrouwe.github.io/JoltPhysics/index.html#collision-detection", "https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collision groups and bitmask filtering

## Category and mask
Each shape has `category` bits (what I am) and `mask` bits (what I collide with); Box2D v3 stores them as 64-bit values. Box2D's rule (`b2ShouldShapesCollide` in `src/shape.h`):
```c
bool ShouldCollide(Filter a, Filter b) {
    if (a.groupIndex == b.groupIndex && a.groupIndex != 0)
        return a.groupIndex > 0;                       // same positive group: always; negative: never
    return (a.maskBits & b.categoryBits) != 0 && (a.categoryBits & b.maskBits) != 0;
}
```
The check is **symmetric**: both sides must accept each other. Forgetting one side is the classic
"why don't these collide" bug.

## A project layer table
```
bit 0 World static     mask: everything
bit 1 Player           mask: World, Enemy, EnemyProjectile, Trigger
bit 2 Enemy            mask: World, Player, PlayerProjectile, Enemy
bit 3 PlayerProjectile mask: World, Enemy
bit 4 EnemyProjectile  mask: World, Player
bit 5 Trigger          mask: Player
bit 6 Ragdoll          mask: World
bit 7 Debris           mask: World            (no gameplay cost)
```
Keep it in one source file/config, generated into engine settings where possible; review it when
adding a layer. Run through the symmetric rule above this table gives exactly these colliding pairs: World-World,
World with Player/Enemy/PlayerProjectile/EnemyProjectile/Ragdoll/Debris, Player-Enemy, Player-EnemyProjectile,
Player-Trigger, Enemy-Enemy, Enemy-PlayerProjectile. World does **not** collide with Trigger even though World's
mask is 'everything', because Trigger's mask lacks World: the one-sided declaration is silently ignored.

## Beyond bits
- **Group index / ignore pairs:** a character's own parts, a vehicle and its wheels. Box2D negative
  group; Jolt `GroupFilterTable` (sub-group pairs); PhysX/Unity `Physics.IgnoreCollision(a, b)`.
- **Custom filter callbacks** for game logic (one-way platforms, team-based friendly fire): Box2D
  `b2World_SetCustomFilterCallback` (type `b2CustomFilterCallbackFcn`, only called for shapes with
  `enableCustomFiltering`) or `b2World_SetPreSolveCallback`; Jolt `ObjectLayerPairFilter` + `ContactListener::OnContactValidate`.
- **Broad-phase layers (Jolt):** each `BroadPhaseLayer` has its own tree (typically one for static, one for moving bodies),
  mapped from object layers by `BroadPhaseLayerInterface` and filtered by `ObjectVsBroadPhaseLayerFilter`.

## Queries
Ray and shape casts take their own filter (Box2D: `b2QueryFilter` with category and mask bits, tested both ways by `b2ShouldQueryCollide`). Common bug: the line-of-sight ray hits the
shooter's own collider or triggers. Use a dedicated query mask and exclude triggers.

## Engine mapping
| Engine | Mechanism |
|---|---|
| Unity | Layers + Layer Collision Matrix (Edit > Project Settings > Physics); LayerMask in queries; per-collider `includeLayers`/`excludeLayers`; `Physics.IgnoreCollision`, `Physics.IgnoreLayerCollision` |
| Godot | `collision_layer` / `collision_mask` (32 layers); the mask is what a body scans: A detects B if A.mask has B.layer |
| Box2D / Jolt | category/mask bits, groups, object and broad-phase layers |
Godot documents the mask as what a body scans for, i.e. a per-body one-directional declaration, unlike Box2D's symmetric test. Unity warns that include/exclude settings on two colliders can give conflicting decisions.

## Verify
- [ ] Table-driven test spawns one body per layer pair and asserts collide/no-collide.
- [ ] Physics debug view colours shapes by layer.

## Checked (2026-10-22)
- Box2D main: `b2ShouldShapesCollide` and `b2ShouldQueryCollide` in `src/shape.h` (rule identical to the skill's code), 64-bit `categoryBits`/`maskBits` and `groupIndex` in `types.h`, `b2CustomFilterCallbackFcn` + `enableCustomFiltering` + `b2World_SetCustomFilterCallback` (the old name `b2CustomFilterFcn` does not exist), `b2World_SetPreSolveCallback`.
- Ported the Box2D rule and the skill's layer table to Python and enumerated all pairs (list added; World-Trigger is the one-sided case). Negative group never collides, positive group always collides, one-sided masks do not collide.
- Jolt master headers: `GroupFilterTable`, `ObjectLayerPairFilter`, `BroadPhaseLayerInterface`, `ObjectVsBroadPhaseLayerFilter`, `OnContactValidate`; Architecture.md on broad-phase layers.
- Unity ScriptReference/manual: `Collider.includeLayers`, `Physics.IgnoreCollision`, `IgnoreLayerCollision`, Layer Collision Matrix path. Godot docs source: 32 layers, mask meaning.
- Removed the Unreal row (could not be checked) and the unverified 'Unity 32 layers' wording; the C code is Box2D's own rule, run as the Python port.
