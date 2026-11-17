---
id: computing-software.computer-graphics-engineering.opengl.vulkan-push-descriptors
name: vulkan-push-descriptors
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-descriptors, push-descriptors, vkcmdpushdescriptorset]
level: advanced
status: docs-checked
description: "Record Vulkan descriptors directly into command buffers with push descriptors (VK_KHR_push_descriptor, core 1.4): layout flag, per-draw use, and limits."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_push_descriptor.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/versions.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Push descriptors

Push descriptors are written straight into the command buffer: no descriptor pool, no set
allocation, no lifetime tracking. Good for per-draw or per-dispatch resources that change
constantly (post-processing chains, compute passes with ping-pong images, tools/editors).

## Layout
```c
VkDescriptorSetLayoutCreateInfo li = { VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO };
li.flags = VK_DESCRIPTOR_SET_LAYOUT_CREATE_PUSH_DESCRIPTOR_BIT_KHR;   // only ONE push set per pipeline layout
li.bindingCount = 2; li.pBindings = bindings;
vkCreateDescriptorSetLayout(dev, &li, NULL, &pushLayout);
```

## Recording
```c
VkDescriptorImageInfo src = { VK_NULL_HANDLE, inputView, VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL };
VkDescriptorImageInfo dst = { VK_NULL_HANDLE, outputView, VK_IMAGE_LAYOUT_GENERAL };
VkWriteDescriptorSet w[2] = {
  { VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET, NULL, 0 /*dstSet ignored*/, 0, 0, 1, VK_DESCRIPTOR_TYPE_SAMPLED_IMAGE, &src },
  { VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET, NULL, 0, 1, 0, 1, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE, &dst } };
vkCmdPushDescriptorSetKHR(cmd, VK_PIPELINE_BIND_POINT_COMPUTE, pipelineLayout, /*set*/ 1, 2, w);
vkCmdDispatch(cmd, gx, gy, 1);
```
The descriptors are recorded into the command buffer, so you manage no set objects. Use update templates
(`vkCmdPushDescriptorSetWithTemplateKHR`, core name `vkCmdPushDescriptorSetWithTemplate`) for lower CPU cost.

## Limits and support
- `maxPushDescriptors` (>= 32) total descriptors in the push set.
- Core in Vulkan 1.4 (gated by the `pushDescriptor` member of `VkPhysicalDeviceVulkan14Features`;
  commands lose the `KHR` suffix); also available as extension `VK_KHR_push_descriptor`.
- Combine: set 0 = bindless/global (normal set), set 1 = push descriptors for per-pass resources.

## Gotchas
- A pipeline layout may contain at most one set layout created with the push-descriptor flag
  (VUID-VkPipelineLayoutCreateInfo-pSetLayouts-00293).
- For many draws with identical resources, a normal set bound once avoids re-pushing; measure.

## Verify
- [ ] Descriptor pools for transient passes removed; validation clean; per-pass CPU time not regressed.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: `maxPushDescriptors` minimum is 32 (limits table); push descriptors are core in 1.4 (`VK_KHR_push_descriptor` promotedto `VK_VERSION_1_4`) with a new `pushDescriptor` feature bit in `VkPhysicalDeviceVulkan14Features` (versions appendix).
- Confirmed: Only one push-descriptor set layout per pipeline layout (VUID-VkPipelineLayoutCreateInfo-pSetLayouts-00293); `vkCmdPushDescriptorSet` and `vkCmdPushDescriptorSetWithTemplate` core names exist in vk.xml.
- Removed: Android driver support claim, descriptor-buffer incompatibility claim and command-buffer memory cost claim (no source found).

Method: documentation only; no commands were run.
