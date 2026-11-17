---
id: computing-software.computer-graphics-engineering.opengl.vulkan-synchronization-validation-and-hazards
name: vulkan-synchronization-validation-and-hazards
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-synchronization, synchronization-validation, sync-hazards, validation-layers, vkconfig]
level: advanced
status: docs-checked
description: "Find Vulkan data races with Synchronization Validation: enabling it, reading RAW/WAR/WAW hazard reports, and fixing the barrier or semaphore at fault."
sources: ["https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/main/docs/syncval_usage.md", "https://docs.vulkan.org/guide/latest/extensions/VK_KHR_synchronization2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synchronisation validation and hazard debugging

**Goal:** catch missing or wrong barriers before they become vendor-specific flicker, using the
validation layer's synchronisation checks.

## 1. Enable
Enable the `VK_LAYER_KHRONOS_validation` layer and turn on its `validate_sync` setting:
- vkconfig (Vulkan Configurator): the "Synchronization Only" preset (it disables other validation checks), or
- `VK_EXT_layer_settings`: a `VkLayerSettingEXT` named `validate_sync` (bool) in `VkLayerSettingsCreateInfoEXT`, or
- environment: `VK_VALIDATION_VALIDATE_SYNC=1` (Android: `adb shell setprop debug.vulkan.khronos_validation.validate_sync 1`).
The full set of checks runs at `vkQueueSubmit`/`vkQueueSubmit2`, so hazards across command buffers and queues are caught; record-time reporting (on by default,
`syncval_record_time_validation`) reports a subset at the `vkCmd*` call.

## 2. Read the report
Messages look like `vkQueueSubmit(): WRITE_AFTER_WRITE hazard detected. vkCmdEndRenderPass (...) writes to resource, which was previously written by vkCmdClearColorImage (...)`,
followed by the stages and access types of the current synchronisation, and sometimes a "Vulkan insight" line. With `syncval_message_extra_properties`
the message adds structured fields:
- **hazard_type** (for example `WRITE_AFTER_WRITE`), **prior_access** (stage and access of the earlier operation), **write_barriers** (barriers applied to the prior write),
  **command** and **prior_command** (the two commands involved).
- RAW: a read after a write without waiting for it. WAW: two writes unordered (often a
  clear vs a draw, or a copy into an image still being written). WAR: a write after a read
  needs only an execution dependency. WRW and RRW are racing accesses from unsynchronised subpasses or queues.
Name objects with `vkSetDebugUtilsObjectNameEXT` so the message says "GBufferNormal" instead
of a handle.

## 3. Fix pattern
Add or correct the barrier with src stage/access covering the prior access and dst stage/access covering the access that conflicts:
```cpp
VkImageMemoryBarrier2 b{VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER_2};
b.srcStageMask = VK_PIPELINE_STAGE_2_COLOR_ATTACHMENT_OUTPUT_BIT;
b.srcAccessMask = VK_ACCESS_2_COLOR_ATTACHMENT_WRITE_BIT;
b.dstStageMask = VK_PIPELINE_STAGE_2_FRAGMENT_SHADER_BIT;
b.dstAccessMask = VK_ACCESS_2_SHADER_SAMPLED_READ_BIT;
b.oldLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
b.newLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
```
Hazards across submits mean a missing semaphore wait (wrong `pWaitDstStageMask`, e.g. waiting
at `FRAGMENT_SHADER` when the first use is a transfer or compute).

## Gotchas
- Syncval adds CPU overhead; run it regularly in development and CI on short test scenes (the layer docs recommend running it after core validation errors are fixed).
- `ALL_COMMANDS` + `MEMORY_READ|WRITE` barriers silence it but cost GPU overlap; fix with
  precise stages after the bug is found.
- Known limitations in the layer docs: memory aliasing hazards are not detected properly, indirect buffers and host accesses are not tracked, and descriptor accesses are not tracked precisely.

## Verify
- [ ] A full frame of the test scene produces zero SYNC-HAZARD messages.
- [ ] Toggling between GPU vendors shows no flicker that syncval did not predict.

## Checked
Checked 2026-10-26 against Vulkan-ValidationLayers docs/syncval_usage.md (main).
Confirmed: validate_sync setting, vkconfig preset, layer-settings and environment ways to enable it; submit-time and record-time reporting and the syncval_record_time_validation setting; message anatomy and extra-properties keys; hazard types (RAW, WAR, WAW, WRW, RRW) and the WAR execution-dependency rule; known limitations. Removed the VK_LAYER_ENABLES route, the syncval_submit_time_validation setting and the old usage/prior_usage message format, none of which the current document lists.
Method: documentation only; no commands were run.
