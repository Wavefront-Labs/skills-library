---
id: computing-software.computer-graphics-engineering.opengl.vulkan-nonuniform-indexing-and-update-after-bind
name: vulkan-nonuniform-indexing-and-update-after-bind
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-descriptors, nonuniformext, update-after-bind, partially-bound]
level: advanced
status: docs-checked
description: "Get Vulkan bindless right: nonuniformEXT on divergent indices, UPDATE_AFTER_BIND and PARTIALLY_BOUND flags, variable counts, and the corruption you get otherwise."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/features.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GL_EXT_nonuniform_qualifier.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nonuniformEXT and update-after-bind

## nonuniformEXT
Indexing a descriptor array with a value that differs across invocations of one draw/subgroup
**must** be marked:
```glsl
#extension GL_EXT_nonuniform_qualifier : require
layout(set = 0, binding = 0) uniform texture2D textures[];
layout(set = 0, binding = 1) uniform sampler samp;
layout(location = 0) flat in uint vMaterial;       // can differ per triangle in a merged draw
vec4 c = texture(sampler2D(textures[nonuniformEXT(materials[vMaterial].albedo)], samp), uv);
```
The extension states Vulkan requires the qualifier when the index is not dynamically uniform, and indexing arrays by non-uniform expressions is only
allowed when the matching `...ArrayNonUniformIndexing` feature is enabled. Without the qualifier the result can be neighbouring triangles sampling
each other's textures. Put `nonuniformEXT` on the index expression at the point of use; the extension lists the operators through which the
qualifier propagates.

An index taken from a push constant is the same for every invocation of a draw, so it is dynamically uniform and needs no qualifier.

## Binding flags
```c
VkDescriptorBindingFlags flags[2] = {
  VK_DESCRIPTOR_BINDING_PARTIALLY_BOUND_BIT |              // unused slots may be invalid
  VK_DESCRIPTOR_BINDING_UPDATE_AFTER_BIND_BIT |            // update while bound / in flight (unused slots)
  VK_DESCRIPTOR_BINDING_VARIABLE_DESCRIPTOR_COUNT_BIT,     // last binding size chosen at allocation
  0 };
VkDescriptorSetLayoutBindingFlagsCreateInfo bf = { VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_BINDING_FLAGS_CREATE_INFO };
bf.bindingCount = 2; bf.pBindingFlags = flags;
layoutCI.pNext = &bf;
layoutCI.flags = VK_DESCRIPTOR_SET_LAYOUT_CREATE_UPDATE_AFTER_BIND_POOL_BIT;
// pool: VK_DESCRIPTOR_POOL_CREATE_UPDATE_AFTER_BIND_BIT
// allocation: VkDescriptorSetVariableDescriptorCountAllocateInfo { counts = {100000} }
```
Features to enable (1.2 `VkPhysicalDeviceVulkan12Features`): `descriptorIndexing`,
`shaderSampledImageArrayNonUniformIndexing`, `runtimeDescriptorArray`,
`descriptorBindingPartiallyBound`, `descriptorBindingSampledImageUpdateAfterBind`,
`descriptorBindingVariableDescriptorCount`.

## Update-after-bind semantics
- You may write descriptors that the GPU is **not** currently using even while the set is bound
  in pending command buffers. Writing a slot an in-flight draw reads is still a race: free
  slots only after the frames that used them complete (deferred free list).
- Limits come from the `maxPerStageDescriptorUpdateAfterBind*` / `maxDescriptorSetUpdateAfterBind*`
  properties (much larger minimums than the normal limits, for example 500000 for several; see the required-limits table).

## Gotchas
- Without `PARTIALLY_BOUND`, every element must be valid, even unused ones; fill with a
  default texture or use the flag.
- `robustness`: out-of-range indices are undefined; clamp in debug builds and use GPU-assisted
  validation to catch them.

## Verify
- [ ] Mixed-material merged draw looks correct on AMD/Intel; GPU-assisted validation reports no OOB descriptor index.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and the GL_EXT_nonuniform_qualifier text. Confirmed: the GLSL extension says Vulkan requires `nonuniformEXT` when indexing descriptor bindings with an index that is not dynamically uniform, and lists the operators through which it propagates (so the old advice that it does not propagate through all compilers was removed); `PARTIALLY_BOUND` means only dynamically used descriptors must be valid, and without it all statically used descriptors must be valid; `UPDATE_AFTER_BIND` semantics; all feature and flag names; update-after-bind limits have minimums such as 500000. Removed the AMD/Intel/NVIDIA behaviour description, the `gl_DrawID` claim and the HLSL line, which none of the checked documents cover.

Method: documentation only; no commands were run.
