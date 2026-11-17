---
id: computing-software.computer-graphics-engineering.opengl.vulkan-descriptor-update-templates
name: vulkan-descriptor-update-templates
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-descriptors, descriptor-update-template, vkupdatedescriptorsetwithtemplate]
level: advanced
status: docs-checked
description: "Speed up Vulkan descriptor writes with update templates: map a C struct to bindings once, then update sets (or push descriptors) from that struct."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_descriptor_update_template.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/extensions/VK_KHR_descriptor_update_template.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Descriptor update templates (core 1.1)

`vkUpdateDescriptorSets` takes arrays of `VkWriteDescriptorSet` that the driver must parse every
call. A template pre-describes where each descriptor lives in *your* struct, so updates become
a single call with a pointer.

## Define the struct and template
```c
struct MaterialDescriptors {
    VkDescriptorBufferInfo params;          // binding 0: UBO
    VkDescriptorImageInfo  albedo;          // binding 1: combined image sampler
    VkDescriptorImageInfo  normal;          // binding 2
};
VkDescriptorUpdateTemplateEntry e[3] = {
  { 0, 0, 1, VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER,         offsetof(MaterialDescriptors, params), 0 },
  { 1, 0, 1, VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, offsetof(MaterialDescriptors, albedo), 0 },
  { 2, 0, 1, VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, offsetof(MaterialDescriptors, normal), 0 } };
// fields: dstBinding, dstArrayElement, descriptorCount, type, offset, stride (for arrays)
VkDescriptorUpdateTemplateCreateInfo ci = { VK_STRUCTURE_TYPE_DESCRIPTOR_UPDATE_TEMPLATE_CREATE_INFO };
ci.descriptorUpdateEntryCount = 3; ci.pDescriptorUpdateEntries = e;
ci.templateType = VK_DESCRIPTOR_UPDATE_TEMPLATE_TYPE_DESCRIPTOR_SET;
ci.descriptorSetLayout = materialSetLayout;
vkCreateDescriptorUpdateTemplate(dev, &ci, NULL, &tmpl);
```

## Update
```c
MaterialDescriptors d = { {ubo, off, sizeof(Params)},
                          {sampler, albedoView, VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL},
                          {sampler, normalView, VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL} };
vkUpdateDescriptorSetWithTemplate(dev, set, tmpl, &d);
```
For arrays, set `descriptorCount = N` and `stride = sizeof(element)` so entries can be
interleaved in an array of structs.

## With push descriptors
Create the template with `templateType = VK_DESCRIPTOR_UPDATE_TEMPLATE_TYPE_PUSH_DESCRIPTORS`,
`pipelineBindPoint` and `pipelineLayout` + `set`, then
`vkCmdPushDescriptorSetWithTemplate(cmd, tmpl, layout, set, &d)` (core in 1.4, `...KHR` with the
extension): per-draw descriptors without allocating sets at all.

## When it matters
- Engines updating many descriptor sets per frame (per-draw sets): templates avoid building and
  parsing `VkWriteDescriptorSet` arrays; measure the CPU saving.
- For bindless designs with few updates, templates are unnecessary.

## Gotchas
- The struct layout must match offsets exactly; use `offsetof` and static asserts.
- Image layout in `VkDescriptorImageInfo` must match the layout at use time (validation checks at draw).
- Template is tied to a set layout (or pipeline layout+set for push); create one per layout.

## Verify
- [ ] CPU profiler shows descriptor update cost reduced; validation clean.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: `VK_KHR_descriptor_update_template` is promoted to Vulkan 1.1 (vk.xml `promotedto`); `VkDescriptorUpdateTemplateEntry` members are `dstBinding`, `dstArrayElement`, `descriptorCount`, `descriptorType`, `offset`, `stride` in that order.
- Confirmed: `VK_DESCRIPTOR_UPDATE_TEMPLATE_TYPE_PUSH_DESCRIPTORS` and `vkCmdPushDescriptorSetWithTemplate` exist in vk.xml; the push variant is core in 1.4.
- Removed the unsourced vendor speed-up figure.

Method: documentation only; no commands were run.
