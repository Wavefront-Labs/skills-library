---
id: computing-software.game-programming.godot.particle-shaders
name: particle-shaders
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, particle-shader, gpuparticles, process-material, shaders, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot particle shaders (shader_type particles): start and process functions, CUSTOM and USERDATA, emitting sub-particles, collisions and converting ParticleProcessMaterial."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html", "https://docs.godotengine.org/en/stable/classes/class_gpuparticles3d.html", "https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Particle shaders

**Goal:** custom GPU particle behaviour (swarms, attractors, curl noise) beyond ParticleProcessMaterial.

## Start point
Create a ShaderMaterial with a `shader_type particles;` shader and assign it as the GPUParticles3D/2D
`process_material`. Particle shaders only work with the GPU particle nodes; CPUParticles are simulated on
the CPU (their drawing can still use custom canvas_item or spatial shaders).

## Structure
```glsl
shader_type particles;
uniform float speed = 4.0;
uniform vec3 attractor = vec3(0.0);

void start() {           // runs when a particle is spawned
    if (RESTART_POSITION) {
        TRANSFORM = EMISSION_TRANSFORM * mat4(1.0);
        TRANSFORM[3].xyz += vec3(fract(sin(float(INDEX)) * 43758.5), 0.0, 0.0);
    }
    if (RESTART_VELOCITY) VELOCITY = vec3(0.0, speed, 0.0);
    CUSTOM = vec4(0.0);  // x commonly lifetime progress
}
void process() {         // every frame per particle
    VELOCITY += normalize(attractor - TRANSFORM[3].xyz) * DELTA * 9.0;
    CUSTOM.y += DELTA / LIFETIME;
    COLOR.a = 1.0 - CUSTOM.y;
    if (CUSTOM.y >= 1.0) ACTIVE = false;
}
```
Built-ins: `TRANSFORM`, `VELOCITY` (ignored when the `disable_velocity` render mode is set),
`COLOR`, `CUSTOM` (passed to the draw material as `INSTANCE_CUSTOM`), `MASS`, `USERDATA1` to `USERDATA6`,
`NUMBER`, `INDEX`, `RANDOM_SEED`, `LIFETIME`, `DELTA`, `ACTIVE`. Other render modes: `keep_data`,
`disable_force`, `collision_use_scale`.

## Sub-emitters
Set the GPUParticles `sub_emitter`, then `emit_subparticle(TRANSFORM, VELOCITY, COLOR, CUSTOM,
FLAG_EMIT_POSITION | FLAG_EMIT_VELOCITY)` from process (e.g. sparks on death).

## Collision
Read `COLLIDED`, `COLLISION_NORMAL` and `COLLISION_DEPTH` (all set from the last collision with a
particle collider) in `process()` and respond yourself, for example by reflecting `VELOCITY`.

## Draw material
The mesh material reads `INSTANCE_CUSTOM` and `COLOR` (enable Vertex Color as Albedo in
StandardMaterial3D or use them in a spatial shader).

## Gotchas
- The node's `visibility_aabb` (GPUParticles3D, default 8x8x8 around the origin) or `visibility_rect`
  (GPUParticles2D) must cover the particles or they are culled when the emitter is off screen.
- CPUParticles are simulated on the CPU and do not run particle shaders.
- Randomness: derive it from `INDEX`, `NUMBER` and `RANDOM_SEED` with your own hash.

## Verify
- [ ] Particles behave identically after restart; no culling pops with the AABB set.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `start()` and `process()` functions; render modes `keep_data`, `disable_force`, `disable_velocity` and `collision_use_scale` (the earlier text had `DISABLE_VELOCITY`); built-ins `TRANSFORM`, `VELOCITY`, `COLOR`, `CUSTOM` (readable as `INSTANCE_CUSTOM` in the mesh shader), `MASS`, `USERDATA1` to `USERDATA6`, `NUMBER`, `INDEX`, `RANDOM_SEED`, `LIFETIME`, `DELTA`, `ACTIVE`, `EMISSION_TRANSFORM`, `RESTART_POSITION`, `RESTART_VELOCITY`, `COLLIDED`, `COLLISION_NORMAL`, `COLLISION_DEPTH`; `emit_subparticle(mat4, vec3, vec4, vec4, uint)` and the `FLAG_EMIT_*` constants; `GPUParticles3D.sub_emitter`, `GPUParticles3D.visibility_aabb` and `GPUParticles2D.visibility_rect`. Removed the unconfirmed Convert step, the USERDATA project-setting claim, the Compatibility-renderer claim and the list of collision node types.

Method: documentation only; no commands were run.
