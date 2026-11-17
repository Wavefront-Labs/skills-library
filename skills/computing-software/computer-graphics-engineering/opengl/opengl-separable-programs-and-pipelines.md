---
id: computing-software.computer-graphics-engineering.opengl.opengl-separable-programs-and-pipelines
name: opengl-separable-programs-and-pipelines
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, separable-programs, program-pipelines, glcreateshaderprogramv, arb-separate-shader-objects]
level: advanced
status: docs-checked
description: "Mix and match vertex and fragment stages in OpenGL with separable programs and program pipeline objects: interface matching, uniforms, validation."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glCreateShaderProgram.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glUseProgramStages.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBindProgramPipeline.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glValidateProgramPipeline.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glProgramParameter.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_separate_shader_objects.txt", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Separable programs and program pipelines

**Goal:** link each stage on its own (GL 4.1 / ES 3.1 / `ARB_separate_shader_objects`) and
combine stages at bind time, cutting the N x M program explosion of vertex x fragment variants.

## 1. Create
```c
GLuint vs = glCreateShaderProgramv(GL_VERTEX_SHADER, 1, &vsSrc);   // compile+link, SEPARABLE set
GLuint fs = glCreateShaderProgramv(GL_FRAGMENT_SHADER, 1, &fsSrc);
// check GL_LINK_STATUS + info log on each
GLuint pipe; glCreateProgramPipelines(1, &pipe);
glUseProgramStages(pipe, GL_VERTEX_SHADER_BIT, vs);
glUseProgramStages(pipe, GL_FRAGMENT_SHADER_BIT, fs);
glBindProgramPipeline(pipe);      // only used when NO program is bound with glUseProgram
```
For manual linking set `glProgramParameteri(prog, GL_PROGRAM_SEPARABLE, GL_TRUE)` before
`glLinkProgram`.

## 2. Interface rules
- To use a built-in output such as `gl_Position` in a separable program the shader must
  redeclare the block: `out gl_PerVertex { vec4 gl_Position; };`; the program fails to link if
  a member is used that the redeclaration lacks.
- Match varyings **by location**: an output matches an input by name and type or by identical
  `location` and type, so declare `layout(location = 0) out vec3 vNormal;` /
  `layout(location = 0) in vec3 vNormal;` in both stages.
- Uniforms belong to a program: set with `glProgramUniform*(prog, loc, ...)` (no bind needed)
  or share via UBOs/SSBOs bound to fixed binding points.

## 3. Validate
`glValidateProgramPipeline(pipe)`, then query `GL_VALIDATE_STATUS` with `glGetProgramPipelineiv`
and read the log with `glGetProgramPipelineInfoLog`.

## Gotchas
- `glUseProgram(p)` with a non-zero program overrides the bound pipeline; call
  `glUseProgram(0)` when switching to pipelines.

## Verify
- [ ] Pipeline validation passes; RenderDoc shows the expected program per stage.
- [ ] Swapping only the fragment stage changes shading without relinking.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glCreateShaderProgramv sets GL_PROGRAM_SEPARABLE; GL_PROGRAM_SEPARABLE must be set before linking and starts GL_FALSE (glProgramParameter); glUseProgramStages bit names and GL_ALL_SHADER_BITS; a bound pipeline has no effect while a program from glUseProgram is current (glBindProgramPipeline); GL_VALIDATE_STATUS and glValidateProgramPipeline; separable-program gl_PerVertex redeclaration rule, interface matching by name or location, glProgramUniform* (ARB_separate_shader_objects); GL 4.1 (gl.xml). Removed the unconfirmed optimisation and SPIR-V claims.
Method: documentation only; no commands were run.
