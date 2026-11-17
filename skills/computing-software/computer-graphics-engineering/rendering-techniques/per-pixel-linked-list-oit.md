---
id: computing-software.computer-graphics-engineering.rendering-techniques.per-pixel-linked-list-oit
name: per-pixel-linked-list-oit
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, linked-list-oit, order-independent-transparency, a-buffer, atomics, compute-shader]
level: advanced
status: draft
description: "Implement exact OIT with per-pixel linked lists: head-pointer image, atomic node allocation, sort-and-blend resolve, memory budgets and overflow handling."
sources: ["https://www.gdcvault.com/play/1014546/", "https://on-demand.gputechconf.com/gtc/2014/presentations/S4385-order-independent-transparency-opengl.pdf", "https://github.com/nvpro-samples/vk_order_independent_transparency"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Per-pixel linked list OIT

An A-buffer: every transparent fragment is stored, then each pixel's fragments are sorted by depth
and blended exactly.

## 1. Resources
- Head pointer image `r32ui` (screen size), cleared to 0xFFFFFFFF each frame.
- Node buffer: `struct Node { uint color; float depth; uint next; }` (12-16 bytes), capacity
  `screenPixels * avgLayers` (e.g. 1920x1080 x 8 x 16 B = 265 MB at full depth; budget carefully).
- Atomic counter.

## 2. Build pass (transparent geometry, no blending, early depth test against opaques)
```glsl
layout(early_fragment_tests) in;
void main() {
    uint idx = atomicAdd(counter, 1u);
    if (idx >= maxNodes) return;                            // overflow: drop
    uint prev = imageAtomicExchange(headPtr, ivec2(gl_FragCoord.xy), idx);
    nodes[idx] = Node(packUnorm4x8(premultipliedColor), gl_FragCoord.z, prev);
}
```
Colour writes disabled; depth write off.

## 3. Resolve pass (fullscreen)
```glsl
Node local[MAX_LAYERS]; int n = 0;
uint i = imageLoad(headPtr, p).r;
while (i != 0xFFFFFFFFu && n < MAX_LAYERS) { local[n++] = nodes[i]; i = nodes[i].next; }
// insertion sort by depth (far to near)
for (int a = 1; a < n; a++) { Node k = local[a]; int b = a - 1;
    while (b >= 0 && local[b].depth < k.depth) { local[b + 1] = local[b]; b--; } local[b + 1] = k; }
vec4 col = vec4(opaque, 1.0);
for (int k = 0; k < n; k++) { vec4 c = unpackUnorm4x8(local[k].color); col.rgb = c.rgb + col.rgb * (1.0 - c.a); }
```
MAX_LAYERS 8-32; sort in registers. Fragments beyond the cap: merge the farthest into a tail
(k-buffer style) rather than dropping.

## 4. Variants
- **Fixed-size per-pixel arrays** (k-buffer) avoid pointer chasing but waste memory.
- **Fragment shader interlock / ROVs** (`GL_ARB_fragment_shader_interlock`, D3D ROV) enable
  in-place k-buffers without lists.
- Store colour as RGBA8 premultiplied or R11G11B10 + alpha to save memory.

## Gotchas
- Memory scales with depth complexity: particles can create hundreds of layers; exclude them
  (render particles with weighted blended OIT) or cap.
- Divergent list lengths across a warp hurt resolve performance.
- MSAA multiplies node count; usually not combined.

## Verify
- [ ] Matches a reference depth-peeled result exactly for scenes within the layer cap.
- [ ] Overflow counter monitored; no visible drops in worst-case views.
