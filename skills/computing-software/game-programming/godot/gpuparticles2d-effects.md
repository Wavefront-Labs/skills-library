---
id: computing-software.game-programming.godot.gpuparticles2d-effects
name: gpuparticles2d-effects
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-2d, gpuparticles2d, cpuparticles2d, particleprocessmaterial, one-shot, emitting, particle-effects, game-programming]
level: intro
status: docs-checked
description: "Make 2D effects in Godot with GPUParticles2D: ParticleProcessMaterial settings, one-shot bursts, pre-warming, local vs world coords, CPUParticles2D fallback and performance."
sources: ["https://docs.godotengine.org/en/stable/tutorials/2d/particle_systems_2d.html", "https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html", "https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPUParticles2D effects

**Goal:** dust puffs, hit sparks, explosions and ambient effects that look right and do not cost
much.

## Building an effect
1. `GPUParticles2D` with `process_material = ParticleProcessMaterial`, `texture` (soft circle, spark).
2. Key node properties: `amount`, `lifetime`, `one_shot`, `explosiveness` (0 = steady stream,
   1 = all at once), `randomness`, `local_coords` (particles move with the node vs stay in world),
   `preprocess` (simulate seconds in advance for ambient effects already "running").
3. ParticleProcessMaterial: Emission Shape (point, sphere, box, ring, points from texture), Direction
   + Spread, Initial Velocity min/max, Gravity, Damping, Scale + Scale Curve, Color + Color Ramp
   (fade out alpha), Angular velocity, Hue variation.

## One-shot bursts from code
```gdscript
const HIT_SPARKS := preload("res://fx/hit_sparks.tscn")
func spawn_sparks(pos: Vector2, normal: Vector2) -> void:
    var p: GPUParticles2D = HIT_SPARKS.instantiate()
    get_tree().current_scene.add_child(p)          # not a child of the dying enemy
    p.global_position = pos
    p.rotation = normal.angle()
    p.one_shot = true
    p.emitting = true
    p.finished.connect(p.queue_free)               # finished is only emitted by one_shot emitters
```
`restart()` re-triggers a one-shot on a reused instance. The class reference says that after `finished`
there can be a short period where setting `emitting = true` does not restart the cycle, and that
`restart()` avoids the delay.

## World vs local
`local_coords = false` (the default: particles live in world space): trails stay behind a
moving emitter (rocket smoke). `true` makes particles move with the emitter (aura around the player).

## Performance
- GPUParticles2D: processed on the GPU. CPUParticles2D has near-feature parity but lower performance with
  large particle counts; it can do better on low-end systems or in GPU-bottlenecked scenes. The docs
  recommend GPUParticles2D unless there is a reason not to.
- Convert between the two in the editor 2D toolbar; converting GPU to CPU may have issues if you use
  GPU-only features (such as trails).
- Keep `amount` low for frequent effects; use `visibility_rect` correctly (it controls whether particles
  are rendered: outside the viewport they are not drawn, so too small = effect disappears at screen
  edges; use Particles > Generate Visibility Rect on the selected node).
- If a flipbook texture has a black background, set the CanvasItemMaterial blend mode to Add.

## Verify
- [ ] Bursts spawned at a dying enemy remain visible after the enemy is freed.
- [ ] Effects remain visible at screen edges (visibility rect correct).

## Checked
2026-11-08. Confirmed against the 2D particle systems tutorial and the GPUParticles2D class reference:
explosiveness, preprocess, local coords default (off), one-shot, visibility rect generation, finished
signal and restart(), CPU/GPU trade-offs; ParticleProcessMaterial property names against its class page.
Removed: Godot version gates, shader-compilation hitch and ubershader claims, renderer compatibility claim,
the exact convert menu label. The code sample is illustrative and was not run.
Method: documentation only; no commands were run.
