---
id: computing-software.computer-graphics-engineering.opengl.opengl-program-binary-caching
name: opengl-program-binary-caching
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, program-binary, shader-cache, glgetprogrambinary, compile-stutter]
level: practitioner
status: docs-checked
description: "Cut OpenGL shader start-up and hitching with glGetProgramBinary caches: cache keys, driver invalidation, source fallback and warm-up."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetProgramBinary.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glProgramBinary.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glProgramParameter.xhtml", "https://registry.khronos.org/OpenGL/extensions/KHR/KHR_parallel_shader_compile.txt", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Program binary caching

**Goal:** compile and link GLSL once per machine/driver, then reload the driver's binary on later
runs (GL 4.1 / ES 3.0 / `ARB_get_program_binary`).

## 1. Save
```c
glProgramParameteri(prog, GL_PROGRAM_BINARY_RETRIEVABLE_HINT, GL_TRUE);  // before link
glLinkProgram(prog);
GLint len; glGetProgramiv(prog, GL_PROGRAM_BINARY_LENGTH, &len);
std::vector<uint8_t> blob(len); GLenum fmt;
glGetProgramBinary(prog, len, nullptr, &fmt, blob.data());
// write {fmt, blob} to cache/<key>.bin
```

## 2. Load with fallback
```c
GLuint prog = glCreateProgram();
glProgramBinary(prog, fmt, blob.data(), blob.size());
GLint ok; glGetProgramiv(prog, GL_LINK_STATUS, &ok);
if (!ok) { /* delete cache entry, compile from source, re-save */ }
```
A binary load can fail at any time (driver update, different GPU); the source path must
always exist.

## 3. Cache key
Hash of: all shader sources after preprocessing (including the `#define` permutation set),
`GL_VENDOR`, `GL_RENDERER`, `GL_VERSION` and the binary format.
Store per user (app data dir); never ship binaries in the installer.

## 4. Hitching
- Some drivers may still do work the first time a program is used; warm up by drawing with every
  program once during loading and measure whether it helps.
- Compile in parallel with `KHR_parallel_shader_compile`: `glMaxShaderCompilerThreadsKHR`,
  then poll `GL_COMPLETION_STATUS_KHR` instead of blocking on `GL_LINK_STATUS`.
- `GL_NUM_PROGRAM_BINARY_FORMATS` is the number of supported program binary formats; if it is 0
  the implementation offers none, so the source path must keep working.

## Verify
- [ ] Second launch: program creation time drops (log ms per program) and no compiles run.
- [ ] Corrupting a cache file falls back to source cleanly.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: GL_PROGRAM_BINARY_RETRIEVABLE_HINT should be set before glLinkProgram (glProgramParameter); glGetProgramBinary errors when GL_LINK_STATUS is false and GL_PROGRAM_BINARY_LENGTH; glProgramBinary acts as an implicit link, sets GL_LINK_STATUS, and a binary may fail to load after a hardware or software configuration change; GL_NUM_PROGRAM_BINARY_FORMATS (glGet); glProgramBinary GL 4.1 and ES 3.0 (gl.xml); glMaxShaderCompilerThreadsKHR and COMPLETION_STATUS_KHR (KHR_parallel_shader_compile). Removed the unconfirmed driver recompile, Mesa and NVIDIA cache claims.
Method: documentation only; no commands were run.
