---
id: computing-software.computer-graphics-engineering.opengl.opengl-shader-compile-link-and-info-logs
name: opengl-shader-compile-link-and-info-logs
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, glsl-programs, shader-compilation, program-linking, info-log, glsl-version, khr-parallel-shader-compile, shader-includes]
level: practitioner
status: docs-checked
description: "Compile and link GLSL programs robustly: info logs with file:line mapping, version/define injection, parallel compilation, and validating interface mismatches."
sources: ["https://registry.khronos.org/OpenGL/extensions/KHR/KHR_parallel_shader_compile.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glValidateProgram.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetUniformLocation.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://github.com/KhronosGroup/glslang"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL shader compile, link and info logs

**Goal:** shader errors that point at the right file and line, programs that fail loudly
instead of rendering black, and compile time that does not freeze the first frame.

## 1. Compile with prologue injection
```c
GLuint compile(GLenum stage, const char* src, const char* defines, const char* name) {
    const char* parts[] = { "#version 460 core\n", defines, "#line 1\n", src };
    GLuint s = glCreateShader(stage);
    glShaderSource(s, 4, parts, NULL);
    glCompileShader(s);
    GLint ok; glGetShaderiv(s, GL_COMPILE_STATUS, &ok);
    if (!ok) {
        GLint n; glGetShaderiv(s, GL_INFO_LOG_LENGTH, &n);
        char* log = malloc(n); glGetShaderInfoLog(s, n, NULL, log);
        fprintf(stderr, "[%s]\n%s", name, log);   // the log format is implementation-defined
    }
    return s;
}
```
- `#version` must be the first non-comment line; inject defines **after** it.
- `#line 1` resets numbering so log lines match the source file. For an `#include`
  preprocessor, emit `#line N FILEID` per chunk and keep a FILEID→path table.

## 2. Link and check
```c
GLuint p = glCreateProgram();
glAttachShader(p, vs); glAttachShader(p, fs);
glLinkProgram(p);
glGetProgramiv(p, GL_LINK_STATUS, &ok);   // print glGetProgramInfoLog on failure
glDetachShader(p, vs); glDeleteShader(vs);    // shader objects no longer needed
```
Link errors catch interface mismatches between stages (a statically referenced input with no matching output,
or differing types). Read the info log even on success in debug builds: it may contain warnings.

## 3. Don't stall the first frame
- `KHR_parallel_shader_compile`: `glMaxShaderCompilerThreadsKHR(0xFFFFFFFF)`, issue all
  compiles/links up front, then poll `GL_COMPLETION_STATUS_KHR` (`glGetShaderiv`/`glGetProgramiv`) and read
  `GL_COMPILE_STATUS`/`GL_LINK_STATUS` once it is true. The extension's initial thread-count state is 0xFFFFFFFF
  (an implementation-specific maximum).
- Pair with program binary caching for subsequent runs.

## 4. Hot reload
Watch shader files; on change compile into a *new* program, swap only if linking succeeds,
so a typo keeps the old shader running and prints the log.

## Gotchas
- Unused uniforms/attributes are optimised away: `glGetUniformLocation` returns -1. Not an
  error — but explains "my uniform does nothing".
- Validate shaders offline with `glslangValidator` (glslang) in CI as a second compiler.
- `glValidateProgram` checks against *current state* (e.g. two samplers of different
  types on one unit); call it before a draw in debug builds, not right after link.

## Verify
- [ ] A deliberate syntax error prints `file:line` matching your editor.
- [ ] CI runs `glslangValidator` on every shader permutation.
- [ ] Startup with parallel compile shows no long single-frame hitch in a frame-time graph.

## Checked

Date: 2026-10-26. Documentation: KHR_parallel_shader_compile extension text, GLSL 4.60 spec, OpenGL 4.6 core spec, gl4 reference pages for glValidateProgram and glGetUniformLocation, glslang README. Confirmed: `glMaxShaderCompilerThreadsKHR` (0 = no parallel compile, 0xFFFFFFFF = implementation maximum, which is also the initial state) and `GL_COMPLETION_STATUS_KHR` for shaders and programs; `#version` must precede everything but comments and white space; `#line line` resets the line number; LinkProgram checks stage-interface mismatches; `glValidateProgram` validates against the current state and writes the info log; `glGetUniformLocation` returns -1 for inactive uniforms. Removed: vendor log formats, the claim that LINK_STATUS blocks, GLES `#version 300 es` note, vendor GLSL leniency claim.

Method: documentation only; no commands were run.
