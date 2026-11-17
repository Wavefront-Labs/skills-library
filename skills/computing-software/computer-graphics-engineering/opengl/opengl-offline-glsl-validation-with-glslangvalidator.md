---
id: computing-software.computer-graphics-engineering.opengl.opengl-offline-glsl-validation-with-glslangvalidator
name: opengl-offline-glsl-validation-with-glslangvalidator
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-shader-programs, glslangvalidator, shader-ci, glsl-lint]
level: practitioner
status: docs-checked
description: "Catch GLSL errors in CI before they hit drivers: the Khronos glslang reference validator, stage inference, defines, includes and linking stages."
sources: ["https://github.com/KhronosGroup/glslang", "https://github.com/KhronosGroup/glslang/blob/main/README.md", "https://github.com/KhronosGroup/glslang/blob/main/StandAlone/StandAlone.cpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline GLSL validation with glslang

glslang is the Khronos reference validator and GLSL/ESSL front end. Run it in CI on every shader so
portability errors fail the build, not the user. The command-line tool's usage text reads
`glslang [option]... [file]...`; older distributions call it glslangValidator, so check what your
install provides and use that name in the commands below.

## Basic use
```sh
glslang shader.vert                    # stage inferred from extension
glslang -S frag lighting.glsl          # explicit stage instead of the file extension
glslang -DUSE_SHADOWS=1 -DMAX_LIGHTS=16 -I shaders/include shader.frag
glslang -l prog.vert prog.frag        # link all input files into one module
```
- Extension to stage: `.vert .tesc .tese .geom .frag .comp .rgen .rint .rahit .rchit .rmiss .rcall
  .mesh .task`; names may also end `.<stage>.glsl` or `.<stage>.hlsl`.
- `-D<name[=def]>` defines a macro; `-I<dir>` adds an include path.
- `--stdin` reads from standard input and requires `-S`.
- `--client opengl100` is the same as `-G100` and defines `GL_SPIRV`; SPIR-V output needs client
  semantics (`-G`/`-V` or `--client`).

## CI script
```sh
set -e
for f in $(git ls-files 'shaders/*.vert' 'shaders/*.frag' 'shaders/*.comp'); do
  for variant in "" "-DUSE_SHADOWS=1" "-DSKINNED=1"; do
    glslang $variant -I shaders/include "$f" > /dev/null || { echo "FAIL $f $variant"; exit 1; }
  done
done
```
Validate every permutation you ship; errors often hide behind `#ifdef`. A shell loop fails the build
on any non-zero exit.

## Gotchas
- A pass is not a guarantee for a given driver; keep a runtime compile test on your lowest target
  device.

## Verify
- [ ] CI fails on a deliberately broken shader; all variants validated in the pipeline log.

## Checked

2026-11-01. Confirmed in glslang README.md (reference validator, GLSL/ESSL front end) and StandAlone.cpp (usage text,
options -S, -D, -I, -l, -G, --client, --stdin, extension to stage table). Removed: vendor behaviour comparisons,
ES-rule specifics, `--target-env opengl` with spirv-val advice, limit and extension-query advice, exit-code claim.

Method: documentation only; no commands were run.
