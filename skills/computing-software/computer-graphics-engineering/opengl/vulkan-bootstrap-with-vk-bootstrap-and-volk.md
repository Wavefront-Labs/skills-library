---
id: computing-software.computer-graphics-engineering.opengl.vulkan-bootstrap-with-vk-bootstrap-and-volk
name: vulkan-bootstrap-with-vk-bootstrap-and-volk
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-instance-device, vk-bootstrap, volk, function-loading, vkinstance]
level: practitioner
status: docs-checked
description: "Cut Vulkan setup boilerplate with vk-bootstrap (instance, device, queues, swapchain) and load entry points with volk for faster dispatch."
sources: ["https://github.com/charles-lunarg/vk-bootstrap", "https://github.com/zeux/volk"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootstrapping Vulkan with vk-bootstrap and volk

**Goal:** get a validated instance, a suitable physical/logical device, queues and a swapchain
in ~50 lines, with device-level function pointers loaded directly.

## 1. volk first
```cpp
#define VK_NO_PROTOTYPES          // or link with volk only, not vulkan-1
#include <volk.h>
VK_CHECK(volkInitialize());       // loads the Vulkan loader library at run time (no link-time dependency on vulkan-1)
```
After instance creation: `volkLoadInstance(instance)`; after device creation:
`volkLoadDevice(device)`. Device functions are then loaded directly from the driver, skipping loader dispatch (volk's README says this overhead
can be as high as 7% depending on the driver and application). With only `volkLoadInstance`, device calls go through loader dispatch, which supports
multiple `VkDevice` objects; for several devices with direct calls use `volkLoadDeviceTable`.

## 2. vk-bootstrap
```cpp
vkb::InstanceBuilder ib;
auto inst = ib.set_app_name("app").request_validation_layers(debug)
              .use_default_debug_messenger().require_api_version(1, 3, 0).build();
vkb::Instance vkbInst = inst.value();          // check inst.has_value(), inst.error().message()
volkLoadInstance(vkbInst.instance);
VkPhysicalDeviceVulkan13Features f13{VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_3_FEATURES};
f13.dynamicRendering = VK_TRUE; f13.synchronization2 = VK_TRUE;
vkb::PhysicalDeviceSelector sel{vkbInst};
auto phys = sel.set_minimum_version(1, 3).set_required_features_13(f13)
               .set_surface(surface).select().value();
vkb::Device dev = vkb::DeviceBuilder{phys}.build().value();
volkLoadDevice(dev.device);
VkQueue gfx = dev.get_queue(vkb::QueueType::graphics).value();
uint32_t gfxFamily = dev.get_queue_index(vkb::QueueType::graphics).value();
auto sc = vkb::SwapchainBuilder{dev}.set_desired_format({VK_FORMAT_B8G8R8A8_SRGB,
            VK_COLOR_SPACE_SRGB_NONLINEAR_KHR}).set_desired_present_mode(VK_PRESENT_MODE_FIFO_KHR)
            .set_desired_extent(w, h).build().value();
```
`SwapchainBuilder::set_old_swapchain(sc)` handles recreation.

## Gotchas
- vk-bootstrap only selects; it does not enable features you do not request. Chain every
  feature struct you use, or the validation layer reports use of a disabled feature.
- Tear-down order is yours: `vkb::destroy_swapchain`, `vkb::destroy_device`,
  `vkb::destroy_surface`, `vkb::destroy_instance`.
- If files include `vulkan/vulkan.h` without `volk.h`, symbol conflicts can occur (volk's README); define `VK_NO_PROTOTYPES` when compiling such code.
- Prefer a discrete GPU explicitly (`prefer_gpu_device_type`) on laptops with two GPUs.

## Verify
- [ ] Validation layer silent on startup; `vkGetPhysicalDeviceProperties` name is the
      intended GPU.
- [ ] Clearing the swapchain image to a colour presents correctly after resize.

## Checked
Checked 2026-10-26 against vk-bootstrap src/VkBootstrap.h and README (main) and volk volk.h and README (main).
Confirmed: InstanceBuilder (set_app_name, request_validation_layers, use_default_debug_messenger, require_api_version), PhysicalDeviceSelector (set_minimum_version, set_required_features_13, set_surface, prefer_gpu_device_type), DeviceBuilder, Device::get_queue and get_queue_index, QueueType, SwapchainBuilder setters including set_old_swapchain, vkb::destroy_* helpers, Result error() as std::error_code; volkInitialize, volkLoadInstance, volkLoadDevice, volkLoadDeviceTable and the VK_NO_PROTOTYPES advice. Removed the vkguide attribution and the MoltenVK loader claim.
Method: documentation only; no commands were run.
