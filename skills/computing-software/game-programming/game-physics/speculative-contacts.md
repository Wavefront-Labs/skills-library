---
id: computing-software.game-programming.game-physics.speculative-contacts
name: speculative-contacts
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, ccd, continuous-collision-detection, speculative-contacts, speculative-margin, ghost-collisions, contact-solver, unity-continuous-speculative, game-programming]
level: advanced
status: verified
description: "Use speculative contacts for cheap continuous collision: creating contacts before touch with negative separation, solver treatment, margin sizing, and ghost-collision artifacts."
sources: ["https://docs.unity3d.com/Manual/speculative-ccd.html", "https://box2d.org/posts/2020/06/ghost-collisions/", "https://github.com/jrouwe/JoltPhysics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Speculative contacts

**Goal:** prevent tunnelling for most fast motion at almost no extra cost by letting the regular
contact solver handle contacts that have not happened yet.

## Idea
During narrow phase, create contacts for shape pairs that are **not yet touching** but are within a
margin that covers this step's motion. Such a contact has positive separation `s > 0`. The solver
allows the bodies to approach by at most `s` this step:
```
velocity constraint for a speculative contact:
    allowed approach speed = s / dt
    impulse applied only if relative normal velocity would exceed it:
    lambda = -m_eff * (vn + s / dt), clamped to lambda >= 0
```
If the bodies would not reach each other this step, the impulse is zero and nothing happens. If they
would, they arrive exactly touching. No TOI search or sub-stepping is required.

## Margin
- Margin = |relative velocity| * dt (+ a small constant), computed per pair from the broad phase's
  expanded (swept) AABBs. Unity's manual describes its Continuous Speculative mode this way (AABB inflated by linear and angular motion).
- Box2D v3 and Jolt use a fixed distance instead: `B2_SPECULATIVE_DISTANCE` is 4 * 0.005 m = 0.02 m and Jolt's `mSpeculativeContactDistance`
  defaults to 0.02 m, so on their own they do not stop very fast bodies; they are paired with continuous collision (Box2D) or LinearCast (Jolt).
- Too small: fast objects still tunnel. Too large: many more contact pairs and more ghost collisions (Jolt's header says the same).

## Ghost collisions (the main artifact)
Because contacts are created from current geometry and the predicted path (Unity: from the closest-point algorithm, so the contact normal can be inaccurate), objects can be stopped by
a contact that would not have happened (e.g. sliding fast across a seam of two boxes, a ball passing
near a corner it would miss). Symptoms: objects bumping on flat composite floors or bouncing off
invisible edges at speed. Mitigations: smaller margins, merging collision geometry (one mesh/chain
instead of tiles), smooth chain shapes with ghost vertices (Box2D chain shapes), restricting
speculative contacts to fast bodies.

## Rotation
Speculative margins computed from linear velocity can miss fast-rotating thin objects; add an angular
term (`|w| * radius * dt`) or keep TOI for such bodies.

## In engines
- Unity: Rigidbody collision detection mode **Continuous Speculative**: less computation than sweep-based CCD, handles linear and rotational motion,
  but can give false (ghost) collisions and can still miss collisions if the solver adds too much energy.
- Box2D v3 uses speculative contacts by default with continuous collision for fast vs static.
- Many custom engines combine speculative contacts with a TOI pass for bullets.

## Verify
- [ ] Fast boxes do not tunnel through thin walls with speculative mode only.
- [ ] Rolling a fast ball across a tiled floor shows no bumps (or tiles merged/chain shapes used).
- [ ] Contact pair count increase vs discrete mode measured and acceptable.

## Checked (2026-10-22)
- Python check of the velocity constraint `lambda = -m_eff * (vn + s/dt)` clamped at 0 (unit mass, dt = 1/60): gap 0.5 m at 10 m/s approach gives lambda 0 (travel 0.167 m, no contact); gap 0.1 m at 10 m/s gives lambda 4.0, new approach speed 6.0 m/s, travel exactly 0.1 m (arrives touching); at 6 m/s and 5 m/s lambda 0 with travel 0.10 and 0.083 m. This confirms the skill's formula.
- Unity manual 'Speculative CCD' page (fetched): inflated AABB from linear and angular motion, less demanding than sweep-based, ghost collisions from closest-point normals, missed collisions when the solver adds energy. Unity `CollisionDetectionMode` ScriptReference. Box2D main `constants.h` (`B2_SPECULATIVE_DISTANCE`, `B2_LINEAR_SLOP`); Jolt `PhysicsSettings.h` comment on ghost collisions and 0.02 default.
- Removed 'works for kinematic bodies too' for Unity (not stated on the pages read).
