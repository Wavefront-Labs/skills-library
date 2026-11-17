---
id: computing-software.computer-graphics-engineering.opengl.vulkan-events-and-split-barriers
name: vulkan-events-and-split-barriers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-synchronization, vk-events, vkcmdwaitevents2, split-barriers-vulkan]
level: advanced
status: docs-checked
description: "Use Vulkan events (vkCmdSetEvent2/vkCmdWaitEvents2) as split barriers to overlap independent work between a producer and consumer in one queue."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/xml/vk.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Events as split barriers

`vkCmdPipelineBarrier2` makes everything after it wait for everything before it (within the
stage masks). An event splits that into **signal** (after the producer) and **wait** (before the
consumer), so unrelated work recorded in between can run while the producer drains.

```c
// producer
vkCmdDispatch(cmd, ...);                          // writes lightGrid
VkMemoryBarrier2 mb = { VK_STRUCTURE_TYPE_MEMORY_BARRIER_2 };
mb.srcStageMask = VK_PIPELINE_STAGE_2_COMPUTE_SHADER_BIT;  mb.srcAccessMask = VK_ACCESS_2_SHADER_STORAGE_WRITE_BIT;
mb.dstStageMask = VK_PIPELINE_STAGE_2_FRAGMENT_SHADER_BIT; mb.dstAccessMask = VK_ACCESS_2_SHADER_STORAGE_READ_BIT;
VkDependencyInfo dep = { VK_STRUCTURE_TYPE_DEPENDENCY_INFO }; dep.memoryBarrierCount = 1; dep.pMemoryBarriers = &mb;
vkCmdSetEvent2(cmd, lightGridReady, &dep);

// independent work: shadow maps, depth prepass ...
renderShadows(cmd);

// consumer
vkCmdWaitEvents2(cmd, 1, &lightGridReady, &dep);   // MUST pass the same dependency info
renderLighting(cmd);
vkCmdResetEvent2(cmd, lightGridReady, VK_PIPELINE_STAGE_2_FRAGMENT_SHADER_BIT);  // before next set
```
With synchronization2, the `VkDependencyInfo` given to `vkCmdWaitEvents2` must be exactly equal to
the one given to `vkCmdSetEvent2` (VUID-vkCmdWaitEvents2-pEvents), so the barriers are known at signal time.

## When events help
- Long producer (compute pass) followed by unrelated graphics work, then a consumer.
- Image layout transitions can be split the same way (image barrier inside the dependency).
- Events must not be used to order commands submitted to different queues; use semaphores there.

## When they don't
- If the producer is short or there is no independent work between set and wait, there is no gain;
  measure with a GPU trace.
- `vkCmdSetEvent2` and `vkCmdResetEvent2` can only be recorded outside a render pass instance;
  `vkCmdWaitEvents2` is allowed inside but restricted, so keep events outside render passes.
- For an event signalled by `vkSetEvent`, the wait's barriers may only include host operations in
  their first scope; prefer timeline semaphores for host-to-GPU signalling.

## Gotchas
- An event must be reset before being set again; set/reset ordering is on the GPU timeline,
  so record reset after the wait.
- `VK_EVENT_CREATE_DEVICE_ONLY_BIT` (1.3) specifies that host event commands will not be used with the event.

## Verify
- [ ] GPU trace shows shadow work overlapping the tail of the compute pass; sync validation clean.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Events insert fine-grained dependencies between commands in the same queue (or host and queue) and must not be used across queues (events section).
- Confirmed: `vkCmdWaitEvents2` pDependencyInfos must be exactly equal to those given to `vkCmdSetEvent2`; `vkCmdResetEvent2` needs an execution dependency with earlier waits; per-command `renderpass` attribute in vk.xml: set and reset outside render pass, wait both.
- Confirmed: For events signalled by `vkSetEvent` the barriers may only include host operations in the first scope (VUID-vkCmdWaitEvents2-pEvents-03839).
- Removed the mobile-driver and TDR remarks (no source found).

Method: documentation only; no commands were run.
