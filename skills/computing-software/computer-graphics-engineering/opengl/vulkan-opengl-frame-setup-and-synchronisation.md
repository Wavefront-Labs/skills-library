---
id: computing-software.computer-graphics-engineering.opengl.vulkan-opengl-frame-setup-and-synchronisation
name: vulkan-opengl-frame-setup-and-synchronisation
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [opengl, vulkan, gl-4-6, glsl, spir-v, rendering-pipeline, swapchain, frames-in-flight, fences, semaphores, pipeline-barriers, synchronization2, dynamic-rendering, vma, vulkan-memory-allocator, vao, vbo, ubo, dsa, direct-state-access, validation-layers, renderdoc, graphics-api, gpu, vkacquirenextimagekhr, vkqueuepresentkhr]
level: advanced
status: docs-checked
description: "Set up a correct render loop in Vulkan (and modern OpenGL): swapchain, frames in flight with fences/semaphores, barriers, buffer uploads, validation layers and RenderDoc."
sources: ["https://docs.vulkan.org/spec/latest/", "https://docs.vulkan.org/guide/latest/swapchain_semaphore_reuse.html", "https://github.com/KhronosGroup/OpenGL-Registry"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Vulkan / OpenGL frame setup and synchronisation

**Goal:** a render loop that keeps CPU and GPU both busy, never reads or overwrites a
resource the other is still using, and is debuggable — the part of a graphics API
beginners get subtly wrong. Vulkan in detail, OpenGL equivalents noted.

## Vulkan: the per-frame skeleton (2 frames in flight)
```cpp
constexpr int FRAMES_IN_FLIGHT = 2;
struct Frame { VkCommandPool pool; VkCommandBuffer cmd;
               VkSemaphore imageAvailable; VkFence inFlight; };
// per swapchain IMAGE (not per frame): VkSemaphore renderFinished[imageCount];

void drawFrame() {
    Frame& f = frames[frameIndex];
    vkWaitForFences(dev, 1, &f.inFlight, VK_TRUE, UINT64_MAX);   // CPU waits until GPU finished this slot
    uint32_t img;
    VkResult r = vkAcquireNextImageKHR(dev, swapchain, UINT64_MAX, f.imageAvailable, VK_NULL_HANDLE, &img);
    if (r == VK_ERROR_OUT_OF_DATE_KHR) { recreateSwapchain(); return; }
    vkResetFences(dev, 1, &f.inFlight);                          // reset only once we know we'll submit
    vkResetCommandPool(dev, f.pool, 0);
    record(f.cmd, img);                                          // barriers + rendering + barrier to PRESENT
    // submit: wait imageAvailable at COLOR_ATTACHMENT_OUTPUT, signal renderFinished[img], fence inFlight
    // present: wait renderFinished[img]
    frameIndex = (frameIndex + 1) % FRAMES_IN_FLIGHT;
}
```
Key points:
- **Fence** = GPU→CPU ("this frame's commands are done, you may reuse its command buffer
  and per-frame buffers"). **Semaphore** = GPU→GPU ordering between queue operations
  (acquire → render → present).
- Anything the CPU writes per frame (uniform buffers, dynamic vertex data, descriptor
  sets) needs **one copy per frame in flight**, indexed by `frameIndex`, or you overwrite
  data the GPU is still reading.
- 2 frames in flight is a common default; each extra frame in flight adds latency, so measure before raising it.
- Handle `VK_ERROR_OUT_OF_DATE_KHR` / `VK_SUBOPTIMAL_KHR` (resize, minimise) by recreating
  the swapchain after `vkDeviceWaitIdle`. On some platforms (for example the spec's XCB platform note) a minimised window has a (0, 0) extent and no swapchain can be created — pause until it is non-zero.
- Using one `renderFinished` (present wait) semaphore per frame in flight instead of per swapchain image is unsafe: the Vulkan Guide's
  semaphore-reuse chapter says the validation layer reports it since SDK 1.4.313 (`VUID-vkQueueSubmit-pSignalSemaphores-00067`); index by image.

## Barriers (synchronization2)
Every time an image changes role you need a layout transition + memory dependency:
```cpp
VkImageMemoryBarrier2 b{VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER_2};
b.srcStageMask  = VK_PIPELINE_STAGE_2_COLOR_ATTACHMENT_OUTPUT_BIT;
b.srcAccessMask = VK_ACCESS_2_COLOR_ATTACHMENT_WRITE_BIT;
b.dstStageMask  = VK_PIPELINE_STAGE_2_FRAGMENT_SHADER_BIT;
b.dstAccessMask = VK_ACCESS_2_SHADER_SAMPLED_READ_BIT;
b.oldLayout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
b.newLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
// image + subresourceRange, then vkCmdPipelineBarrier2 with a VkDependencyInfo
```
- Typical transitions: `UNDEFINED → COLOR_ATTACHMENT_OPTIMAL` (start of frame, discards
  contents), `COLOR_ATTACHMENT_OPTIMAL → PRESENT_SRC_KHR` (end of frame),
  `TRANSFER_DST → SHADER_READ_ONLY` after texture upload.
- `ALL_COMMANDS` + `MEMORY_READ|WRITE` is a correct-but-slow sledgehammer for debugging.
- **Dynamic rendering** is core in Vulkan 1.3 and avoids render pass/framebuffer objects; set load/store ops
  (`CLEAR`, `DONT_CARE`, `STORE`) deliberately for each attachment.

## Memory and uploads
- Use **VMA** (Vulkan Memory Allocator) — don't call `vkAllocateMemory` per buffer
  (the allocation count is limited: `maxMemoryAllocationCount` is only guaranteed to be at least 4096).
- Static meshes/textures: write to a host-visible staging buffer, `vkCmdCopyBuffer` /
  `vkCmdCopyBufferToImage` into device-local memory, barrier, then use. Batch uploads.
- Per-frame dynamic data: host-visible, persistently mapped, one region per frame in flight.

## OpenGL equivalents (4.5/4.6)
- Prefer **DSA** (`glCreateBuffers`, `glNamedBufferStorage`, `glCreateVertexArrays`,
  `glVertexArrayVertexBuffer`) over bind-to-edit.
- Immutable storage (`glBufferStorage`/`glNamedBufferStorage`) with `GL_MAP_PERSISTENT_BIT | GL_MAP_COHERENT_BIT` + a ring of regions (one per frame in flight) guarded by `glFenceSync` / `glClientWaitSync` is the GL analogue of frames in
  flight. Without the fence, writing a mapped region the GPU is reading is a race.
- The driver hides most hazards in GL — but `glMemoryBarrier` is still required after
  compute shader or image store writes before reading them.
- Debug: `glDebugMessageCallback` with a debug context.

## Debugging
- Always develop with `VK_LAYER_KHRONOS_validation` enabled (and synchronisation validation
  turned on via vkconfig) — treat every message as a bug.
- **RenderDoc**: capture a frame, inspect each draw's inputs/outputs, pipeline state and
  resource contents. Name objects (`vkSetDebugUtilsObjectNameEXT`) so captures are readable.

## Verify
- [ ] Validation layers (including sync validation) report zero messages over a run with resizing.
- [ ] Per-frame CPU-written resources are duplicated per frame in flight.
- [ ] Window resize and minimise don't crash or hang.
- [ ] RenderDoc capture shows expected layouts and no redundant full-pipeline barriers.
- [ ] GPU and CPU frame timings overlap (CPU isn't stalled waiting on the fence every frame).

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/VK_KHR_surface/wsi.adoc, chapters/limits.adoc, xml/vk.xml), the Vulkan Guide swapchain_semaphore_reuse chapter, and the OpenGL-Registry gl.xml.
Confirmed: minimised-window (0, 0) note; maxMemoryAllocationCount minimum 4096; present-wait semaphore reuse rule and VUID; VkSubmitInfo2/VkImageMemoryBarrier2 structures; dynamic rendering in 1.3; in gl.xml glCreateBuffers, glNamedBufferStorage, glCreateVertexArrays and glVertexArrayVertexBuffer are in GL 4.5, glBufferStorage in 4.4, glMemoryBarrier in 4.2, glDebugMessageCallback in 4.3, and the persistent and coherent map bits exist. Removed the mobile bandwidth and frames-in-flight opinion claims.
Method: documentation only; no commands were run.
