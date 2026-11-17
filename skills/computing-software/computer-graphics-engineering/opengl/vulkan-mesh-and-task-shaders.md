---
id: computing-software.computer-graphics-engineering.opengl.vulkan-mesh-and-task-shaders
name: vulkan-mesh-and-task-shaders
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-pipelines, vk-ext-mesh-shader, task-shader, meshlets-vulkan]
level: sme
status: docs-checked
description: "Use VK_EXT_mesh_shader: task/mesh GLSL, meshlet output limits, vkCmdDrawMeshTasksEXT, payloads for culling, and the guaranteed minimum limits for sizing."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_mesh_shader.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GLSL_EXT_mesh_shader.txt", "https://github.com/zeux/meshoptimizer/blob/master/src/meshoptimizer.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mesh and task shaders (VK_EXT_mesh_shader)

Replaces the vertex/input-assembly front end with compute-like stages: an optional **task**
shader decides how many mesh workgroups to launch (culling/LOD), each **mesh** workgroup outputs
a small batch of vertices and primitives (a meshlet).

## Mesh shader
```glsl
#version 460
#extension GL_EXT_mesh_shader : require
layout(local_size_x = 32) in;
layout(triangles, max_vertices = 64, max_primitives = 124) out;
struct Meshlet { uint vertexOffset, triangleOffset, vertexCount, triangleCount; };
layout(std430, set = 0, binding = 0) readonly buffer Meshlets { Meshlet meshlets[]; };
layout(std430, set = 0, binding = 1) readonly buffer VertIdx { uint vertexIndices[]; };
layout(std430, set = 0, binding = 2) readonly buffer TriIdx  { uint8_t triIndices[]; };  // needs 8-bit storage
taskPayloadSharedEXT struct { uint meshletIds[32]; } payload;
layout(location = 0) out vec3 vNormal[];
void main() {
    Meshlet m = meshlets[payload.meshletIds[gl_WorkGroupID.x]];
    SetMeshOutputsEXT(m.vertexCount, m.triangleCount);           // call once, before writing outputs
    for (uint i = gl_LocalInvocationIndex; i < m.vertexCount; i += 32) {
        uint v = vertexIndices[m.vertexOffset + i];
        gl_MeshVerticesEXT[i].gl_Position = viewProj * vec4(positions[v], 1);
        vNormal[i] = normals[v];
    }
    for (uint t = gl_LocalInvocationIndex; t < m.triangleCount; t += 32) {
        uint b = m.triangleOffset + t * 3;
        gl_PrimitiveTriangleIndicesEXT[t] = uvec3(triIndices[b], triIndices[b+1], triIndices[b+2]);
    }
}
```

## Task shader (culling)
```glsl
layout(local_size_x = 32) in;
taskPayloadSharedEXT struct { uint meshletIds[32]; } payload;
void main() {
    uint id = gl_GlobalInvocationID.x;
    bool visible = id < meshletCount && coneAndFrustumVisible(id);
    uvec4 ballot = subgroupBallot(visible);
    uint slot = subgroupBallotExclusiveBitCount(ballot);
    if (visible) payload.meshletIds[slot] = id;
    EmitMeshTasksEXT(subgroupBallotBitCount(ballot), 1, 1);      // exactly once, under uniform control flow
}
```
Host: `vkCmdDrawMeshTasksEXT(cmd, ceil(meshletCount / 32), 1, 1)` or the indirect(-count) variants.

## Sizing
- The example uses 64 vertices / 124 primitives, within the guaranteed minimum limits
  (`maxMeshOutputVertices` and `maxMeshOutputPrimitives` at least 256, `maxMeshWorkGroupInvocations`
  at least 128). Query `VkPhysicalDeviceMeshShaderPropertiesEXT` (`maxMeshOutputVertices`,
  `maxPreferredMeshWorkGroupInvocations`, `prefersLocalInvocationVertexOutput`) and tune per device.
- Build meshlets offline with meshoptimizer `meshopt_buildMeshlets` plus bounds
  (`meshopt_computeMeshletBounds`) for cone culling.

## Gotchas
- Features `meshShader`, `taskShader`; pipeline has no vertex input state and no input assembly.
- `SetMeshOutputsEXT` may be called at most once per workgroup, under uniform control flow, before any
  output write; indexing outputs beyond the counts passed to it, or writing primitive indices outside
  [0, primitiveCount - 1], is undefined behaviour.
- Per-primitive outputs need `perprimitiveEXT` qualifiers in both mesh and fragment shaders.
- The extension is optional: check the `meshShader` and `taskShader` features and keep a vertex-shader path.

## Verify
- [ ] Mesh shader statistics (`VK_QUERY_TYPE_MESH_PRIMITIVES_GENERATED_EXT`) drop when task culling is on; image identical to the vertex path.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: GLSL_EXT_mesh_shader: `EmitMeshTasksEXT` exactly once under uniform control flow; `SetMeshOutputsEXT` no more than once, uniform, and required before output writes; out-of-range output indexing is undefined.
- Confirmed: Limits table minimums for `VkPhysicalDeviceMeshShaderPropertiesEXT`: `maxMeshWorkGroupInvocations` 128, `maxMeshOutputVertices` 256, `maxMeshOutputPrimitives` 256; `maxPreferredMeshWorkGroupInvocations` and `prefersLocalInvocationVertexOutput` exist in vk.xml; `VK_QUERY_TYPE_MESH_PRIMITIVES_GENERATED_EXT` exists.
- Confirmed: Pipeline chapter: vertex input and input assembly state are required only when the pipeline has a vertex shader; `meshopt_buildMeshlets` and `meshopt_computeMeshletBounds` exist in meshoptimizer.h.
- Removed vendor meshlet-size guidance and mobile support remark (no source found).

Method: documentation only; no commands were run.
