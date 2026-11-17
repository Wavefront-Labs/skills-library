---
id: computing-software.computer-graphics-engineering.opengl.vulkan-device-lost-handling-and-crash-diagnostics
name: vulkan-device-lost-handling-and-crash-diagnostics
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-device, vk-device-lost, device-fault, gpu-crash]
level: sme
status: docs-checked
description: "Handle VK_ERROR_DEVICE_LOST: find the faulting work with VK_EXT_device_fault, checkpoints and buffer markers, and recover or exit cleanly."
sources: ["https://docs.vulkan.org/spec/latest/appendices/VK_EXT_device_fault.html", "https://docs.vulkan.org/spec/latest/appendices/VK_AMD_buffer_marker.html", "https://docs.vulkan.org/spec/latest/appendices/VK_NV_device_diagnostic_checkpoints.html", "https://docs.vulkan.org/spec/latest/chapters/devsandqueues.html#devsandqueues-lost-device"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VK_ERROR_DEVICE_LOST

Device loss means the GPU hung or faulted (page fault, timeout/TDR, driver reset). After it,
commands that can fail may return `VK_ERROR_DEVICE_LOST`. The lost state cannot be reset, but the spec
still allows any command to be called: child objects must be destroyed before the device, and waits
(`vkDeviceWaitIdle`, `vkQueueWaitIdle`, `vkWaitForFences`) return in finite time with `VK_SUCCESS` or
`VK_ERROR_DEVICE_LOST`. Create a new `VkDevice` to continue.

## Typical root causes
1. Use-after-free: destroying buffers/images/descriptor sets still referenced by in-flight
   command buffers (missing frames-in-flight fence waits).
2. Out-of-bounds access in shaders (bindless index past the array, unbounded SSBO writes)
   without `robustBufferAccess`.
3. Infinite loops / very long dispatches (the OS or driver watchdog resets the GPU).
4. Missing barriers causing reads of garbage indirect args (huge draw counts).
5. Driver bugs (last; prove with minimal repro).

## Gather evidence
**VK_EXT_device_fault (cross-vendor; enable the `deviceFault` feature; the newer `VK_KHR_device_fault` offers `vkGetDeviceFaultReportsKHR` and `vkGetDeviceFaultDebugInfoKHR`):**
```c
VkDeviceFaultCountsEXT counts = { VK_STRUCTURE_TYPE_DEVICE_FAULT_COUNTS_EXT };
vkGetDeviceFaultInfoEXT(device, &counts, NULL);
std::vector<VkDeviceFaultAddressInfoEXT> addrs(counts.addressInfoCount);
std::vector<VkDeviceFaultVendorInfoEXT> vend(counts.vendorInfoCount);
VkDeviceFaultInfoEXT info = { VK_STRUCTURE_TYPE_DEVICE_FAULT_INFO_EXT };
info.pAddressInfos = addrs.data(); info.pVendorInfos = vend.data();
vkGetDeviceFaultInfoEXT(device, &counts, &info);   // faulting VA + description
```
Map the faulting address back to a resource by logging buffer device addresses / VMA
allocations at creation time.

**Breadcrumbs:** write markers before/after each pass:
`vkCmdWriteBufferMarker2AMD(cmd, VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT, markerBuf, offset, passId)`
into host-visible memory, or `vkCmdSetCheckpointNV` + `vkGetQueueCheckpointData2NV` on NVIDIA.
After the loss, the last completed marker tells you which pass hung.

**Vendor tools:** NVIDIA and AMD publish their own GPU crash-dump tools; see the vendor documentation.

## Reproduce with validation
Run with validation + GPU-assisted validation (out-of-bounds descriptor indexing, buffer device
address checks) and synchronisation validation. Most device-lost bugs show up as validation
errors earlier in the frame.

## Recovery policy
- Games: destroy device and all resources, recreate from scratch, reload assets; show a message
  if it repeats.
- Tools: save user data first (CPU side), then attempt recreate.
- Always log driver version, GPU, last markers and fault info to a crash report.

## Gotchas
- `robustBufferAccess2`/`robustImageAccess2` (VK_EXT_robustness2) make out-of-bounds reads return zero, masking bugs; enable in
  release as a safety net only if the cost is acceptable, keep off in debug.
- Long compute jobs: split into chunks well under the OS watchdog timeout; don't change watchdog settings on
  users' machines.

## Verify
- [ ] Forced hang test (infinite loop shader behind a debug key) produces a report naming the pass and recovers or exits cleanly.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/devsandqueues.adoc lost-device section, appendices/VK_EXT_device_fault.adoc, VK_EXT_robustness2.adoc, validusage.json, xml/vk.xml).
Confirmed: lost-device behaviour and finite-time waits; vkGetDeviceFaultInfoEXT two-call pattern and VkDeviceFaultCountsEXT / VkDeviceFaultInfoEXT members; deviceFault feature; VK_KHR_device_fault commands; robustness2 zero-read behaviour; existence of vkCmdWriteBufferMarker2AMD, vkCmdSetCheckpointNV and vkGetQueueCheckpointData2NV in vk.xml. Removed the Windows TDR figure and vendor tool claims.
Method: documentation only; no commands were run.
