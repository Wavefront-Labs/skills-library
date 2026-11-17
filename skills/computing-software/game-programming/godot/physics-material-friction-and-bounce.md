---
id: computing-software.game-programming.godot.physics-material-friction-and-bounce
name: physics-material-friction-and-bounce
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-physics-material, physicsmaterial, friction, bounce, game-programming]
level: practitioner
status: docs-checked
description: "Tune Godot PhysicsMaterial friction, rough, bounce and absorbent on bodies, understand how two materials combine, and avoid jitter with high bounce."
sources: ["https://docs.godotengine.org/en/stable/classes/class_physicsmaterial.html", "https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html", "https://docs.godotengine.org/en/stable/classes/class_rigidbody3d.html", "https://docs.godotengine.org/en/stable/tutorials/physics/using_jolt_physics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PhysicsMaterial friction and bounce

**Goal:** ice that slides, rubber that bounces, mud that absorbs.

## Properties
Assign a `PhysicsMaterial` resource to a static body or rigid body (2D and 3D; the physics introduction
page names static and rigid bodies):
| Property | Range | Meaning |
|---|---|---|
| `friction` | 0-1 (default 1.0) | 0 frictionless, 1 maximum friction |
| `rough` | bool (default false) | see combining below |
| `bounce` | float (default 0.0) | bounciness |
| `absorbent` | bool (default false) | marks the surface as absorbent; see the class page for its effect on bounce |

## Combining
- Friction: if `rough` is true on one object the engine uses that object's friction; if false the lowest
  friction of all colliding objects is used; if true on both, the highest friction is used. So a very
  slippery floor makes objects slide unless one of them is rough.
- Jolt Physics is built into Godot since 4.4 as an alternative to Godot Physics, and new projects use it
  by default. Its contact handling differs, so retune and test with the engine you ship.

## Gotchas
- Check the physics body classes you use for whether they read physics materials; do not assume
  CharacterBody-style movement applies friction or bounce, and implement acceleration in script.

## Verify
- [ ] Objects slide/bounce as designed under the physics engine you ship (and the other, if both are supported).

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the PhysicsMaterial class page, the Physics introduction and the Using Jolt Physics page: friction 0-1 default 1.0, rough/absorbent/bounce defaults, rough combine rule (lowest friction unless rough; both rough takes highest), static and rigid bodies take a PhysicsMaterial, Jolt added in 4.4 and default for new projects. Removed: sum-and-clamp bounce rule, absorbent subtraction detail, AnimatableBody and CharacterBody claims, per-shape claim, bounce-near-1 jitter claim, recipe numbers and the 0.95 limit.
Method: documentation only; no commands were run.
