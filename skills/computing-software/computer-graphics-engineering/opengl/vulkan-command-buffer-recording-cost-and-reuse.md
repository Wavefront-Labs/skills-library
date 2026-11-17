---
id: computing-software.computer-graphics-engineering.opengl.vulkan-command-buffer-recording-cost-and-reuse
name: vulkan-command-buffer-recording-cost-and-reuse
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, command-buffers, command-buffer-reuse, simultaneous-use, recording-performance]
level: advanced
status: docs-checked
description: "Reduce Vulkan command recording cost: re-record vs reuse, SIMULTANEOUS_USE, pool reset strategy, state redundancy, and measuring recording time."
sources: ["https://docs.vulkan.org/spec/latest/chapters/cmdbuffers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command recording cost and reuse

## Re-record each frame (default)
Most engines record every frame: camera, visibility and per-frame data change anyway.
Recording is cheap if you:
- Reset the **pool** (`vkResetCommandPool`) once per frame per thread instead of resetting
  individual command buffers (`VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT` is only needed to allow
  per-buffer `vkResetCommandBuffer`).
- Mark `VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT` when each recording is submitted only once and re-recorded before the next submission.
- Avoid redundant binds: cache the last bound pipeline, descriptor sets, vertex/index buffers
  in your recorder.
- Sort draws by pipeline, then material set, then mesh to minimise binds.

## Reusing pre-recorded command buffers
Static work (e.g. a fixed UI pass, a post chain with constant targets) can be recorded once and
resubmitted, as long as everything it references stays valid and data changes go through
buffers (uniforms via dynamic offsets or buffer device addresses, not baked push constants).
- If a command buffer may be pending on the GPU while submitted again (e.g. same buffer for
  two frames in flight), it needs `VK_COMMAND_BUFFER_USAGE_SIMULTANEOUS_USE_BIT` (resubmission while pending
  on any queue of the same family). Usually simpler: one copy per frame in flight.
- Swapchain-image-dependent passes need one buffer per swapchain image (or dynamic rendering
  with image views supplied at record time).

## Measuring
- CPU-time each `vkBeginCommandBuffer`..`vkEndCommandBuffer` per pass (Tracy zones).
- Compare per-draw cost against your own frame budget; if recording dominates, look for descriptor updates
  or pipeline binds per draw.
- Parallelise with one command pool per thread per frame; record primaries or secondaries.

## Gotchas
- Command buffers allocated from a pool must only be recorded by one thread at a time; pools are
  externally synchronised.
- Freeing and reallocating command buffers every frame is slow; allocate once, reset the pool.
- `vkEndCommandBuffer` can return out-of-memory errors; check it.

## Verify
- [ ] Recording time per frame visible in profiler; no repeated identical bind calls in an API call capture.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/cmdbuffers.adoc, xml/vk.xml).
Confirmed: RESET_COMMAND_BUFFER_BIT, TRANSIENT, ONE_TIME_SUBMIT and SIMULTANEOUS_USE semantics; pool reset returns buffers to the initial state; vkEndCommandBuffer can return VK_ERROR_OUT_OF_HOST_MEMORY and VK_ERROR_OUT_OF_DEVICE_MEMORY; pools are externally synchronised. Removed unverified driver-overhead, Arm/Mali and per-draw timing claims and the api_dump layer name.
Method: documentation only; no commands were run.
