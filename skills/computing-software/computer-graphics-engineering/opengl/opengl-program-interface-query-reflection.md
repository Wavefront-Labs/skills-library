---
id: computing-software.computer-graphics-engineering.opengl.opengl-program-interface-query-reflection
name: opengl-program-interface-query-reflection
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, program-interface-query, glgetprograminterface, shader-reflection-gl]
level: advanced
status: docs-checked
description: "Reflect linked OpenGL programs with glGetProgramInterfaceiv/glGetProgramResourceiv to enumerate uniforms, blocks, SSBOs and attributes."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetProgramResource.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetProgramInterface.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetProgramResourceName.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetProgramResourceIndex.xhtml", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_gl_spirv.txt", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Program interface queries (GL 4.3)

Use reflection to build material editors, validate CPU struct layouts against shader blocks,
and auto-bind resources.

## Enumerate active uniforms (not in blocks)
```c
GLint n = 0;
glGetProgramInterfaceiv(prog, GL_UNIFORM, GL_ACTIVE_RESOURCES, &n);
const GLenum props[] = { GL_NAME_LENGTH, GL_TYPE, GL_LOCATION, GL_BLOCK_INDEX, GL_ARRAY_SIZE };
for (GLint i = 0; i < n; ++i) {
    GLint v[5]; glGetProgramResourceiv(prog, GL_UNIFORM, i, 5, props, 5, NULL, v);
    if (v[3] != -1) continue;                       // member of a UBO, skip here
    std::string name(v[0], '\0');
    glGetProgramResourceName(prog, GL_UNIFORM, i, v[0], NULL, name.data());
    name.pop_back();                                 // length includes the NUL
    printf("%s type=0x%x loc=%d size=%d\n", name.c_str(), v[1], v[2], v[4]);
}
```

## Interfaces you can query
| Interface | Gives |
|---|---|
| `GL_PROGRAM_INPUT` / `GL_PROGRAM_OUTPUT` | vertex attributes, fragment outputs (`GL_LOCATION`) |
| `GL_UNIFORM_BLOCK` | UBOs: `GL_BUFFER_BINDING`, `GL_BUFFER_DATA_SIZE`, active variables |
| `GL_SHADER_STORAGE_BLOCK` | SSBOs: same properties |
| `GL_UNIFORM` / `GL_BUFFER_VARIABLE` | members: `GL_OFFSET`, `GL_ARRAY_STRIDE`, `GL_MATRIX_STRIDE`, `GL_IS_ROW_MAJOR` |
| `GL_ATOMIC_COUNTER_BUFFER`, `GL_TRANSFORM_FEEDBACK_VARYING`, subroutines | as named |

## Validate a CPU struct against a UBO
Query `GL_OFFSET` of each member via `glGetProgramResourceIndex(prog, GL_UNIFORM, "Frame.viewProj")`
and compare with `offsetof(FrameCPU, viewProj)` at startup; assert on mismatch. Catches
std140 padding bugs (vec3 followed by float, arrays of float with 16-byte stride) immediately.

## Gotchas
- Only **active** resources appear; unused uniforms are gone, so tools must tolerate missing names.
- `glGetProgramResourceIndex` also matches an array's name with `[0]` appended, so handle both
  `"lights"` and `"lights[0]"` spellings when matching names.
- For SPIR-V programs (`ARB_gl_spirv`) it is implementation-dependent whether names are
  reported; when they are not, name-based queries return `GL_INVALID_INDEX` or -1 and every
  name has length 1 (the null character). Use explicit bindings and locations instead.

## Verify
- [ ] Reflection dump lists every expected binding; offset assertion passes for all shared structs.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed: property and interface tables for GL_UNIFORM, GL_UNIFORM_BLOCK, GL_SHADER_STORAGE_BLOCK, GL_BUFFER_VARIABLE, GL_PROGRAM_INPUT and OUTPUT, GL_ATOMIC_COUNTER_BUFFER, GL_TRANSFORM_FEEDBACK_VARYING and subroutine uniforms (glGetProgramResource, glGetProgramInterface); GL_NAME_LENGTH includes the terminating null; GL_ACTIVE_RESOURCES counts only the active resource list; glGetProgramResourceIndex accepts a name with [0] appended; GL 4.3 (gl.xml); SPIR-V name reflection behaviour (ARB_gl_spirv). Removed the unconfirmed struct-array enumeration claim.
Method: documentation only; no commands were run.
