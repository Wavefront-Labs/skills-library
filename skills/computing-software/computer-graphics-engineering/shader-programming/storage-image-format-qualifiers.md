---
id: computing-software.computer-graphics-engineering.shader-programming.storage-image-format-qualifiers
name: storage-image-format-qualifiers
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-interfaces, image-format-qualifiers, storage-image, uav, rwtexture2d, imageload, imagestore, compute-shader]
level: practitioner
status: docs-checked
description: "Access storage images correctly: GLSL format qualifiers (rgba8, r32f), writeonly/readonly, formatless loads, imageAtomic*, HLSL RWTexture typed UAV loads and sRGB limits."
sources: ["https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#features-shaderStorageImageReadWithoutFormat", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#formats", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/SPIR-V.rst", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/typed-unordered-access-view-loads"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage image format qualifiers

## 1. GLSL
```glsl
layout(set = 0, binding = 0, rgba16f) uniform readonly  image2D src;
layout(set = 0, binding = 1, rgba8)   uniform writeonly image2D dst;
layout(set = 0, binding = 2, r32ui)   uniform uimage2D counters;

void main() {
    ivec2 p = ivec2(gl_GlobalInvocationID.xy);
    vec4 c = imageLoad(src, p);
    imageStore(dst, p, c);
    imageAtomicAdd(counters, p, 1u);
}
```
- The qualifier (`rgba8`, `rgba16f`, `r32f`, `r32ui`, `rgba8ui`, `r11f_g11f_b10f`, ...) declares
  how the shader interprets texels; it must be compatible with the view format.
- Omitting the format qualifier on writes needs the `shaderStorageImageWriteWithoutFormat` feature, and on reads
  `shaderStorageImageReadWithoutFormat` (with Vulkan 1.3 or `VK_KHR_format_feature_flags2` it applies to the formats in
  the spec's "storage without format" list). Query both.
- Image atomics need a format with `STORAGE_IMAGE_ATOMIC_BIT` (typically `r32ui`/`r32i`); 64-bit integer image
  atomics need `shaderImageInt64Atomics`, float ones `shaderImageFloat32Atomics` (`VK_EXT_shader_atomic_float`).

## 2. HLSL
```hlsl
RWTexture2D<float4> dst : register(u0);
RWTexture2D<uint>   counters : register(u1);
[[vk::image_format("rgba16f")]] RWTexture2D<float4> hdr : register(u2);  // DXC -> SPIR-V
```
- D3D12 typed UAV loads: R32_FLOAT, R32_UINT and R32_SINT are supported on all D3D12 hardware; additional formats need
  `TypedUAVLoadAdditionalFormats` (D3D12_FEATURE_DATA_D3D12_OPTIONS) plus a per-format
  `D3D12_FORMAT_SUPPORT2_UAV_TYPED_LOAD` check.
- Without `vk::image_format`, DXC emits `Unknown` format and relies on the without-format features.

## 3. Formats that don't work
- sRGB, block-compressed and depth formats are generally not usable as storage images: query
  `VK_FORMAT_FEATURE_STORAGE_IMAGE_BIT`. For sRGB, write to an `rgba8` unorm view of a mutable-format image and apply
  the transfer function in the shader before storing.
- For compressed targets, write through an uncompressed alias view (for example a 64-bit-per-texel uint format for a
  BC1 block) and copy, after checking the format-compatibility rules.
- For depth, copy to or from a colour `r32f` image.

## 4. Synchronisation
Storage writes are incoherent: barrier (`VK_ACCESS_SHADER_WRITE_BIT` -> read access,
`ResourceBarrier` UAV barrier) between dispatches that write then read the same image.
Within a workgroup use `memoryBarrierImage(); barrier();`.

## Gotchas
- Query `vkGetPhysicalDeviceFormatProperties` for `STORAGE_IMAGE_BIT` before choosing a format.
- `imageLoad` has no filtering and no LOD; it reads exactly one texel of the bound mip.
- Use `coherent` on image declarations when invocations of the same dispatch read what others wrote.

## Verify
- [ ] Validation layers silent about format/feature mismatches.
- [ ] Output matches a CPU reference for each format path (rgba8 rounding, f16 precision).

## Checked

Checked 2026-10-26 against Vulkan-Docs features and formats chapters (main, 2026-10-23), DXC docs/SPIR-V.rst, Microsoft typed UAV loads page. Confirmed: `shaderStorageImageReadWithoutFormat`/`WriteWithoutFormat` feature semantics and the storage-without-format list; `STORAGE_IMAGE_ATOMIC_BIT`; `shaderImageInt64Atomics` and `shaderImageFloat32Atomics`; DXC `[[vk::image_format("rgba8")]]` syntax; D3D12 typed UAV load formats and the `TypedUAVLoadAdditionalFormats` plus `CheckFeatureSupport` procedure. Softened (not asserted as fact): sRGB/compressed/depth storage restrictions, now phrased as 'query the format feature'; removed 'widely supported' and 'universal on DX12 hardware'.

Method: documentation only; no commands were run.
