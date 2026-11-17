---
id: computing-software.computer-graphics-engineering.opengl.vulkan-external-memory-interop
name: vulkan-external-memory-interop
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-memory, external-memory, vulkan-interop, cuda-vulkan-interop]
level: sme
status: docs-checked
description: "Share Vulkan memory and semaphores with CUDA, D3D11/12, OpenGL or dma-buf via VK_KHR_external_memory/semaphore: export, import, layouts and sync."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_external_memory_win32.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_external_memory_fd.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/memory.adoc", "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EXTRES__INTEROP.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/extensions/EXT/EXT_external_objects.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External memory interop

Zero-copy sharing between Vulkan and other APIs/processes: CUDA inference on rendered frames,
video decode into textures (dma-buf), GL/D3D apps embedding Vulkan renderers.

## 1. Export memory from Vulkan
```c
VkExternalMemoryImageCreateInfo emi = { VK_STRUCTURE_TYPE_EXTERNAL_MEMORY_IMAGE_CREATE_INFO };
emi.handleTypes = VK_EXTERNAL_MEMORY_HANDLE_TYPE_OPAQUE_WIN32_BIT;   // OPAQUE_FD_BIT on Linux
imageCI.pNext = &emi;                                                 // on the image/buffer
VkExportMemoryAllocateInfo exp = { VK_STRUCTURE_TYPE_EXPORT_MEMORY_ALLOCATE_INFO };
exp.handleTypes = emi.handleTypes;
VkMemoryDedicatedAllocateInfo ded = { VK_STRUCTURE_TYPE_MEMORY_DEDICATED_ALLOCATE_INFO, &exp, image };
allocInfo.pNext = &ded;                          // some handle types require a dedicated allocation (see Gotchas)
vkAllocateMemory(dev, &allocInfo, NULL, &mem);
VkMemoryGetWin32HandleInfoKHR gh = { VK_STRUCTURE_TYPE_MEMORY_GET_WIN32_HANDLE_INFO_KHR, NULL, mem, emi.handleTypes };
HANDLE h; vkGetMemoryWin32HandleKHR(dev, &gh, &h);  // vkGetMemoryFdKHR on Linux
```
Check `vkGetPhysicalDeviceImageFormatProperties2` with `VkPhysicalDeviceExternalImageFormatInfo`
first: not every format/usage is exportable.

## 2. Import elsewhere
- **CUDA:** `cudaImportExternalMemory` (type `cudaExternalMemoryHandleTypeOpaqueWin32`/`OpaqueFd`,
  size = allocation size; the `cudaExternalMemoryDedicated` flag is required for the D3D11/D3D12 resource handle types) then
  `cudaExternalMemoryGetMappedBuffer` or `...GetMappedMipmappedArray` for images.
- **OpenGL:** `EXT_memory_object` + `EXT_memory_object_win32/fd`: `glImportMemoryWin32HandleEXT`,
  then `glTextureStorageMem2DEXT` with matching format, size and tiling (optimal on both sides).
- **D3D12:** `VK_EXTERNAL_MEMORY_HANDLE_TYPE_D3D12_RESOURCE_BIT` with a shared NT handle from
  `CreateSharedHandle`, imported via `VkImportMemoryWin32HandleInfoKHR`.
- **dma-buf (Linux video/camera):** `VK_EXT_external_memory_dma_buf` +
  `VK_EXT_image_drm_format_modifier` to import with the producer's DRM modifier.

## 3. Share semaphores for sync
Export a semaphore (`VkExportSemaphoreCreateInfo`, timeline type for CUDA) and import it as
`cudaExternalSemaphore`/GL semaphore object. Order: Vulkan signals -> other API waits -> other
API signals -> Vulkan waits. Never rely on `vkDeviceWaitIdle` + CPU handoff in production.

## 4. Layouts and ownership
Images shared outside Vulkan need a queue family ownership transfer to/from
`VK_QUEUE_FAMILY_EXTERNAL` and a layout the other API understands (GL's
`glWaitSemaphoreEXT`/`glSignalSemaphoreEXT` take the expected layouts, e.g.
`GL_LAYOUT_SHADER_READ_ONLY_EXT`).

## Gotchas
- Both sides must use the same physical GPU: compare `deviceUUID` (`VkPhysicalDeviceIDProperties`)
  with CUDA's `cudaDeviceProp::uuid` / GL's `GL_DEVICE_UUID_EXT`.
- Win32 handles: a successful `vkGetMemoryWin32HandleKHR` gives the application ownership of the handle (close it with
  `CloseHandle`), and importing a Win32 handle never transfers ownership to the driver. For FDs, a successful
  `vkGetMemoryFdKHR` gives the fd to the application and a successful import transfers it back to the driver (CUDA's
  import of an FD likewise takes ownership; its Win32 import does not).
- Importing a Vulkan-created handle of the Win32 opaque, D3D11 or D3D12 types needs a dedicated allocation that names
  the same image or buffer, and for the D3D11/D3D12 resource types `allocationSize` is ignored (the size is queried
  from the OS). Check `VkExternalMemoryProperties` (via `vkGetPhysicalDeviceImageFormatProperties2`) for dedicated-only handle types.
- Size and offset of imported CUDA memory must match the Vulkan allocation size, not the image size.

## Verify
- [ ] UUIDs match; CUDA kernel reads the rendered frame with no copies (Nsight Systems shows no memcpy) and no tearing between producer/consumer.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23), the OpenGL-Registry EXT_external_objects texts and the CUDA runtime API reference (external resource interoperability, `cudaDeviceProp`). Confirmed: handle ownership rules (Win32 get transfers ownership to the app and import never gives it back; FD import transfers it to the driver); dedicated-allocation rules and ignored `allocationSize` for D3D11/D3D12 imports (memory.adoc); `cudaImportExternalMemory`, `cudaExternalMemoryGetMappedBuffer`, `cudaExternalMemoryGetMappedMipmappedArray`, handle types `OpaqueWin32` and `OpaqueFd`, the `cudaExternalMemoryDedicated` flag (required for D3D11/D3D12 types), timeline semaphore handle types, and `cudaDeviceProp::uuid`; the GL names `glImportMemoryWin32HandleEXT`, `glTextureStorageMem2DEXT`, `glWaitSemaphoreEXT`, `glSignalSemaphoreEXT`, `GL_LAYOUT_SHADER_READ_ONLY_EXT` and `GL_DEVICE_UUID_EXT` appear in the registry text; Vulkan names exist in vk.xml. Corrected the earlier claim that dedicated allocation is required for most interop and the one-line ownership rule.

Method: documentation only; no commands were run.
