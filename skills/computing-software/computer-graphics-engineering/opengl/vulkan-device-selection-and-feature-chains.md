---
id: computing-software.computer-graphics-engineering.opengl.vulkan-device-selection-and-feature-chains
name: vulkan-device-selection-and-feature-chains
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-device, physical-device-selection, queue-families, vulkan-features, pnext-chain, vkphysicaldevicevulkan13features, device-extensions, logical-device]
level: practitioner
status: docs-checked
description: "Pick a Vulkan physical device, find graphics/present/compute/transfer queue families, and enable 1.2/1.3 features and extensions through pNext chains."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/devsandqueues.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/features.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan device selection and feature chains

**Goal:** choose the right GPU deterministically, get the queues you need, and enable
exactly the features your renderer depends on — failing early with a clear message if
missing.

## 1. Score physical devices
```cpp
uint32_t n; vkEnumeratePhysicalDevices(inst, &n, nullptr);
std::vector<VkPhysicalDevice> gpus(n); vkEnumeratePhysicalDevices(inst, &n, gpus.data());
for (auto g : gpus) {
    VkPhysicalDeviceProperties p; vkGetPhysicalDeviceProperties(g, &p);
    if (p.apiVersion < VK_API_VERSION_1_3) continue;
    if (!hasRequiredExtensions(g) || !hasRequiredFeatures(g) || !findQueues(g)) continue;
    int score = (p.deviceType == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) ? 1000 : 100;
    // tie-break on VRAM: sum DEVICE_LOCAL heaps from vkGetPhysicalDeviceMemoryProperties
}
```
Allow an override (`--gpu=N` / env var) — users with two GPUs need it.

## 2. Queue families
```cpp
vkGetPhysicalDeviceQueueFamilyProperties(g, &qn, props);
for (uint32_t i = 0; i < qn; ++i) {
    VkBool32 present; vkGetPhysicalDeviceSurfaceSupportKHR(g, i, surface, &present);
    if ((props[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) && present) gfx = i;
    if ((props[i].queueFlags & VK_QUEUE_COMPUTE_BIT) && !(props[i].queueFlags & VK_QUEUE_GRAPHICS_BIT)) asyncCompute = i;
    if ((props[i].queueFlags & VK_QUEUE_TRANSFER_BIT) && !(props[i].queueFlags & (VK_QUEUE_GRAPHICS_BIT|VK_QUEUE_COMPUTE_BIT))) transfer = i;
}
```
The spec guarantees at least one queue family that supports both graphics and compute, and a family reporting
graphics or compute supports transfer operations even if it does not report `VK_QUEUE_TRANSFER_BIT`. Dedicated
compute/transfer families are optional; fall back to the graphics family.

## 3. Query and enable features via pNext
```cpp
VkPhysicalDeviceVulkan13Features f13{VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_3_FEATURES};
VkPhysicalDeviceVulkan12Features f12{VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_2_FEATURES, &f13};
VkPhysicalDeviceFeatures2 f2{VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_FEATURES_2, &f12};
vkGetPhysicalDeviceFeatures2(g, &f2);                       // what the device supports
bool ok = f13.dynamicRendering && f13.synchronization2 && f12.bufferDeviceAddress
       && f12.descriptorIndexing && f12.timelineSemaphore;
// enable: build a NEW zeroed chain with only the features you need set to VK_TRUE
VkDeviceCreateInfo dci{VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO};
dci.pNext = &want2;            // VkPhysicalDeviceFeatures2 chain; pEnabledFeatures must be NULL
dci.enabledExtensionCount = (uint32_t)exts.size(); dci.ppEnabledExtensionNames = exts.data();
```
- Enabling everything the device reports can cost performance (e.g. `robustBufferAccess`).
- Extension features (e.g. `VkPhysicalDeviceMeshShaderFeaturesEXT`) chain the same way and
  require the extension in `ppEnabledExtensionNames`.
- Promoted extensions: on 1.3 use the core `dynamicRendering` feature (in `VkPhysicalDeviceVulkan13Features`); the
  `VK_KHR_dynamic_rendering` extension is only needed on devices below 1.3.

## 4. Check limits you depend on
`VkPhysicalDeviceProperties::limits`: `maxPushConstantsSize` (≥128),
`minUniformBufferOffsetAlignment`, `maxDescriptorSetSampledImages`, `timestampPeriod`,
`maxComputeWorkGroupSize`. Store them; never hard-code 256 alignment.

## Gotchas
- Integrated + discrete laptops: the surface may only be presentable from one; always check
  present support per family.
- `VkPhysicalDeviceFeatures2` in `pNext` and `pEnabledFeatures` together is invalid.
- The instance's API version and each physical device's `apiVersion` are independent; check the device's value.
- Each (`queueFamilyIndex`, `flags`) combination may appear only once in `pQueueCreateInfos`; merge entries and raise `queueCount`.

## Verify
- [ ] Startup log lists selected GPU, driver version, queue family indices and enabled features.
- [ ] Running on a device missing a required feature exits with a named feature, not a crash.
- [ ] Validation layers report no feature-not-enabled errors.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23); vk.xml for promotion data. Confirmed: at least one queue family must support both graphics and compute, and the transfer bit is optional to report for graphics or compute families (the skill claimed graphics families 'always support compute'); `pEnabledFeatures` must be NULL when `VkPhysicalDeviceFeatures2` is chained (VUID-VkDeviceCreateInfo-pNext-00373); the (`queueFamilyIndex`, `flags`) pair must be unique in `pQueueCreateInfos` (VUID-VkDeviceCreateInfo-queueFamilyIndex-02802; the old text said any repeated family index is invalid); features.adoc notes that some features such as `robustBufferAccess` may cost performance; `VK_KHR_dynamic_rendering` is promoted to Vulkan 1.3. Removed the unsourced claim about old drivers reporting different instance and device versions.

Method: documentation only; no commands were run.
