---
id: computing-software.computer-graphics-engineering.opengl.opengl-spirv-shaders
name: opengl-spirv-shaders
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, gl-spirv, arb-gl-spirv, spir-v, glslang, glspecializeshader, shader-binary-format]
level: advanced
status: docs-checked
description: "Load precompiled SPIR-V into OpenGL 4.6 with glShaderBinary and glSpecializeShader: glslang flags for GL, explicit locations/bindings, and the reflection features you lose."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_gl_spirv.txt", "https://github.com/KhronosGroup/glslang/blob/main/StandAlone/StandAlone.cpp", "https://github.com/google/shaderc/blob/main/glslc/README.asciidoc", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPIR-V shaders in OpenGL

**Goal:** ship compiled SPIR-V instead of GLSL source to OpenGL 4.6 (or `ARB_gl_spirv`),
sharing one offline compiler with a Vulkan backend and removing per-vendor GLSL parsing
differences.

## 1. Compile for the GL target
```sh
glslangValidator -G -o mesh.vert.spv mesh.vert         # -G[ver] = OpenGL semantics (not -V)
glslangValidator -G -o mesh.frag.spv mesh.frag
# or: glslc --target-env=opengl4.5 mesh.frag -o mesh.frag.spv
```
With `GL_ARB_gl_spirv`, name-based lookups are not reliable (names are optional in SPIR-V), so
give inputs, outputs and loose uniforms an explicit `layout(location = N)` and resource blocks
and samplers an explicit `layout(binding = N)`.

## 2. Load and specialise
```c
GLuint s = glCreateShader(GL_FRAGMENT_SHADER);
glShaderBinary(1, &s, GL_SHADER_BINARY_FORMAT_SPIR_V, bytes, (GLsizei)size);
GLuint idx[] = {0};  GLuint val[] = {4};                       // specialization constant id 0 = 4
glSpecializeShader(s, "main", 1, idx, val);
GLint ok; glGetShaderiv(s, GL_COMPILE_STATUS, &ok);             // specialization result
// attach + link exactly as with GLSL
```
`glSpecializeShader` replaces `glCompileShader`; check `GL_COMPILE_STATUS` afterwards.

## 3. What changes
- **No reflection by name**: `glGetUniformLocation` and block index queries by name don't
  work reliably (names may be stripped). Hard-code locations/bindings in a shared header.
- **Specialization constants** (`layout(constant_id = 0) const int N = 1;`) work and let
  one binary cover several variants.
- Subroutines and the other features removed by GL_KHR_vulkan_glsl are unavailable.
- The driver still turns SPIR-V into native code, so combine with program binaries (see
  `opengl-program-binary-caching`) if start-up cost matters.

## 4. Check support at runtime
SPIR-V loading is core in GL 4.6; on older contexts look for `GL_ARB_gl_spirv` in the extension
list (it needs GL 3.3 or later). Keep a GLSL fallback path for older drivers.

## Gotchas
- In glslang `-V` selects Vulkan semantics and `-G` OpenGL semantics; compile GL modules with `-G`.
- Test each vendor's driver before dropping the GLSL path.
- SPIR-V stage interfaces are matched by location (ARB_gl_spirv, "SPIR-V Shader Interface
  Matching"), so keep locations consistent across stages.

## Verify
- [ ] Program links and renders identically to the GLSL path on each vendor.
- [ ] Startup GLSL parse time removed (compare `glCompileShader` timings).
- [ ] CI compiles every shader with `-G` and fails on any warning.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). glslang StandAlone.cpp usage text and shaderc glslc README (both read from GitHub). Confirmed: glslangValidator -G[ver] creates SPIR-V under OpenGL semantics; glslc --target-env=opengl4.5; GL_SHADER_BINARY_FORMAT_SPIR_V, glShaderBinary and glSpecializeShader are GL 4.6 (gl.xml); the SpecializeShader example with specialization constants and GL_COMPILE_STATUS, names being optional and implementation-dependent, interface matching by location, GL 3.3 requirement (ARB_gl_spirv); subroutines removed with GL_KHR_vulkan_glsl (GLSL 4.60); local_size_x_id is SPIR-V only. Removed the unconfirmed vendor-bug, stutter and zeros-on-mismatch claims.
Method: documentation only; no commands were run.
