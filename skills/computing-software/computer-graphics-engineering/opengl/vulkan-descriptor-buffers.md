---
id: computing-software.computer-graphics-engineering.opengl.vulkan-descriptor-buffers
name: vulkan-descriptor-buffers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-descriptors, descriptor-buffer, vk-ext-descriptor-buffer, bindless]
level: advanced
status: docs-checked
description: "Write Vulkan descriptors straight into GPU buffers with VK_EXT_descriptor_buffer: layout sizes and offsets, vkGetDescriptorEXT, binding and pitfalls."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_descriptor_buffer.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorbuffers.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Descriptor buffers (VK_EXT_descriptor_buffer)

**Goal:** manage descriptors as plain memory (like D3D12 heaps): no descriptor pools, no
`vkUpdateDescriptorSets`, cheap per-draw offsets.

**Status:** `VK_EXT_descriptor_buffer` is marked deprecated by `VK_EXT_descriptor_heap` in the Vulkan registry; it remains usable on implementations that expose it.

## 1. Layouts
Create set layouts with `VK_DESCRIPTOR_SET_LAYOUT_CREATE_DESCRIPTOR_BUFFER_BIT_EXT` (such layouts can only be
used with descriptor buffers and cannot contain `UNIFORM_BUFFER_DYNAMIC` or `STORAGE_BUFFER_DYNAMIC` bindings or
use update-after-bind pools), and pipelines with `VK_PIPELINE_CREATE_DESCRIPTOR_BUFFER_BIT_EXT`. Query sizes:
```cpp
VkDeviceSize layoutSize; vkGetDescriptorSetLayoutSizeEXT(dev, layout, &layoutSize);
layoutSize = alignUp(layoutSize, dbProps.descriptorBufferOffsetAlignment);
VkDeviceSize off; vkGetDescriptorSetLayoutBindingOffsetEXT(dev, layout, binding, &off);
```
## 2. Write descriptors
Buffer created with `VK_BUFFER_USAGE_RESOURCE_DESCRIPTOR_BUFFER_BIT_EXT` (and
`SAMPLER_DESCRIPTOR_BUFFER_BIT_EXT` for samplers) + `SHADER_DEVICE_ADDRESS_BIT` (needed to query the
buffer's address), host-visible and mapped:
```cpp
VkDescriptorImageInfo ii{VK_NULL_HANDLE, view, VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL};
VkDescriptorGetInfoEXT gi{VK_STRUCTURE_TYPE_DESCRIPTOR_GET_INFO_EXT};
gi.type = VK_DESCRIPTOR_TYPE_SAMPLED_IMAGE; gi.data.pSampledImage = &ii;
vkGetDescriptorEXT(dev, &gi, dbProps.sampledImageDescriptorSize,
                   mapped + setOffset + off + arrayIndex * dbProps.sampledImageDescriptorSize);
```
Uniform/storage buffers are described by `VkDescriptorAddressInfoEXT` (device address + range).

## 3. Bind
```cpp
VkDescriptorBufferBindingInfoEXT bi{VK_STRUCTURE_TYPE_DESCRIPTOR_BUFFER_BINDING_INFO_EXT};
bi.address = dbAddress; bi.usage = VK_BUFFER_USAGE_RESOURCE_DESCRIPTOR_BUFFER_BIT_EXT;
vkCmdBindDescriptorBuffersEXT(cmd, 1, &bi);
uint32_t idx = 0; VkDeviceSize setOff = frame * layoutSize;
vkCmdSetDescriptorBufferOffsetsEXT(cmd, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeLayout, 0, 1, &idx, &setOff);
```
Descriptor-buffer bindings and classic `vkCmdBindDescriptorSets` bindings invalidate each other, so
bind the buffers once per command buffer and switch sets with `vkCmdSetDescriptorBufferOffsetsEXT`.
The bound buffer address must be a multiple of `descriptorBufferOffsetAlignment`, and the layout size
may be larger than the sum of its descriptors.

## Gotchas
- Descriptor memory written by the CPU is read by the GPU at execution: double/triple buffer
  per frame in flight, exactly like uniform data.
- Query `maxResourceDescriptorBufferRange`, `maxSamplerDescriptorBufferRange` and the per-type descriptor
  sizes in `VkPhysicalDeviceDescriptorBufferPropertiesEXT`; samplers use the `SAMPLER_DESCRIPTOR_BUFFER_BIT_EXT` usage.
- A pipeline created with `VK_PIPELINE_CREATE_DESCRIPTOR_BUFFER_BIT_EXT` is used with descriptor buffers instead of descriptor sets.

## Verify
- [ ] Validation clean; a GPU capture shows the expected resources per draw.
- [ ] Profile shows descriptor update CPU time near zero for large scenes.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and vk.xml. Confirmed: all function, struct, flag and limit names used exist (`vkGetDescriptorSetLayoutSizeEXT`, `vkGetDescriptorSetLayoutBindingOffsetEXT`, `vkGetDescriptorEXT`, `vkCmdBindDescriptorBuffersEXT`, `vkCmdSetDescriptorBufferOffsetsEXT`, `VkDescriptorGetInfoEXT.data.pSampledImage`); layouts with the descriptor-buffer bit cannot use dynamic buffer descriptor types or update-after-bind pools; classic set bindings and descriptor-buffer bindings invalidate each other; the buffer binding address must be aligned to `descriptorBufferOffsetAlignment`; `vkGetBufferDeviceAddress` needs `SHADER_DEVICE_ADDRESS_BIT`; vk.xml marks the extension `deprecatedby` VK_EXT_descriptor_heap. Removed the rebinding-cost claim, the sampler count claim and the tooling-support claim.

Method: documentation only; no commands were run.
