---
id: computing-software.computer-graphics-engineering.opengl.vulkan-buffer-device-address
name: vulkan-buffer-device-address
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-memory, buffer-device-address, bda, gl-ext-buffer-reference, push-constants, vertex-pulling, pointers-in-shaders]
level: advanced
status: docs-checked
description: "Use Vulkan buffer device addresses as GPU pointers: enable the feature, pass 64-bit addresses via push constants, read them with GLSL buffer_reference, and debug faults."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/resources.adoc", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/buffer_device_address.adoc", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GLSL_EXT_buffer_reference.txt", "https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator/blob/master/include/vk_mem_alloc.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan buffer device address

**Goal:** skip descriptors for buffers entirely — shaders receive raw 64-bit GPU
addresses and dereference typed pointers (core 1.2).

## 1. Enable and create
```cpp
f12.bufferDeviceAddress = VK_TRUE;                          // Vulkan12Features
VkBufferCreateInfo bi{...}; bi.usage |= VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT;
VmaAllocatorCreateInfo vci{}; vci.flags |= VMA_ALLOCATOR_CREATE_BUFFER_DEVICE_ADDRESS_BIT;
// memory must be allocated with VK_MEMORY_ALLOCATE_DEVICE_ADDRESS_BIT (VMA does this when flagged)
VkBufferDeviceAddressInfo ai{VK_STRUCTURE_TYPE_BUFFER_DEVICE_ADDRESS_INFO}; ai.buffer = buf;
VkDeviceAddress addr = vkGetBufferDeviceAddress(dev, &ai);
```

## 2. Pass and dereference
```glsl
#extension GL_EXT_buffer_reference : require
struct Vertex { vec3 pos; float u; vec3 nrm; float v; };      // scalar-friendly layout
layout(buffer_reference, std430) readonly buffer VertexBuf { Vertex v[]; };
layout(push_constant) uniform PC { mat4 mvp; VertexBuf verts; } pc;
void main() {
    Vertex vx = pc.verts.v[gl_VertexIndex];                   // vertex pulling via pointer
    gl_Position = pc.mvp * vec4(vx.pos, 1);
}
```
CPU side pushes `{mvp, addr}` with `vkCmdPushConstants`. Pointer arithmetic: cast via
`uint64_t` (`GL_EXT_shader_explicit_arithmetic_types_int64`) or index arrays.

## 3. Patterns
- **Per-draw data tables**: one SSBO of structs holding addresses of each mesh's vertex,
  index and material buffers; index by `gl_InstanceIndex`/draw id.
- **Linked structures / scene graphs** on GPU; trees with child pointers.

## 4. Alignment and layout
Declare alignment for references: `layout(buffer_reference, buffer_reference_align = 16)`.
Use `GL_EXT_scalar_block_layout` (`scalar`) to match tightly packed C structs.

## Gotchas
- Accesses through an address are not bounds checked by Vulkan: an access outside the buffer is
  invalid usage. After `VK_ERROR_DEVICE_LOST`, `VK_KHR_device_fault` (promoted from
  `VK_EXT_device_fault`) can report fault address information.
- Do not enable `VK_EXT_buffer_device_address` on a device where
  `VkPhysicalDeviceVulkan12Features::bufferDeviceAddress` is enabled.
- Buffer lifetime is your problem: freeing a buffer whose address is stored in another
  buffer is a dangling pointer the validation layer can't see.
- Name buffers and log addresses in debug builds so a faulting address can be mapped back.
- Reproducing addresses in capture/replay needs the `bufferDeviceAddressCaptureReplay` feature.

## Verify
- [ ] Debug runs with the validation layers enabled report no errors.
- [ ] Mesh renders identically via BDA vertex pulling and the classic vertex-input path.
- [ ] Device-lost reports include a faulting address mapped back to a named buffer.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: `bufferDeviceAddress` is a `VkPhysicalDeviceVulkan12Features` member; `VK_KHR_buffer_device_address` promoted to 1.2; `VkBufferDeviceAddressInfo::buffer` needs `VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT` (VUID-VkBufferDeviceAddressInfo-buffer-02601); `VK_MEMORY_ALLOCATE_DEVICE_ADDRESS_BIT` and `bufferDeviceAddressCaptureReplay` exist (memory chapter).
- Confirmed: Enabling `VK_EXT_buffer_device_address` together with the 1.2 feature is rejected (VUID in the device chapter). `VK_EXT_device_fault` is promoted to `VK_KHR_device_fault`.
- Confirmed: GLSL_EXT_buffer_reference: `buffer_reference_align` is a power of two, and a reference can be constructed from a `uint64_t`.
- Confirmed: VMA names (`VMA_ALLOCATOR_CREATE_BUFFER_DEVICE_ADDRESS_BIT`, which adds the device-address allocate flag automatically) confirmed in vk_mem_alloc.h.
- Removed: ray-tracing requirement, GPU-assisted-validation coverage of BDA and RenderDoc remarks (no source found).

Method: documentation only; no commands were run.
