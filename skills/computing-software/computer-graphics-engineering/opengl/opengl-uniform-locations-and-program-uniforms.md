---
id: computing-software.computer-graphics-engineering.opengl.opengl-uniform-locations-and-program-uniforms
name: opengl-uniform-locations-and-program-uniforms
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, uniform-locations, explicit-uniform-location, glprogramuniform]
level: practitioner
status: docs-checked
description: "Set OpenGL uniforms robustly: explicit layout(location), glProgramUniform without binding, -1 locations from optimised-out uniforms, arrays and samplers."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glProgramUniform.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glUniform.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetUniformLocation.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uniform locations and glProgramUniform

## Explicit locations (ARB_explicit_uniform_location, in GLSL 4.60)
```glsl
layout(location = 0) uniform mat4 uModel;       // a matrix takes one location
layout(location = 1) uniform vec3 uTint;
layout(location = 2) uniform float uWeights[8]; // one location per element: 2..9
layout(binding = 2)  uniform sampler2D uAlbedo; // texture unit fixed in the shader
```
With fixed locations, C++ code uses constants, no `glGetUniformLocation` string lookups, and
every program sharing the convention can be fed the same way.

## Setting without binding (GL 4.1 / DSA style)
```c
glProgramUniformMatrix4fv(prog, 0, 1, GL_FALSE, &model[0][0]);   // no glUseProgram needed
glProgramUniform3f(prog, 1, 1.0f, 0.5f, 0.2f);
```
Classic `glUniform*` writes to the program bound by `glUseProgram`; forgetting to bind is the
most common "uniform does nothing" bug. `glProgramUniform` removes that state dependency.

## Location -1
- `glGetUniformLocation` returns -1 when the uniform is unused and optimised away. Setting
  location -1 is silently ignored (not an error), so debug code that disables a term makes its
  uniform vanish. Do not treat -1 as a fatal error; log once in debug builds.
- Array element locations: `uWeights[3]` = location of `uWeights[0]` + 3 is guaranteed for
  explicit locations; for queried locations query `"uWeights[3]"` or set the whole array at once.

## Types and transposes
- Matrices: `transpose = GL_FALSE` for column-major data; pass `GL_TRUE` for row-major data.
- `uint` uniforms need `glUniform1ui`; a mismatched integer/float or size variant generates `GL_INVALID_OPERATION`.
- Samplers take `glUniform1i(unit)`, never a texture name.

## When to stop using plain uniforms
Plain uniforms are per-program state: switching programs means re-uploading. For per-frame
and per-material data shared across programs use UBOs (std140) or SSBOs; keep plain uniforms
for a handful of per-draw values, or `layout(location)` uniforms set via `glProgramUniform`.

## Verify
- [ ] KHR_debug shows no `GL_INVALID_OPERATION` from uniform calls.
- [ ] RenderDoc pipeline state lists uniform values matching what the CPU set.

## Checked

Date: 2026-10-26. Documentation: GLSL 4.60 spec (uniform layout qualifiers), gl4 reference pages for glProgramUniform, glUniform and glGetUniformLocation. Confirmed: explicit `location` on default-block uniforms, arrays and structs take consecutive locations per inner-most scalar, vector or matrix element (so a matrix takes ONE location); `glProgramUniform*` is GL 4.1; location -1 is silently ignored; `glGetUniformLocation` returns -1 for inactive uniforms and accepts `[]` and `.` operators; integer/float variant and size mismatches generate `GL_INVALID_OPERATION`. Fixed: the example claimed `mat4` occupies four locations, which contradicted the spec; locations renumbered. Removed: version tags other than 4.1, bool and separable-pipeline remarks, GLM and push-constant references.

Method: documentation only; no commands were run.
