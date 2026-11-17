---
id: computing-software.computer-graphics-engineering.opengl.vulkan-timestamp-queries-and-debug-labels
name: vulkan-timestamp-queries-and-debug-labels
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-queries, vulkan-debugging, timestamp-queries, debug-labels, object-names, vkcmdwritetimestamp2, timestampperiod, vkcmdbegindebugutilslabelext, gpu-profiling]
level: practitioner
status: docs-checked
description: "Build a Vulkan GPU pass timer with timestamp query pools read back frames later, and label passes and objects with debug utils so captures and profilers are readable."
sources: ["https://docs.vulkan.org/spec/latest/chapters/queries.html#queries-timestamps", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/queries.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/devsandqueues.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_calibrated_timestamps.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan timestamp queries and debug labels

**Goal:** an always-on per-pass GPU timing overlay, and RenderDoc/Nsight captures where
every pass and resource has a human name.

## 1. Timestamp pool per frame in flight
```cpp
VkQueryPoolCreateInfo qi{VK_STRUCTURE_TYPE_QUERY_POOL_CREATE_INFO};
qi.queryType = VK_QUERY_TYPE_TIMESTAMP; qi.queryCount = 2 * MAX_PASSES;
vkCreateQueryPool(dev, &qi, nullptr, &frame.tsPool);
// recording:
vkCmdResetQueryPool(cmd, frame.tsPool, 0, 2 * MAX_PASSES);           // or vkResetQueryPool on host (1.2)
vkCmdWriteTimestamp2(cmd, VK_PIPELINE_STAGE_2_TOP_OF_PIPE_BIT,    frame.tsPool, 2*p);
  ... pass p ...
vkCmdWriteTimestamp2(cmd, VK_PIPELINE_STAGE_2_BOTTOM_OF_PIPE_BIT, frame.tsPool, 2*p + 1);
```
Read after that frame's fence/timeline signals (never wait on queries in the same frame):
```cpp
uint64_t ts[2 * MAX_PASSES];
vkGetQueryPoolResults(dev, frame.tsPool, 0, 2*n, sizeof ts, ts, sizeof(uint64_t), VK_QUERY_RESULT_64_BIT);
double ms = (ts[2*p+1] - ts[2*p]) * props.limits.timestampPeriod / 1e6;   // period is ns per tick
```
- Check `queueFamilyProperties.timestampValidBits` (0 = unsupported on that queue) and
  `limits.timestampComputeAndGraphics`.
- Only `timestampValidBits` bits of a timestamp are meaningful: mask both values before subtracting
  if fewer than 64 are valid.
- `vkCmdWriteTimestamp2` takes a single pipeline stage; the implementation may write the timestamp
  at any logically later stage.
- `VK_KHR_calibrated_timestamps` (promoted from `VK_EXT_calibrated_timestamps`) correlates GPU ticks
  with CPU clocks for a combined timeline.

## 2. Pass labels
```cpp
VkDebugUtilsLabelEXT l{VK_STRUCTURE_TYPE_DEBUG_UTILS_LABEL_EXT}; l.pLabelName = "GBuffer";
l.color[0] = 0.2f; l.color[1] = 0.6f; l.color[2] = 1.0f; l.color[3] = 1.0f;
vkCmdBeginDebugUtilsLabelEXT(cmd, &l);  ...  vkCmdEndDebugUtilsLabelEXT(cmd);
```
Wrap in an RAII `GpuScope` that also writes the two timestamps — one macro gives both a
timing entry and a capture marker.

## 3. Object names
```cpp
VkDebugUtilsObjectNameInfoEXT n{VK_STRUCTURE_TYPE_DEBUG_UTILS_OBJECT_NAME_INFO_EXT};
n.objectType = VK_OBJECT_TYPE_IMAGE; n.objectHandle = (uint64_t)img; n.pObjectName = "HDR.color";
vkSetDebugUtilsObjectNameEXT(dev, &n);
```
Names show in validation messages, RenderDoc, Nsight, RGP. Name images, buffers, pipelines,
command buffers, queues and semaphores.

## Gotchas
- Debug utils functions are instance-level extension entry points: load them, and make the
  calls no-ops when the extension is absent (release, some Android devices).
- Resetting a query that the GPU is still writing (previous use of this frame slot) is
  invalid — per-frame pools solve it.

## Verify
- [ ] Overlay pass times sum close to total GPU frame time from an external tool.
- [ ] No CPU stall in `vkGetQueryPoolResults` (results read 2+ frames late).
- [ ] A capture tool shows nested pass labels and named resources.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: `timestampPeriod` is nanoseconds per tick; timestamps need a queue family with non-zero `timestampValidBits` (the number of meaningful bits); `vkCmdWriteTimestamp2` needs synchronization2, a single stage, a TIMESTAMP pool and an unavailable query.
- Confirmed: `VK_EXT_debug_utils` is an instance extension (vk.xml `type`); `VK_EXT_calibrated_timestamps` is promoted to `VK_KHR_calibrated_timestamps`. Core names `vkCmdWriteTimestamp2`, `vkResetQueryPool` exist.
- Removed tile-GPU and power-state remarks (no source found).

Method: documentation only; no commands were run.
