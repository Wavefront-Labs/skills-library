---
id: computing-software.computer-graphics-engineering.opengl.vulkan-performance-query-counters
name: vulkan-performance-query-counters
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-queries, performance-query, gpu-counters-vulkan, profiling-lock]
level: sme
status: docs-checked
description: "Read hardware performance counters in-app with VK_KHR_performance_query: enumerate counters, profiling lock, multi-pass queries and interpreting results."
sources: ["https://docs.vulkan.org/spec/latest/appendices/VK_KHR_performance_query.html", "https://docs.vulkan.org/spec/latest/chapters/queries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VK_KHR_performance_query

Lets an app read vendor hardware counters (busy %, cache hit rates, ALU utilisation) around
command buffer regions, for in-engine profiling overlays without external tools.

## 1. Enumerate counters per queue family
```c
uint32_t n = 0;
vkEnumeratePhysicalDeviceQueueFamilyPerformanceQueryCountersKHR(gpu, qfi, &n, NULL, NULL);
std::vector<VkPerformanceCounterKHR> ctr(n, { VK_STRUCTURE_TYPE_PERFORMANCE_COUNTER_KHR });
std::vector<VkPerformanceCounterDescriptionKHR> desc(n, { VK_STRUCTURE_TYPE_PERFORMANCE_COUNTER_DESCRIPTION_KHR });
vkEnumeratePhysicalDeviceQueueFamilyPerformanceQueryCountersKHR(gpu, qfi, &n, ctr.data(), desc.data());
// desc[i].name / category / description; ctr[i].unit (GENERIC, PERCENTAGE, NANOSECONDS, BYTES, ... CYCLES), scope, storage type
```

## 2. Passes
Hardware can only sample a few counters at once. Ask how many replays are needed:
```c
VkQueryPoolPerformanceCreateInfoKHR pci = { VK_STRUCTURE_TYPE_QUERY_POOL_PERFORMANCE_CREATE_INFO_KHR };
pci.queueFamilyIndex = qfi; pci.counterIndexCount = k; pci.pCounterIndices = chosen;
uint32_t passes; vkGetPhysicalDeviceQueueFamilyPerformanceQueryPassesKHR(gpu, &pci, &passes);
```
Each submission must be executed `passes` times, with `VkPerformanceQuerySubmitInfoKHR::counterPassIndex`
= 0..passes-1 (recorded commands identical). Choose counters that fit in one pass for live overlays; the `performanceCounterQueryPools` feature must be enabled.

## 3. Profiling lock
```c
VkAcquireProfilingLockInfoKHR li = { VK_STRUCTURE_TYPE_ACQUIRE_PROFILING_LOCK_INFO_KHR, NULL, 0, UINT64_MAX };
vkAcquireProfilingLockKHR(device, &li);       // before recording command buffers with perf queries
// ... record, submit, read ...
vkReleaseProfilingLockKHR(device);
```
The profiling lock must be held before `vkBeginCommandBuffer` is called on any command buffer that uses a performance query pool.

## 4. Query and read
`vkCmdBeginQuery(cmd, perfPool, 0, 0)` / `vkCmdEndQuery`, then `vkGetQueryPoolResults` (flags must not include `64_BIT`, `WITH_AVAILABILITY`, `WITH_STATUS` or `PARTIAL`; the pool must have been recorded once per pass) into an
array of `VkPerformanceCounterResultKHR` (a union: `int32/int64/uint32/uint64/float32/float64`
per the counter's storage type).

## Support
- Check `VK_KHR_performance_query` and the `performanceCounterQueryPools` feature per device and queue family; which counters exist is implementation-specific.
- Counter semantics are vendor-specific; read the description strings and vendor docs.

## Gotchas
- Follow the spec's profiling-lock rule: acquire before beginning command buffer recording, release after the work completes.
- Running multi-pass replays changes frame timing; use for analysis, not for timing measurements.

## Verify
- [ ] Overlay shows plausible counter values (e.g. GPU busy near 100% in a GPU-bound scene) on a supported driver.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (appendices/VK_KHR_performance_query.adoc, validusage.json, xml/vk.xml).
Confirmed: VkPerformanceCounterResultKHR union members; VkAcquireProfilingLockInfoKHR fields (flags, timeout); counter unit enums; profiling lock must be held before vkBeginCommandBuffer (VUID-vkCmdBeginQuery-queryPool-03223); counterPassIndex rule; vkGetQueryPoolResults restrictions for performance queries; performanceCounterQueryPools feature. Removed the vendor support list and vendor tool names.
Method: documentation only; no commands were run.
