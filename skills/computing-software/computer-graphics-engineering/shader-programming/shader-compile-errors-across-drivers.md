---
id: computing-software.computer-graphics-engineering.shader-programming.shader-compile-errors-across-drivers
name: shader-compile-errors-across-drivers
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, shader-compile-errors, glslang, glsl-portability, driver-differences, shader-validation]
level: practitioner
status: docs-checked
description: "Diagnose shader compile and link errors that differ across drivers: GLSL version/extension quirks, strict vs lenient compilers, ES precision, and validating with glslang first."
sources: ["https://github.com/KhronosGroup/glslang", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader compile errors across drivers

## 1. Why the same shader fails differently
OpenGL drivers each contain their own GLSL compiler, so diagnostics and leniency differ between vendors. Vulkan/D3D12 avoid this
by consuming pre-compiled SPIR-V/DXIL.

## 2. Validate with the reference compiler first
```bash
glslangValidator shader.frag                 # GLSL against the declared #version
glslangValidator -S frag --target-env opengl shader.glsl
glslangValidator -V shader.frag              # Vulkan semantics
```
If glslang rejects it, assume some driver will too.

## 3. Common portability failures
| Error / behaviour | Cause | Fix |
|---|---|---|
| `implicit cast from int to float` | `float x = 1;` relies on implicit conversion, which depends on the GLSL version | `1.0` |
| `no default precision for float` (ES) | missing `precision mediump float;` in FS | add precision statement |
| `#version must be first` | anything other than comments and white space before `#version` | put it first |
| `'texture2D': no matching overloaded function` | not part of modern core GLSL | `texture()` |
| unknown extension | `#extension` not supported | check `GL_EXTENSIONS`, use `: enable` + `#ifdef` |
| `uniform block member layout` mismatch | std140 vs shared | explicit `layout(std140)` |
| out-of-range array index | indexing past the end; with a non-constant index the value is undefined | fix the index |
| link error on stage interface | VS/FS interface mismatch | match names/types/locations; use `layout(location=)` |

## 4. Read the info log properly
```c
glGetShaderiv(s, GL_COMPILE_STATUS, &ok);
if (!ok) { glGetShaderiv(s, GL_INFO_LOG_LENGTH, &len); glGetShaderInfoLog(s, len, NULL, buf); }
glGetProgramiv(p, GL_LINK_STATUS, &ok);  // link errors are separate
```
Line numbers count from the start of the concatenated source string; use `#line` after injecting
headers so numbers match the file.

## 5. Process
- Compile all shaders at startup in debug builds and fail loudly.
- CI: validate with glslang for every target (`#version 300 es`, `330 core`, `450`).
- Keep a device matrix (NVIDIA, AMD, Intel, Mesa, Adreno, Mali) and log driver strings with errors.

## Gotchas
- Some drivers report success but produce wrong output for undefined behaviour; compile success is
  not correctness.

## Verify
- [ ] glslang clean for every target profile.
- [ ] All shaders compile on the strictest driver in the device matrix.

## Checked

Checked 2026-10-26 against glslang StandAlone help text (main, 2026-10-23), GLSL 4.60 and GLSL ES 3.00 specifications. Confirmed: glslangValidator options `-S <stage>`, `-V`, `--target-env` (vulkan1.x/opengl), `-E`; the `#version` placement rule (only comments and white space before it); no default float precision in ES fragment shaders; `#extension` directive behaviours; non-constant out-of-range indexing yields undefined values. Removed as unconfirmed: vendor leniency claims (NVIDIA vs others), BOM, ES 2.0 loop restriction row, lazy-compilation remark, 'removed in core 1.40' wording.

Method: documentation only; no commands were run.
