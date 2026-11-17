---
id: computing-software.game-programming.game-engine-architecture.debug-drawing-system
name: debug-drawing-system
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, debug-tools, debug-draw, immediate-mode, debug-lines, debug-text, gizmos, visual-debugging, game-programming]
level: practitioner
status: draft
description: "Build an immediate-mode debug drawing API: lines, boxes, spheres, text with durations, depth-test options, batching into one draw call, categories and stripping from shipping."
sources: ["https://www.gameenginebook.com/", "https://github.com/glampert/debug-draw", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/DrawDebugLine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debug drawing system

**Goal:** any programmer can call `DebugDraw::sphere(pos, r, Color::Red, 2.0f)` from anywhere,
including gameplay, physics and AI threads, and see it in the world (Gregory GEA ch. 10.2).

## API shape (immediate mode)
```cpp
namespace DebugDraw {
    void line(Vec3 a, Vec3 b, Color c, float duration = 0, bool depthTest = true);
    void arrow(Vec3 from, Vec3 to, Color c, float duration = 0);
    void box(const AABB& b, Color c, float duration = 0);
    void obb(const Mat4& xf, Vec3 halfExtents, Color c, float duration = 0);
    void sphere(Vec3 center, float r, Color c, float duration = 0);
    void cross(Vec3 p, float size, Color c, float duration = 0);
    void text(Vec3 worldPos, std::string_view s, Color c, float duration = 0);
    void text2D(Vec2 screenPos, std::string_view s, Color c);
    void axes(const Mat4& xf, float size, float duration = 0);
}
```
`duration = 0` means "this frame only"; > 0 keeps the primitive for that many seconds (useful for
one-shot events like impacts or raycasts).

## Implementation
- Each call appends to a per-thread buffer of primitives (or one buffer with a mutex/atomic append);
  shapes are tessellated into line vertices at submission or render time.
- Once per frame: merge buffers, build one dynamic vertex buffer with all lines (position + color),
  draw with two draw calls: depth-tested and always-on-top. Text through the debug font renderer,
  projected to screen.
- Expire timed primitives by subtracting frame time; frame-only primitives are cleared after render.
- Cap memory (e.g. 1M line vertices); drop and warn when full.

## Categories and toggles
Tag calls with a category (`Physics`, `AI`, `Nav`, `Audio`) and expose toggles in a dev console or
ImGui panel (`debugdraw ai 1`). Per-entity filters ("only draw AI for selected entity") keep the
screen readable.

## Stripping
Wrap calls in a macro that compiles out in shipping:
```cpp
#if ENABLE_DEBUG_DRAW
  #define DD_SPHERE(...) DebugDraw::sphere(__VA_ARGS__)
#else
  #define DD_SPHERE(...) ((void)0)
#endif
```
Arguments are not evaluated when stripped, so expensive argument computations vanish too.

## Engine equivalents
Unreal `DrawDebugLine/Sphere/Box/String` (Engine/DrawDebugHelpers.h), with `bPersistentLines`,
`LifeTime`, `DepthPriority`; Unity `Debug.DrawLine/DrawRay` (Scene view and Game view with Gizmos on)
and `OnDrawGizmos`; Godot has no built-in 3D debug draw API (use an ImmediateMesh helper or addon).

## Verify
- [ ] 100k debug lines in one frame cost one or two draw calls and stay within a few ms.
- [ ] Calls from worker threads are safe (no crashes under thread sanitizer).
- [ ] Shipping build contains no debug draw symbols or costs.
