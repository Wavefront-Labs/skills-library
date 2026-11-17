---
id: computing-software.computer-graphics-engineering.opengl.vulkan-descriptor-sets-and-pipeline-layouts
name: vulkan-descriptor-sets-and-pipeline-layouts
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [vulkan, descriptor-sets, descriptor-pool, pipeline-layout, push-constants, bindless, descriptor-indexing, update-frequency, uniform-buffer, storage-buffer, opengl-ubo, binding-model]
level: advanced
status: docs-checked
description: "Design a Vulkan descriptor set layout and update strategy by binding frequency, pick push constants vs UBOs, and use bindless indexing without pool-exhaustion bugs."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/extensions/ARB/ARB_bindless_texture.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan descriptor sets and pipeline layouts

**Goal:** structure resource bindings so the GPU driver can bind them cheaply and
your code doesn't deadlock on descriptor pool exhaustion mid-game. This is the
part of Vulkan where a "works on my machine, runs out of descriptors after an
hour" bug hides.

## Organise by update frequency
A `VkPipelineLayout` is built from `VkDescriptorSetLayout`s; how many sets can be bound at once is limited by
`maxBoundDescriptorSets` (guaranteed minimum 4; check the actual value). Group bindings by how often they change, not by what
they conceptually belong to:
- **Set 0**: per-frame/global (camera matrices, lighting, time) — bound once per
  frame.
- **Set 1**: per-pass (shadow pass vs main pass resources).
- **Set 2**: per-material (textures, material constants) — bound per draw-call
  group sharing a material.
- **Set 3**: per-object (if not using push constants/instancing for this).
This minimises rebinding cost: changing only the lowest-frequency set that
actually changed between draws is cheaper than rebinding everything per draw.

## Push constants vs UBOs
- **Push constants**: tiny (guaranteed minimum 128 bytes, 256 in the Vulkan 1.4 limits), no descriptor
  needed, cheapest update path — use for per-draw data that changes every call
  (object index, small transform data) rather than a UBO you'd have to rebind.
- **Uniform buffers**: for anything bigger, or shared across many draws without
  re-uploading. Per-frame-in-flight duplication still applies (see
  `opengl.vulkan-opengl-frame-setup-and-synchronisation`) — one UBO region per
  frame in flight if the CPU writes it every frame.
- Dynamic UBOs (`VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER_DYNAMIC`) let one descriptor
  binding address different offsets into a large buffer per draw via a dynamic
  offset at bind time — cheaper than allocating/binding a separate descriptor set
  per object when object data is small and uniform in size.

## Descriptor pools: the exhaustion bug
- A `VkDescriptorPool` is created with fixed max counts per descriptor type and
  max set count — **allocating beyond those limits fails**
  (`VK_ERROR_OUT_OF_POOL_MEMORY`), and this failure often only manifests after
  enough frames/objects have cycled through, not at startup, if sets are
  allocated and freed dynamically without a clear budget.
- Prefer sizing pools for the actual maximum concurrent descriptor sets needed
  (computed from asset counts, not guessed), or use one large pool per frame in
  flight that's **reset** (not individually freed) each cycle
  (`vkResetDescriptorPool`) when sets are transient/per-frame.
- `VK_DESCRIPTOR_POOL_CREATE_FREE_DESCRIPTOR_SET_BIT` is needed if you intend to
  free individual sets rather than reset the whole pool — omitting it and trying
  to free anyway is a validation error.

## Bindless (descriptor indexing)
- Modern engines increasingly use **bindless**: one large descriptor array (e.g.
  all scene textures) bound once, indexed in the shader by an integer from a
  per-draw/per-instance buffer, instead of rebinding per-material descriptor sets.
  Requires `VK_EXT_descriptor_indexing` (core in 1.2) features: `runtimeDescriptorArray`,
  `shaderSampledImageArrayNonUniformIndexing`, and the `nonuniformEXT()` qualifier
  in shader code when the index isn't dynamically uniform across the invocation
  group (skipping this on hardware that needs it causes undefined/wrong texture
  reads, not a validation error on all drivers).
- Bindless trades descriptor-rebinding overhead for simpler, more GPU-driven
  rendering (works naturally with indirect draws where the CPU doesn't know which
  materials will be used) at the cost of needing descriptor-indexing support and
  more careful validation of index bounds.

## OpenGL equivalent
GL's binding model (textures/UBOs bound to numbered units/binding points) is far
less structured — there's no equivalent "layout" object; the closest analogue to
bindless is `GL_ARB_bindless_texture` (sampler handles as 64-bit values passed
like any other uniform, skipping the bind-unit limit).

## Verify
- [ ] Descriptor set groupings match actual update frequency, not conceptual
      grouping — measured by counting rebinds per frame, not assumed.
- [ ] Descriptor pool sized from a computed maximum (asset counts × sets per
      asset), not a guessed constant; pool exhaustion tested under worst-case load.
- [ ] Dynamic/bindless indices confirmed `nonuniformEXT`-qualified where the index
      varies across an invocation group, if using descriptor indexing.
- [ ] Per-frame-in-flight duplication applied to any UBO written by the CPU every frame.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and the OpenGL-Registry ARB_bindless_texture text. Confirmed: the pipeline layout is limited by `maxBoundDescriptorSets` (minimum 4), not a fixed count of 4 (the original said it was built from up to 4 layouts); `maxPushConstantsSize` minimum 128 (256 in the Vulkan 1.4 limits); `VK_ERROR_OUT_OF_POOL_MEMORY` is returned when a pool has no space left, and sets can be freed individually only when the pool has the free-descriptor-set flag, otherwise only allocate and reset are allowed; `runtimeDescriptorArray` and `shaderSampledImageArrayNonUniformIndexing` are Vulkan 1.2 feature names (descriptor indexing is core in 1.2); `GL_ARB_bindless_texture` uses 64-bit handles. Removed the 'usually 4-8' hardware figure.

Method: documentation only; no commands were run.
