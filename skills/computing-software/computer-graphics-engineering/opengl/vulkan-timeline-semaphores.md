---
id: computing-software.computer-graphics-engineering.opengl.vulkan-timeline-semaphores
name: vulkan-timeline-semaphores
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-synchronization, timeline-semaphores, vksemaphoresubmitinfo, vkwaitsemaphores, vkgetsemaphorecountervalue, cross-queue-sync, gpu-cpu-sync]
level: advanced
status: docs-checked
description: "Replace fence and binary-semaphore juggling with Vulkan timeline semaphores: monotonically increasing values for frame pacing, cross-queue dependencies and CPU polling."
sources: ["https://docs.vulkan.org/spec/latest/chapters/synchronization.html#synchronization-semaphores", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/VK_KHR_surface/wsi.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan timeline semaphores

**Goal:** one semaphore per queue whose 64-bit counter expresses "work up to point N is
done", usable by GPU waits, CPU waits and CPU polls (core in Vulkan 1.2).

## 1. Create
```cpp
VkSemaphoreTypeCreateInfo t{VK_STRUCTURE_TYPE_SEMAPHORE_TYPE_CREATE_INFO};
t.semaphoreType = VK_SEMAPHORE_TYPE_TIMELINE; t.initialValue = 0;
VkSemaphoreCreateInfo ci{VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO, &t};
vkCreateSemaphore(dev, &ci, nullptr, &gfxTimeline);
```
Requires the `timelineSemaphore` feature (Vulkan12Features).

## 2. Signal and wait on submit (sync2)
```cpp
uint64_t v = ++gfxValue;                                   // frame N's value
VkSemaphoreSubmitInfo wait{VK_STRUCTURE_TYPE_SEMAPHORE_SUBMIT_INFO};
wait.semaphore = uploadTimeline; wait.value = uploadReadyValue;
wait.stageMask = VK_PIPELINE_STAGE_2_VERTEX_INPUT_BIT | VK_PIPELINE_STAGE_2_FRAGMENT_SHADER_BIT;
VkSemaphoreSubmitInfo sig{VK_STRUCTURE_TYPE_SEMAPHORE_SUBMIT_INFO};
sig.semaphore = gfxTimeline; sig.value = v; sig.stageMask = VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT;
// VkSubmitInfo2: pWaitSemaphoreInfos = &wait, pSignalSemaphoreInfos = &sig
```

## 3. Frames in flight without fences
```cpp
// before reusing frame slot i (last used with value frameValue[i]):
VkSemaphoreWaitInfo wi{VK_STRUCTURE_TYPE_SEMAPHORE_WAIT_INFO};
wi.semaphoreCount = 1; wi.pSemaphores = &gfxTimeline; wi.pValues = &frameValue[i];
vkWaitSemaphores(dev, &wi, UINT64_MAX);
```
Resource lifetime becomes trivial: tag each deferred deletion with the current value and
free it once `vkGetSemaphoreCounterValue(dev, gfxTimeline, &done)` reports `done >= tag`.

## 4. Cross-queue pipelines
Async compute / transfer queues each own a timeline. Graphics waits on
`computeTimeline >= N` at the stage that consumes the data. Values let you express
"wait for the upload batch 37" without allocating a semaphore per dependency.

## 5. Host signalling
`vkSignalSemaphore` lets the CPU release GPU work (e.g. a submission waiting for an
asset decoder thread) — submit early, signal when data is ready.

## Gotchas
- **Swapchain acquire/present still require binary semaphores** (`vkAcquireNextImageKHR`,
  `vkQueuePresentKHR` don't accept timelines). Mix: binary for WSI, timeline for everything else.
- Values must strictly increase per signal; signalling a value ≤ current is invalid.
- A timeline wait completes only when the counter reaches its value, so make sure some signal
  will reach it.

## Verify
- [ ] Frame loop uses `vkWaitSemaphores` and per-slot values; no per-frame fences needed.
- [ ] Deferred-deletion queue frees resources only after the counter passes their tag.
- [ ] Sync validation reports no hazards between compute and graphics queues.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Timeline semaphores are core in 1.2 (`VK_KHR_timeline_semaphore` promotedto 1.2); feature `timelineSemaphore` is in `VkPhysicalDeviceVulkan12Features`.
- Confirmed: A timeline semaphore has a strictly increasing 64-bit counter; `vkSignalSemaphore` value must be greater than the current value (VUID-VkSemaphoreSignalInfo-value-03258).
- Confirmed: Acquire and present require binary semaphores (WSI valid usage). `vkWaitSemaphores`, `vkGetSemaphoreCounterValue`, `vkSignalSemaphore` and `VkSemaphoreSubmitInfo` exist in vk.xml.

Method: documentation only; no commands were run.
