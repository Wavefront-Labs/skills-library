---
id: computing-software.computer-graphics-engineering.opengl.vulkan-binary-semaphores
name: vulkan-binary-semaphores
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-synchronization, binary-semaphores, wait-stage-mask, acquire-semaphore]
level: practitioner
status: docs-checked
description: "Use Vulkan binary semaphores correctly for acquire/present and queue-to-queue sync: signal/wait pairing, wait stage masks, and reuse rules."
sources: ["https://docs.vulkan.org/spec/latest/chapters/synchronization.html#synchronization-semaphores", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/VK_KHR_surface/wsi.adoc", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/swapchain_semaphore_reuse.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary semaphores

A binary semaphore is GPU-to-GPU: signalled by one queue operation, waited on by exactly one
later queue operation, which unsignals it. Fences are GPU-to-CPU; timeline semaphores are the
general-purpose replacement for both except at the swapchain: `vkAcquireNextImageKHR` and
`vkQueuePresentKHR` require binary semaphores.

## Rules
1. **Every signal must be followed by exactly one wait** before the semaphore is signalled again.
   Signalling an already signalled binary semaphore is invalid.
2. A wait must have a signal that has already been *submitted* (no wait-before-signal for binary;
   timelines allow it).
3. You may only reuse (re-signal) a semaphore once the wait that consumed it has completed
   (known via a fence on that submission or a later timeline value).

## Frame loop with correct masks
```c
vkAcquireNextImageKHR(dev, swapchain, UINT64_MAX, imageAvailable[frame], VK_NULL_HANDLE, &img);

VkSemaphoreSubmitInfo wait = { VK_STRUCTURE_TYPE_SEMAPHORE_SUBMIT_INFO };
wait.semaphore = imageAvailable[frame];
wait.stageMask = VK_PIPELINE_STAGE_2_COLOR_ATTACHMENT_OUTPUT_BIT;   // only colour writes wait
VkSemaphoreSubmitInfo signal = { VK_STRUCTURE_TYPE_SEMAPHORE_SUBMIT_INFO };
signal.semaphore = renderDone[img];                                  // per swapchain IMAGE
signal.stageMask = VK_PIPELINE_STAGE_2_ALL_COMMANDS_BIT;
// vkQueueSubmit2(... waits=wait, signals=signal, fence=inFlight[frame])
// vkQueuePresentKHR waits on renderDone[img]
```
The wait stage mask lets earlier stages (vertex work, compute, shadow passes) start before the
image is available. Using `TOP_OF_PIPE`/`ALL_COMMANDS` for the acquire wait serialises the whole
frame behind the display.

The colour attachment layout transition from `UNDEFINED`/`PRESENT_SRC` must also wait at
`COLOR_ATTACHMENT_OUTPUT` (srcStage of the barrier), forming a dependency chain with the
semaphore wait.

## Why "renderDone" is per image
Present has no completion signal in core Vulkan. `renderDone[img]` is known to be free again only
once that same image index has been acquired again and the wait on that acquire's semaphore (or fence)
has completed, which guarantees the earlier present finished with it. So
index it by image index, while `imageAvailable` is indexed by frame-in-flight (it's protected by
the frame fence). Alternatively attach present fences with `VK_KHR_swapchain_maintenance1` (promoted from
`VK_EXT_swapchain_maintenance1`).

## Queue-to-queue
Graphics -> compute dependencies with binary semaphores work but every pair needs its own
semaphore; prefer one timeline semaphore per queue with increasing values.

## Verify
- [ ] Validation (incl. sync validation) clean over thousands of frames and resizes; GPU trace shows shadow passes starting before acquire completes.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Binary semaphore wait unsignals the semaphore; a wait must reference a signal that is already submitted or pending; exactly one signal may satisfy a binary wait (synchronization chapter and queue-submit valid usage).
- Confirmed: `vkAcquireNextImageKHR` and `vkQueuePresentKHR` require `VK_SEMAPHORE_TYPE_BINARY` semaphores (VUIDs in the WSI chapter).
- Confirmed: `VK_EXT_swapchain_maintenance1` is promoted to `VK_KHR_swapchain_maintenance1` (vk.xml `promotedto`); per-image present semaphore guidance is from the Vulkan Guide chapter `swapchain_semaphore_reuse`.
- Confirmed: `TOP_OF_PIPE` in a second synchronization scope is equivalent to `ALL_COMMANDS` with access 0 (synchronization chapter).

Method: documentation only; no commands were run.
