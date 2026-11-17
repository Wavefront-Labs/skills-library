---
id: computing-software.computer-graphics-engineering.opengl.vulkan-moltenvk-and-portability-subset
name: vulkan-moltenvk-and-portability-subset
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-instance, moltenvk, portability-subset, macos-vulkan]
level: advanced
status: docs-checked
description: "Run Vulkan on macOS/iOS via MoltenVK: portability enumeration flags, VK_KHR_portability_subset limits, config env vars, and Metal-mapping gotchas."
sources: ["https://github.com/KhronosGroup/MoltenVK/blob/main/Docs/MoltenVK_Runtime_UserGuide.md", "https://github.com/KhronosGroup/MoltenVK/blob/main/Docs/MoltenVK_Configuration_Parameters.md", "https://docs.vulkan.org/spec/latest/appendices/VK_KHR_portability_subset.html", "https://docs.vulkan.org/spec/latest/appendices/VK_KHR_portability_enumeration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MoltenVK and the portability subset

MoltenVK translates Vulkan to Metal. It is a *non-conformant* "portability" implementation, so
the loader hides it unless you opt in.

## Instance creation
```c
const char* exts[] = { VK_KHR_SURFACE_EXTENSION_NAME, VK_EXT_METAL_SURFACE_EXTENSION_NAME,
                       VK_KHR_PORTABILITY_ENUMERATION_EXTENSION_NAME,
                       VK_KHR_GET_PHYSICAL_DEVICE_PROPERTIES_2_EXTENSION_NAME };
VkInstanceCreateInfo ci = { VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO };
ci.flags = VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR;      // without it: no devices / INCOMPATIBLE_DRIVER
ci.enabledExtensionCount = 4; ci.ppEnabledExtensionNames = exts;
```
## Device creation
If the device lists `VK_KHR_portability_subset`, you **must** enable it, and query
`VkPhysicalDevicePortabilitySubsetFeaturesKHR` to learn what is missing.

| Portability feature (false = unsupported) | Impact |
|---|---|
| `triangleFans` | convert fans to lists |
| `separateStencilMaskRef` | same front/back stencil ref/mask |
| `imageViewFormatSwizzle` | component swizzles in image views |
| `events` | when false, `vkCreateEvent` must not be used (`VUID-vkCreateEvent-events-04468`) |
| `pointPolygons`, `samplerMipLodBias` | fill mode point, sampler mip bias |
| `vertexAttributeAccessBeyondStride` | attribute offsets must fit inside stride |
| `shaderSampleRateInterpolationFunctions` | `interpolateAtSample` etc. |

## Configuration
MoltenVK settings come from the standard `VK_EXT_layer_settings` extension or runtime environment variables (see MoltenVK_Configuration_Parameters.md):
- `MVK_CONFIG_USE_METAL_ARGUMENT_BUFFERS` (default 1): uses Metal argument buffers for descriptor-set resources where supported; the docs say this dramatically increases the number of bindable buffers, textures and samplers.
- `MVK_CONFIG_LOG_LEVEL` (default 3 = errors, warnings and info; 4 adds debug messages).
- `MVK_CONFIG_SYNCHRONOUS_QUEUE_SUBMITS` (default 1): when on, `vkQueueSubmit` and `vkQueuePresentKHR` are processed on the calling thread; when off, they are dispatched to a GCD queue.
- `MVK_CONFIG_SHADER_CONVERSION_FLIP_VERTEX_Y` (default 1): flips Y in converted vertex shaders; the alternative is a negative-height viewport, in which case you can disable it.

## Gotchas
- MoltenVK converts SPIR-V shaders to MSL automatically (the shader conversion is done with SPIRV-Cross); expect conversion cost on first use of a pipeline and use pipeline caches. The docs mention the MSL source can be retained for export in a pipeline cache.
- The supported-extension list in the MoltenVK Runtime User Guide is the authority on what is available; check it for geometry, tessellation and transform feedback before relying on them.
- Install options: static or dynamic universal `XCFramework`, or on macOS a dynamic library (`libMoltenVK.dylib`). The guide says MoltenVK uses only public Apple APIs unless configured otherwise at build time, so apps remain compatible with standard distribution channels including the App Store.
- Metal's own limits apply; the guide lists, for example, `VK_EXT_descriptor_indexing` limited to Metal Tier 1 (96/128 textures, 16 samplers) in some configurations.

## Verify
- [ ] `vulkaninfo` on the Mac shows the device with `VK_KHR_portability_subset`; app runs with validation layers clean and MoltenVK log free of "not supported" errors.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (appendices/VK_KHR_portability_subset.adoc, VK_KHR_portability_enumeration.adoc, chapters/initialization.adoc, validusage.json, xml/vk.xml) and the MoltenVK docs on main (MoltenVK_Runtime_UserGuide.md, MoltenVK_Configuration_Parameters.md).
Confirmed: ENUMERATE_PORTABILITY_BIT_KHR needs VK_KHR_portability_enumeration enabled; portability_subset must be enabled when the device lists it (VUID-VkDeviceCreateInfo-pProperties-04451); the portability feature names in the table; events rule; configuration parameter defaults and meanings; supported-extension list and install options. Removed the Metal 31/128 limits, geometry/tessellation/transform-feedback statement and the iOS static-only claim, which the docs do not support.
Method: documentation only; no commands were run.
