---
id: computing-software.computer-graphics-engineering.opengl.vulkan-buffer-suballocation-and-alignment
name: vulkan-buffer-suballocation-and-alignment
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-memory, buffer-suballocation, min-uniform-buffer-offset-alignment, linear-allocator]
level: advanced
status: docs-checked
description: "Suballocate one big Vulkan buffer for many objects: offset alignment limits for UBO/SSBO/vertex/indirect, linear per-frame allocators and VMA virtual blocks."
sources: ["https://docs.vulkan.org/spec/latest/chapters/limits.html", "https://gpuopen-librariesandsdks.github.io/VulkanMemoryAllocator/html/virtual_allocator.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Buffer suballocation and alignment

One `VkBuffer` per mesh/uniform block wastes allocations, descriptor updates and binds. Put many
sub-ranges in one large buffer and address them by offset.

## Alignment rules by use
| Use | Offset must be a multiple of |
|---|---|
| Uniform buffer descriptor offset / dynamic offset | `minUniformBufferOffsetAlignment` (the required limit is at most 256; query the real value) |
| Storage buffer descriptor offset | `minStorageBufferOffsetAlignment` (required limit at most 256) |
| Texel buffer view | `minTexelBufferOffsetAlignment` (required limit at most 256; Vulkan 1.3 adds per-format `uniformTexelBufferOffsetAlignmentBytes` and `storageTexelBufferOffsetAlignmentBytes`) |
| Vertex buffer binding offset | no limit beyond attribute format alignment (keep 4) |
| Index buffer offset | offset plus the memory base address must be a multiple of the index type size (2 or 4) |
| Indirect buffer offset | 4 |
| `vkCmdCopyBuffer` | none; `vkCmdFillBuffer`/`UpdateBuffer`: 4 |
| Flush/invalidate (non-coherent) | `nonCoherentAtomSize` |

```c
static VkDeviceSize alignUp(VkDeviceSize v, VkDeviceSize a) { return (v + a - 1) & ~(a - 1); }  // a is power of two
```

## Per-frame linear allocator (uniforms, dynamic vertices)
```c
struct FrameArena { VkBuffer buf; uint8_t* mapped; VkDeviceSize head, cap; };
VkDeviceSize push(FrameArena& a, const void* data, VkDeviceSize size, VkDeviceSize align) {
    VkDeviceSize off = alignUp(a.head, align);
    assert(off + size <= a.cap);              // grow or fail loudly
    memcpy(a.mapped + off, data, size); a.head = off + size; return off;
}
// one arena per frame in flight; reset head = 0 after that frame's fence signals
```
Bind with a dynamic UBO descriptor and pass `off` as the dynamic offset, or pass the buffer
device address + offset in a push constant.

## Long-lived suballocation (meshes)
Use VMA's virtual allocator to manage ranges inside your own big buffer:
```c
VmaVirtualBlockCreateInfo bci = { .size = 256ull << 20 };
VmaVirtualBlock block; vmaCreateVirtualBlock(&bci, &block);
VmaVirtualAllocationCreateInfo ai = { .size = bytes, .alignment = 16 };
VmaVirtualAllocation va; VkDeviceSize off; vmaVirtualAllocate(block, &ai, &va, &off);
// ... vmaVirtualFree(block, va) when the mesh unloads
```
All meshes in one vertex + one index buffer also enables single-bind multi-draw indirect.

## Gotchas
- UBO size limit `maxUniformBufferRange` (guaranteed minimum 16384 bytes) applies per descriptor range, not per
  buffer; SSBO `maxStorageBufferRange` has a guaranteed minimum of 2^27 bytes.
- Freeing a suballocation still used by an in-flight frame corrupts it; defer frees by
  frames-in-flight.
- A buffer's usage flags are the union of all uses; include every flag you'll need.

## Verify
- [ ] Validation clean with offsets aligned to the queried limits (limits can be as large as 256 bytes); assert fires if an arena overflows.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (validusage.json, chapters/limits.adoc) and the VMA header vk_mem_alloc.h (main).
Confirmed: required-limit maxima of 256 for min uniform, storage and texel buffer offset alignment; maxUniformBufferRange minimum 16384 and maxStorageBufferRange minimum 2^27; index offset, indirect offset (4), fill and update offset and size (4) VUIDs; VMA virtual block functions vmaCreateVirtualBlock, vmaVirtualAllocate, vmaVirtualFree and the size and alignment fields. Removed the unverified buffer-device-address alignment row and the typical-value ranges.
Method: documentation only; no commands were run.
