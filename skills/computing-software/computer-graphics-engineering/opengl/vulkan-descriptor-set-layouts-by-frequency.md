---
id: computing-software.computer-graphics-engineering.opengl.vulkan-descriptor-set-layouts-by-frequency
name: vulkan-descriptor-set-layouts-by-frequency
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-descriptors, descriptor-set-layout, binding-frequency, pipeline-layout-design]
level: advanced
status: docs-checked
description: "Design Vulkan descriptor set layouts by update frequency (frame, pass, material, draw) so binds stay compatible across pipelines and rebinding is minimal."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/glossary.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Descriptor set layouts by binding frequency

## The standard scheme
| Set | Contents | Changes |
|---|---|---|
| 0 | per-frame: camera, time, global lights, shadow maps, bindless texture table | once per frame |
| 1 | per-pass: G-buffer inputs, pass constants | per render pass |
| 2 | per-material: material params UBO/SSBO slice, material textures | per material |
| 3 | per-draw (optional): object data, or use push constants / dynamic offsets | per draw |

```glsl
layout(set = 0, binding = 0) uniform Frame { mat4 viewProj; vec4 time; } frame;
layout(set = 2, binding = 0) uniform Material { vec4 baseColor; float roughness; } mat;
layout(set = 2, binding = 1) uniform sampler2D albedoTex;
layout(push_constant) uniform Draw { mat4 model; uint objectId; } draw;
```

## Why order matters: pipeline layout compatibility
Binding a new pipeline keeps descriptor sets 0..N bound if the pipeline layouts are compatible
up to set N: identical set layouts for those sets and identical push constant ranges. So:
- Put the least frequently changing sets at the lowest indices.
- Share the *same* `VkDescriptorSetLayout` objects (or identically defined ones) for sets 0-1
  across all pipelines; keep push constant ranges identical everywhere (e.g. one 128-byte
  range for all stages).
- Then switching pipeline/material only rebinds set 2+.

## Layout creation tips
```c
VkDescriptorSetLayoutBinding b[2] = {
  { 0, VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER, 1, VK_SHADER_STAGE_VERTEX_BIT | VK_SHADER_STAGE_FRAGMENT_BIT, NULL },
  { 1, VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, 1, VK_SHADER_STAGE_FRAGMENT_BIT, NULL } };
```
- Stage flags are part of compatibility: use the same broad flags (`ALL_GRAPHICS` or
  `VERTEX|FRAGMENT|COMPUTE`) for shared sets, or layouts differ.
- Cache layouts by a hash of their bindings to deduplicate (`VkDescriptorSetLayout` creation
  from reflection often creates duplicates).

## Limits
`maxBoundDescriptorSets` is guaranteed to be at least 4; Roadmap 2024 and the Vulkan 1.4 required limits raise
the minimum to 7. Design for 4 unless you require one of those.

## Modern alternative
Fully bindless: set 0 holds big arrays of all textures/buffers (descriptor indexing), per-draw
data is an index or buffer device address in push constants. Then there is basically one layout
for everything and rebinding disappears. Many engines combine: bindless set 0 + per-pass set 1.

## Gotchas
- Binding sets with a pipeline layout that is not compatible disturbs the sets bound earlier (their
  descriptors become undefined); rebind every disturbed set before drawing.

## Verify
- [ ] API dump shows per-frame set bound once per frame and only set 2+ rebinding between materials.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23). Confirmed in `descriptorsets.adoc` (Pipeline Layout Compatibility): layouts are compatible for set N when sets 0..N are identically defined (glossary: all creation arguments identical, which includes stage flags) and push constant ranges are identical; binding with an incompatible layout disturbs earlier and later sets. Confirmed in `limits.adoc`: `maxBoundDescriptorSets` minimum 4, and 7 for Roadmap 2024 and the Vulkan 1.4 limits; `maxPushConstantsSize` minimum 128 (256 for Vulkan 1.4 limits). Removed the dense-binding cost claim, the validation message text and the dynamic-offset ordering claim.

Method: documentation only; no commands were run.
