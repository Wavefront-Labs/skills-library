---
id: computing-software.computer-graphics-engineering.opengl.vulkan-device-properties-and-limits
name: vulkan-device-properties-and-limits
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-device, vk-device-limits, physicaldeviceproperties, gpuinfo]
level: practitioner
status: docs-checked
description: "Query Vulkan device properties and limits with vkGetPhysicalDeviceProperties2 chains and learn which limits matter most, with the values the spec guarantees."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/devsandqueues.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan device properties and limits

## Query with pNext chains
```c
VkPhysicalDeviceVulkan13Properties p13 = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_3_PROPERTIES };
VkPhysicalDeviceVulkan12Properties p12 = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_2_PROPERTIES, &p13 };
VkPhysicalDeviceVulkan11Properties p11 = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_1_PROPERTIES, &p12 };
VkPhysicalDeviceProperties2 props = { VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2, &p11 };
vkGetPhysicalDeviceProperties2(gpu, &props);
const VkPhysicalDeviceLimits& L = props.properties.limits;
```
Extension properties (ray tracing, mesh shader, descriptor buffer) chain the same way.

## Limits that actually bite
| Limit | Spec guarantee | Consequence |
|---|---|---|
| `minUniformBufferOffsetAlignment` | at most 256 | dynamic UBO offsets / suballocation alignment |
| `minStorageBufferOffsetAlignment` | at most 256 | SSBO suballocation |
| `nonCoherentAtomSize` | at most 256 | flush/invalidate ranges must be multiples |
| `maxPushConstantsSize` | at least 128 (256 in the Vulkan 1.4 limits) | push constant block size |
| `maxBoundDescriptorSets` | at least 4 (7 in Roadmap 2024 and the Vulkan 1.4 limits) | set layout design |
| `maxPerStageDescriptorSamplers` etc. | at least 16 (64 in Roadmap 2022); the `UpdateAfterBind` variants have much larger minimums (500000 for several) | bindless feasibility (`maxPerStageDescriptorUpdateAfterBind*`) |
| `maxComputeWorkGroupInvocations` / `Size` / `Count` | at least 128 / (128,128,64) / 65535 per dimension (256 and (256,256,64) in Roadmap 2022 and the Vulkan 1.4 limits) | dispatch sizing |
| `maxComputeSharedMemorySize` | at least 16384 bytes (32768 in Roadmap 2026) | shared tile sizes |
| `timestampPeriod` | nanoseconds per tick (device-specific) | converting timestamp queries |
| `maxImageDimension2D` | at least 4096 (8192 in Roadmap 2022 and the Vulkan 1.4 limits) | atlas/render target sizes |
| `framebufferColorSampleCounts` & depth counts | include 1 and 4 samples | MSAA choice (intersect them) |
| `maxSamplerAnisotropy` | at least 16 when `samplerAnisotropy` is supported | clamp sampler anisotropy |
| `subgroupSize` (1.1 props) | a power of two (device-specific) | subgroup algorithms (use `subgroupSizeControl` for fixed size) |
| `maxMemoryAllocationCount` | at least 4096 | why you suballocate (VMA) |

## Practice
- Log the important limits and `driverVersion` (its encoding is vendor-specific) at startup; bug reports
  become actionable.
- Design to the minimums your target devices guarantee: the spec's required-limits table, or measured values from a device database.
- Assert at runtime that computed offsets respect alignment limits; validation catches some
  but not all (e.g. host-side `nonCoherentAtomSize` misuse corrupts silently).

## Gotchas
- `apiVersion` in properties is the device's maximum; the usable version is min(instance
  requested, device). Don't call 1.3 core functions on a 1.2 device.
- `deviceID` / `vendorID` identify hardware; never key behaviour on `deviceName` strings.

## Verify
- [ ] Startup log prints limits; app runs on a device at the spec minimum (e.g. via a profile/MoltenVK) without validation errors.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23), `chapters/limits.adoc` required-limits table. The old 'Typical' column mixed spec minimums with unsourced vendor values; it is now a 'Spec guarantee' column using the table: offset alignments and `nonCoherentAtomSize` have a required maximum of 256; `maxPushConstantsSize` min 128 (256 for Vulkan 1.4); `maxBoundDescriptorSets` min 4 (7 for Roadmap 2024 and Vulkan 1.4); `maxPerStageDescriptorSamplers` min 16 (64 for Roadmap 2022); update-after-bind variants min 500000; compute work group limits min 128 / (128,128,64) / 65535; `maxComputeSharedMemorySize` min 16384 (32768 for Roadmap 2026); `maxImageDimension2D` min 4096 (8192 for Roadmap 2022 and Vulkan 1.4); framebuffer color and depth sample counts include 1 and 4; `maxSamplerAnisotropy` min 16; `maxMemoryAllocationCount` min 4096. Removed the NVIDIA driverVersion bit layout and the gpuinfo filtering advice, which no checked document covers.

Method: documentation only; no commands were run.
