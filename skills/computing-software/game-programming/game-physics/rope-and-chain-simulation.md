---
id: computing-software.game-programming.game-physics.rope-and-chain-simulation
name: rope-and-chain-simulation
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, constraints, rope-simulation, verlet, distance-constraints, chain-joints, grappling-hook, game-programming]
level: practitioner
status: verified
description: "Simulate ropes and chains: Verlet particles with distance constraints, joint chains of rigid bodies, attaching to dynamics, collision, stretch and the mass-ratio problem."
sources: ["https://www.cs.cmu.edu/afs/cs/academic/class/15462-s13/www/lec_slides/Jakobsen.pdf", "https://matthias-research.github.io/pages/publications/XPBD.pdf", "https://box2d.org/documentation/md_simulation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rope and chain simulation

## Option A: Verlet particles + distance constraints (Jakobsen)
Best for visual or lightly interactive ropes (cables, vines, grappling lines).
```cpp
// per fixed step
for (auto& p : pts) {                                 // Verlet integration
    Vec3 v = (p.pos - p.prev) * damping;              // damping ~0.99
    p.prev = p.pos;
    if (!p.pinned) p.pos += v + gravity * dt * dt;
}
for (int it = 0; it < iterations; ++it) {             // 10-30 iterations
    for (int i = 0; i + 1 < pts.size(); ++i) {
        Vec3 d = pts[i+1].pos - pts[i].pos;
        float len = length(d), err = (len - segLen) / len;
        float wa = pts[i].pinned ? 0 : 0.5f, wb = pts[i+1].pinned ? 0 : 0.5f;
        float w = wa + wb; if (w == 0) continue;
        pts[i].pos   += d * err * (wa / w);
        pts[i+1].pos -= d * err * (wb / w);
    }
    collideWithWorld(pts);                            // push particles out of colliders
}
```
More iterations or substeps = less stretch (the 20-point rope below, 20 iterations at 60 Hz, hung 1.2% longer than rest
length). XPBD with compliance gives timestep-independent stiffness.

## Option B: chain of rigid bodies with joints
Capsules joined by ball/hinge joints (Unity `CharacterJoint`/`ConfigurableJoint`, Box2D revolute
chain, Godot `PinJoint3D`). Interacts properly with other physics, but:
- **Mass ratio problem:** a heavy object on a light chain stretches and jitters (the Small Steps paper shows substeps
  fix this better than more iterations). Keep neighbouring mass ratios modest, add substeps, or add a long-range distance
  limit from anchor to end (Box2D v3 distance joint with `enableLimit` and `maxLength`) to cap stretch.
- Disable collision between adjacent links.

## Option C: a single distance constraint
A grappling hook or swinging rope often only needs one max-distance constraint between player and
anchor (Box2D distance joint with `maxLength`, Unity `SpringJoint`/`ConfigurableJoint` linear limit),
with the visual rope drawn as a curve or Verlet strand. Cheapest and most controllable.

## Wrapping around corners
For grappling: raycast between consecutive anchor points; when the line hits geometry, insert a new
anchor at the hit corner; remove it when the angle unwraps.

## Rendering
Draw a spline (Catmull-Rom) through particles, or a tube mesh; for chains, instance link meshes
aligned to segment directions.

## Verify
- [ ] Rope length stays within ~2-5% stretch under its heaviest attached load.
- [ ] No explosion when an attached body is teleported (re-seat particles on teleport).
