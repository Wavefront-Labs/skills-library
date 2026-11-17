---
id: computing-software.computer-graphics-engineering.directx.vulkan-ray-tracing-pipeline-and-ray-query
name: vulkan-ray-tracing-pipeline-and-ray-query
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxr, vk-khr-ray-tracing, vulkan-ray-query, shader-binding-table-vulkan]
level: sme
status: docs-checked
description: "Port DXR concepts to Vulkan KHR ray tracing: acceleration structure builds, ray tracing pipelines, shader binding table alignment, ray queries and GLSL/HLSL shaders."
sources: ["https://docs.vulkan.org/spec/latest/chapters/raytracing.html", "https://docs.vulkan.org/spec/latest/chapters/accelstructures.html", "https://docs.vulkan.org/spec/latest/chapters/limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan ray tracing (KHR) for DXR developers

## Extension set
`VK_KHR_acceleration_structure` (+ `VK_KHR_deferred_host_operations`), `VK_KHR_ray_tracing_pipeline`
and/or `VK_KHR_ray_query`, plus `bufferDeviceAddress` and descriptor indexing features.

## Concept map
| DXR | Vulkan |
|---|---|
| BLAS/TLAS build (`BuildRaytracingAccelerationStructure`) | `vkCmdBuildAccelerationStructuresKHR` |
| prebuild info | `vkGetAccelerationStructureBuildSizesKHR` |
| instance desc | `VkAccelerationStructureInstanceKHR` (3x4 row-major transform, 24-bit custom index, 8-bit mask, 24-bit SBT record offset, flags) |
| state object / hit groups | `vkCreateRayTracingPipelinesKHR` with shader groups (general, triangles hit, procedural hit) |
| shader table + `DispatchRays` | SBT buffer + `vkCmdTraceRaysKHR` with strided device address regions |
| `RayQuery` | `rayQueryEXT` (GLSL; SPIR-V capability from `SPV_KHR_ray_query`) |
| `InstanceID()` | SPIR-V built-in `InstanceCustomIndexKHR` |

## Shader binding table
```c
uint32_t handleSize = rtProps.shaderGroupHandleSize;                  // exactly 32 in the KHR extension
uint32_t handleAlign = rtProps.shaderGroupHandleAlignment;            // at most 32
uint32_t baseAlign = rtProps.shaderGroupBaseAlignment;                // at most 64
uint32_t stride = alignUp(handleSize + recordDataSize, handleAlign);
vkGetRayTracingShaderGroupHandlesKHR(dev, pipeline, 0, groupCount, groupCount * handleSize, handles);
// copy handles into an SBT buffer created with VK_BUFFER_USAGE_SHADER_BINDING_TABLE_BIT_KHR + device address usage;
// raygen, miss, hit and callable region addresses must each be a multiple of shaderGroupBaseAlignment
VkStridedDeviceAddressRegionKHR rgen = { sbtAddr, alignUp(stride, baseAlign), alignUp(stride, baseAlign) };  // raygen size == stride
VkStridedDeviceAddressRegionKHR miss = { sbtAddr + missOff, stride, stride * missCount };
VkStridedDeviceAddressRegionKHR hit  = { sbtAddr + hitOff,  stride, stride * hitCount };
VkStridedDeviceAddressRegionKHR call = {};
vkCmdTraceRaysKHR(cmd, &rgen, &miss, &hit, &call, width, height, 1);
```
Rules from the spec: the raygen region `size` must equal its `stride`; miss/hit/callable strides must be multiples of `shaderGroupHandleAlignment` and at most `maxShaderGroupStride`.

## Shaders (GLSL)
```glsl
#extension GL_EXT_ray_tracing : require
layout(location = 0) rayPayloadEXT vec3 payload;
layout(set = 0, binding = 0) uniform accelerationStructureEXT tlas;
traceRayEXT(tlas, 0, 0xFF, 0, 1, 0, origin, 0.001, dir, 1e4, 0);
```
`VK_KHR_ray_tracing_pipeline` and `VK_KHR_ray_query` depend on Vulkan 1.2 or `VK_KHR_spirv_1_4`, so compile the shaders for SPIR-V 1.4 or later (Vulkan 1.2 target environment).

## Gotchas
- AS buffers need `ACCELERATION_STRUCTURE_STORAGE_BIT_KHR` + device address usage; scratch
  addresses are aligned to `minAccelerationStructureScratchOffsetAlignment`.
- Barrier between AS build and trace: `ACCELERATION_STRUCTURE_BUILD` stage with `ACCELERATION_STRUCTURE_WRITE` access to
  the `RAY_TRACING_SHADER` stage (or the shader stage that runs the ray query) with `ACCELERATION_STRUCTURE_READ` access.
- `VkTransformMatrixKHR` is a 3x4 row-major affine matrix, not GLM's column-major 4x4.

## Verify
- [ ] Validation clean (including SBT alignment and stride rules).

## Checked
Checked 2026-10-26 against Vulkan-Docs main (tag v1.4.366): chapters/limits.adoc, raytracing.adoc, accelstructures.adoc, synchronization.adoc, commonvalidity/trace_rays_binding_table*.adoc, xml/vk.xml.
Confirmed: shaderGroupHandleSize exact 32 and handle alignment max 32, base alignment max 64 (limits table); raygen size equals stride; SBT address and stride rules; row-major 3x4 transform and 24-bit instance fields; SBT buffer usage flag; AS stage and access names; spirv_1_4 / Vulkan 1.2 dependency. Removed unverified DXC/HLSL and DXR layout claims.
Method: documentation only; no commands were run.
