---
id: computing-software.computer-graphics-engineering.opengl.vulkan-api-version-and-promoted-extensions
name: vulkan-api-version-and-promoted-extensions
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-instance, vk-api-version, promoted-extensions, vulkan-1-3]
level: advanced
status: docs-checked
description: "Negotiate Vulkan instance/device API versions and handle extensions promoted to core (1.1-1.4): which names to enable, feature structs and fallbacks."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/versions.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/initialization.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/extensions.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/xml/vk.xml", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/versions.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API version negotiation and promoted extensions

## Three different versions
1. **Loader/instance version:** `vkEnumerateInstanceVersion` (absent = 1.0 loader).
2. **`VkApplicationInfo::apiVersion`:** the highest version your app *uses*. Since 1.1 it is
   not an error if the device supports less; you just may not use more than the device does.
3. **Device version:** `VkPhysicalDeviceProperties::apiVersion`.
Check the device version before using core functions newer than the device supports.

## Promotion rules
When an extension is promoted to core:
- Its functions exist without the suffix (`vkCmdBeginRendering` vs `vkCmdBeginRenderingKHR`),
  structs/enums lose the suffix but keep the same values.
- You need not enable the extension name on a device that supports the core version, but you
  still must enable the *feature* (`VkPhysicalDeviceVulkan13Features::dynamicRendering = VK_TRUE`).
- Some promotions made parts optional (e.g. 1.2 descriptor indexing features are optional bits).

| Version | Key promotions |
|---|---|
| 1.1 | multiview, 16-bit storage, sampler YCbCr, descriptor update templates, shader draw parameters, device groups, external memory/semaphore/fence, maintenance1-3, get_physical_device_properties2 (subgroup operations are new core 1.1 functionality) |
| 1.2 | timeline semaphores, descriptor indexing (optional), buffer device address, draw indirect count, scalar block layout, 8-bit storage, imageless framebuffer, host query reset, separate depth/stencil layouts, depth/stencil resolve, create_renderpass2 |
| 1.3 | dynamic rendering, synchronization2, maintenance4, extended dynamic state (1 in full, 2 except patch control points and logic op), pipeline creation cache control, inline uniform blocks, shader integer dot product, subgroup size control |
| 1.4 | push descriptors, dynamic rendering local read, maintenance5/6, line rasterization, host image copy (optional), index type uint8, raised minimum limits |

## Writing version-tolerant code
```c
bool has13 = deviceApi >= VK_API_VERSION_1_3;
if (!has13) {
    if (!hasExt("VK_KHR_dynamic_rendering")) fail("need dynamic rendering");
    enable("VK_KHR_dynamic_rendering"); enable("VK_KHR_depth_stencil_resolve"); // dependency
    chain(VkPhysicalDeviceDynamicRenderingFeaturesKHR{.dynamicRendering = VK_TRUE});
} else chain13.dynamicRendering = VK_TRUE;
```
Load functions through `vkGetDeviceProcAddr` (or a loader library such as volk).

## Gotchas
- Enabling an extension name that is core on that device is generally allowed but redundant
  (exception: `VK_EXT_buffer_device_address` with the 1.2 `bufferDeviceAddress` feature); enabling one
  the device doesn't list fails `vkCreateDevice` with `VK_ERROR_EXTENSION_NOT_PRESENT`.
- Mixing `VkPhysicalDeviceVulkan12Features` with the individual promoted feature structs (e.g.
  `VkPhysicalDeviceTimelineSemaphoreFeatures`) in the same chain is a validation error.

## Verify
- [ ] App starts on a device reporting the lowest supported version (test with a profile layer) without missing-function crashes.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Promotion lists computed from vk.xml `promotedto` attributes for 1.1 to 1.4 (including `VK_KHR_maintenance1-3` in 1.1, `EXT_host_query_reset` and `KHR_separate_depth_stencil_layouts` in 1.2, `KHR_maintenance4` in 1.3, `KHR_push_descriptor`, `EXT_host_image_copy`, `KHR_maintenance5/6`, `KHR_line_rasterization`, `KHR_index_type_uint8` in 1.4); 1.4 raised limits and optional host image copy from the versions appendix.
- Confirmed: 1.3 promotes extended dynamic state 1 in full and extended dynamic state 2 except patch control points and logic op (versions appendix). `VkApplicationInfo::apiVersion` is the highest version the app is designed to use and 1.1+ implementations must not return `VK_ERROR_INCOMPATIBLE_DRIVER` for it (initialization chapter).
- Confirmed: VkPhysicalDeviceVulkan12Features must not be chained together with individual promoted 1.2 feature structs such as `VkPhysicalDeviceTimelineSemaphoreFeatures` (VUID-VkDeviceCreateInfo-pNext-02830); `vkCreateDevice` returns `VK_ERROR_EXTENSION_NOT_PRESENT` for unsupported extensions; `VK_KHR_dynamic_rendering` depends on `VK_KHR_depth_stencil_resolve` (vk.xml).
- Removed the min() version formula wording and the Android Baseline remark (no source found).

Method: documentation only; no commands were run.
