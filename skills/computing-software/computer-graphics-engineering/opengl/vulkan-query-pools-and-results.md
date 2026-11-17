---
id: computing-software.computer-graphics-engineering.opengl.vulkan-query-pools-and-results
name: vulkan-query-pools-and-results
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-queries, query-pool, vkgetquerypoolresults, host-query-reset]
level: practitioner
status: docs-checked
description: "Manage Vulkan query pools: reset rules (vkCmdResetQueryPool vs hostQueryReset), result flags (64-bit, WAIT, WITH_AVAILABILITY), copying results to buffers."
sources: ["https://docs.vulkan.org/spec/latest/chapters/queries.html", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/queries.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query pools and results

## Pool per frame in flight
```c
VkQueryPoolCreateInfo qp = { VK_STRUCTURE_TYPE_QUERY_POOL_CREATE_INFO };
qp.queryType = VK_QUERY_TYPE_TIMESTAMP;      // OCCLUSION, PIPELINE_STATISTICS, ...
qp.queryCount = 128;
for (int f = 0; f < FRAMES; ++f) vkCreateQueryPool(dev, &qp, NULL, &pools[f]);
```
A query must be **reset** before each use, and you must not reuse it until its result has been read.

## Resetting
- `vkCmdResetQueryPool(cmd, pool, 0, count)` recorded **outside** any render pass, before the
  queries are written (start of the frame's command buffer).
- `vkResetQueryPool(dev, pool, 0, count)` on the host (core 1.2, feature `hostQueryReset`):
  simpler, no command needed; call after the frame fence signalled and before recording.
- Every query a command writes must be unavailable (reset) first; `vkCmdResetQueryPool` and
  `vkCmdCopyQueryPoolResults` must be recorded outside a render pass instance.

## Reading
```c
uint64_t data[2 * N];   // value + availability per query
VkResult r = vkGetQueryPoolResults(dev, pools[f], 0, N, sizeof(data), data, 2 * sizeof(uint64_t),
    VK_QUERY_RESULT_64_BIT | VK_QUERY_RESULT_WITH_AVAILABILITY_BIT);
// r == VK_NOT_READY if any not available; check data[2*i+1] != 0 per query
```
| Flag | Effect |
|---|---|
| `64_BIT` | request 64-bit results (use for timestamps) |
| `WAIT_BIT` | block until available (stall: only after the frame fence) |
| `WITH_AVAILABILITY_BIT` | appends availability word per query |
| `PARTIAL_BIT` | occlusion: return partial values if not ready |

Read frame N's pool after frame N's fence signals (i.e., at the start of frame N+FRAMES), so
results are ready and no stall happens.

## GPU-side results
`vkCmdCopyQueryPoolResults(cmd, pool, first, count, buffer, offset, stride, flags)` writes
results into a buffer for GPU consumption (e.g. occlusion-driven decisions, or a persistent
readback buffer). Barrier: src stage `COPY`, dst whatever reads it.

## Gotchas
- With multiview in the subpass, a query uses N consecutive query indices (N = bits set in the view
  mask) and must begin and end in the same subpass.
- Timestamp support: `timestampValidBits` of the queue family must be non-zero (zero means
  timestamps are unsupported on that family).
- Pipeline statistics need feature `pipelineStatisticsQuery` and the `pipelineStatistics` mask at pool creation.

## Verify
- [ ] No validation "query not reset" errors; results read without `WAIT_BIT` stalls (CPU profiler).

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: `vkResetQueryPool` requires the `hostQueryReset` feature (`VkPhysicalDeviceVulkan12Features`) and previously submitted commands using the range must have completed (VUID-vkResetQueryPool-firstQuery-02741); command attributes in vk.xml: `vkCmdResetQueryPool` and `vkCmdCopyQueryPoolResults` outside a render pass.
- Confirmed: `vkGetQueryPoolResults` success codes are `VK_SUCCESS` and `VK_NOT_READY`; multiview queries use N consecutive indices and must not span subpasses; `pipelineStatisticsQuery` is required for pipeline statistics pools; timestamps need a non-zero `timestampValidBits`.
- Removed the unsourced 'garbage on some drivers' and occlusion-span remarks.

Method: documentation only; no commands were run.
