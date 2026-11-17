---
id: computing-software.computer-graphics-engineering.directx.d3d12-copydescriptors-and-staging-heaps
name: d3d12-copydescriptors-and-staging-heaps
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, resource-binding, copydescriptors, non-shader-visible-heap, cpu-descriptor-heap]
level: advanced
status: docs-checked
description: "Create D3D12 views in CPU-only (non-shader-visible) heaps and copy them into shader-visible tables with CopyDescriptors/CopyDescriptorsSimple efficiently."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-copydescriptors", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/copying-descriptors", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/non-shader-visible-descriptor-heaps", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_descriptor_heap_flags", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-clearunorderedaccessviewfloat"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CopyDescriptors and staging (CPU) heaps

## Why two kinds of heaps
- **Non-shader-visible** (`D3D12_DESCRIPTOR_HEAP_FLAG_NONE`): not bindable on a command list. Use them as the
  "home" of every view you create (`CreateShaderResourceView`, `CreateUnorderedAccessView`,
  `CreateConstantBufferView`). RTV and DSV heaps are always this kind: creating one with the shader-visible
  flag is an error, and their descriptors are recorded directly into the command list.
- **Shader-visible** (`D3D12_DESCRIPTOR_HEAP_FLAG_SHADER_VISIBLE`, CBV/SRV/UAV and sampler heaps only): bound with
  `SetDescriptorHeaps`; at most one CBV/SRV/UAV heap and one sampler heap can be bound at a time.
  Populate it by copying from home locations, or write to it directly.

## Copying
```cpp
// contiguous source to contiguous destination
device->CopyDescriptorsSimple(count, gpuVisibleCpuHandle /*dest*/, stagingCpuHandle /*src*/,
                              D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV);
// scattered sources gathered into one destination table
D3D12_CPU_DESCRIPTOR_HANDLE dst[] = { tableStart };            UINT dstSizes[] = { 3 };
D3D12_CPU_DESCRIPTOR_HANDLE src[] = { albedoSrv, normalSrv, ormSrv }; UINT srcSizes[] = { 1, 1, 1 };
device->CopyDescriptors(1, dst, dstSizes, 3, src, srcSizes, D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV);
```
- These device methods use the CPU to copy immediately (they are not recorded in a command list), and can be
  called free-threaded as long as no threads perform conflicting writes.
- **Source descriptors must come from a non-shader-visible heap.** The destination can be in any CPU-visible
  heap, shader-visible or not. (Shader-visible heaps may live in write-combined or GPU-local memory, which is
  prohibitively slow to read from.)
- The total number of source descriptors must equal the total number of destination descriptors; the ranges
  need not line up. All source and destination heaps must be the same `D3D12_DESCRIPTOR_HEAP_TYPE`
  (the debug layer reports an error otherwise).
- Prefer `CopyDescriptorsSimple` when copying a single contiguous range: it can have a better CPU cache-miss
  rate.

## UAV clears need both handles
`ClearUnorderedAccessViewFloat/Uint(ViewGPUHandleInCurrentHeap, ViewCPUHandle, resource, values, ...)` takes a GPU
handle to a descriptor in a shader-visible heap that is set on the command list **and** a CPU handle to
an initialised descriptor for the same view in a non-shader-visible heap. Keep a CPU-side copy of every UAV
you clear.

## Gotchas
- Root descriptors (root CBV/SRV/UAV) bypass descriptor heaps entirely: pass GPU virtual addresses for
  frequently changing buffers instead of copying views.
- Only copy descriptors that are initialised; a destroyed resource leaves its views dangling.
- With bindless access (persistent slots written once at load), most per-frame copying disappears.

## Verify
- [ ] No CopyDescriptors call uses a shader-visible heap as a source; UAV clears run without debug-layer errors.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Copying descriptors", "Non shader visible descriptor heaps",
`ID3D12Device::CopyDescriptors`, `D3D12_DESCRIPTOR_HEAP_FLAGS`, `ClearUnorderedAccessViewFloat`
(MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08). Confirmed: source must be non-shader-visible
(a requirement, not just a tip); same-type rule; immediate CPU-timeline copy; both-handle UAV clear
requirement; RTV/DSV heaps never shader-visible; one-bound-heap limit. Removed unconfirmed claims: descriptor
sizes of 32-64 bytes, "thousands per frame is fine".
Method: documentation only; no commands were run.
