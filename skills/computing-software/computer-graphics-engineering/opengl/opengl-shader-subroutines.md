---
id: computing-software.computer-graphics-engineering.opengl.opengl-shader-subroutines
name: opengl-shader-subroutines
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, shader-subroutines, gluniformsubroutinesuiv, shader-permutations-gl]
level: advanced
status: docs-checked
description: "Use GLSL shader subroutines to switch functions without relinking, set them with glUniformSubroutinesuiv, and weigh them against permutations."
sources: ["https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_subroutine.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glUniformSubroutines.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetSubroutineIndex.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.html", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader subroutines (GL 4.0)

Subroutines are GLSL function pointers chosen per draw from the host. Desktop GL 4.0 and later; subroutines are removed from the GLSL
used for Vulkan and SPIR-V (GL_KHR_vulkan_glsl).

## GLSL
```glsl
subroutine vec3 ShadeModel(vec3 n, vec3 l, vec3 v);
layout(index = 0) subroutine(ShadeModel) vec3 lambert(vec3 n, vec3 l, vec3 v) { return vec3(max(dot(n,l),0)); }
layout(index = 1) subroutine(ShadeModel) vec3 toon   (vec3 n, vec3 l, vec3 v) { return vec3(step(0.5, dot(n,l))); }
layout(location = 0) subroutine uniform ShadeModel uShade;
void main() { color = vec4(uShade(N, L, V), 1); }
```

## Host
```c
glUseProgram(prog);
GLuint idx[] = { 1 };     // one entry per active subroutine uniform location in this stage
glUniformSubroutinesuiv(GL_FRAGMENT_SHADER, 1, idx);
```
Without explicit `index`/`location`, query `glGetSubroutineIndex(prog, GL_FRAGMENT_SHADER, "toon")`
and `glGetSubroutineUniformLocation`. `count` must equal
`GL_ACTIVE_SUBROUTINE_UNIFORM_LOCATIONS` for that stage, and all must be set.

## The big gotcha: state is lost on glUseProgram
Per ARB_shader_subroutine, calling `glUseProgram` resets the subroutine uniforms of all stages
to arbitrarily chosen default functions, so selections do not survive a program switch. You must
call `glUniformSubroutinesuiv` after every program bind, before drawing. This kills batching code that sorts by program and assumes
state persists.

## Performance reality
- Compile-time permutations (`#define` variants) or a uniform-controlled `switch` are the usual
  alternatives; nothing in the specification says subroutines are faster than either.
- Use subroutines where host-side selection without relinking matters; measure before shipping
  them in hot paths.

## Verify
- [ ] Switching subroutine changes output without relinking; KHR_debug clean.
- [ ] GPU timing equal to or better than the uniform-switch alternative on target hardware.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: glUniformSubroutinesuiv count must equal GL_ACTIVE_SUBROUTINE_UNIFORM_LOCATIONS for the stage of the current program and indices must be below GL_ACTIVE_SUBROUTINES; glUseProgram resets subroutine uniforms to arbitrarily chosen defaults (ARB_shader_subroutine); location and index layout qualifiers and the removal of subroutines for Vulkan-targeted GLSL (GLSL 4.60); GL 4.0 (gl.xml). Removed the unconfirmed GLES/WebGL and driver-implementation claims.
Method: documentation only; no commands were run.
