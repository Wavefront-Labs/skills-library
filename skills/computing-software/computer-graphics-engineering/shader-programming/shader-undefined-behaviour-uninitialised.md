---
id: computing-software.computer-graphics-engineering.shader-programming.shader-undefined-behaviour-uninitialised
name: shader-undefined-behaviour-uninitialised
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, undefined-behavior-shaders, uninitialized-variables, nan, derivatives, robustness, driver-differences]
level: practitioner
status: docs-checked
description: "Avoid undefined behaviour in shaders: uninitialised variables, out-of-bounds indexing, divide by zero, NaN propagation, derivatives in divergent flow and driver-dependent results."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://www.w3.org/TR/WGSL/#uniformity", "https://docs.vulkan.org/spec/latest/chapters/shaders.html#shaders-robust-buffer-access2", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GLSL_EXT_demote_to_helper_invocation.txt", "https://github.com/KhronosGroup/Vulkan-ValidationLayers/blob/main/docs/gpu_validation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uninitialised variables and undefined behaviour in shaders

Shaders that "work on my GPU" often rely on undefined behaviour that another vendor (or the next
driver) handles differently.

## 1. Uninitialised locals and outputs
- GLSL/HLSL locals are not zero-initialised; the value you read is whatever the compiler left.
- Fragment outputs not written in some paths are undefined: always write every output.
- Struct members partially written then returned: initialise the whole struct (`S s = S(0);` /
  `(S)0`).
WGSL `var` declarations without an initializer start as the zero value of their type (defined behaviour).

## 2. Out-of-bounds access
- Arrays indexed past the end: undefined in GLSL/HLSL (may return 0, garbage, or crash).
- Buffers: GLSL says out-of-bounds reads return undefined values (possibly from other variables or zero) and writes may be
  discarded or overwrite other variables; defined behaviour needs Vulkan robustness (`robustBufferAccess`,
  `robustBufferAccess2`, or pipeline robustness). Out-of-range bindless descriptor indices are undefined.
- Clamp indices from data (`min(i, count - 1)`) at trust boundaries.

## 3. Arithmetic
- Guard divisors: GLSL leaves results undefined where a ratio's divisor is 0 for the trigonometric functions, and integer
  division overflow gives an undefined value.
- `pow(x, y)`: undefined if x < 0, or if x = 0 and y <= 0.
- `log`: undefined if x <= 0; `atan(y, x)`: undefined if x and y are both 0; `acosh`: undefined if x < 1.
- `normalize(vec3(0))` and similar give no usable value; guard the input.
- NaNs propagate through TAA/bloom history and turn the screen black; guard sources.

## 4. Derivatives in non-uniform control flow
Implicit derivatives (`texture()` with implicit LOD, `dFdx`, `fwidth`) are undefined within non-uniform control flow (GLSL). WGSL enforces uniformity analysis and rejects them. Fixes: hoist the sample above the
branch, use `textureLod`/`textureGrad`, or compute derivatives up front.

## 5. Helper invocations and discard
After `discard` control flow exits the shader, and subsequent implicit or explicit derivatives are undefined when that
control flow is non-uniform (GLSL 4.60). The `demote` keyword (`GL_EXT_demote_to_helper_invocation`) turns the invocation
into a helper invocation instead, so it keeps taking part in derivative computation.

## 6. Tooling
- GPU-assisted validation in the Vulkan validation layers inspects GPU resources and instruments shaders to validate
  how invocations access descriptors at run time.
- Test on more than one vendor; differences can signal undefined behaviour.

## Verify
- [ ] Every output and local initialised in every path.
- [ ] GPU-assisted validation clean; NaN check pass (isnan visualisation) clean.

## Checked

Checked 2026-10-26 against GLSL 4.60 specification, WGSL spec (gpuweb main), Vulkan-Docs shaders chapter (main, 2026-10-23), Vulkan-ValidationLayers docs/gpu_validation.md, GL_EXT_demote_to_helper_invocation. Confirmed: GLSL out-of-bounds access text, `pow`/`log`/`atan`/`acosh` undefined-argument rules, overflow in integer division, implicit derivatives undefined in non-uniform control flow, `discard` derivative rule; WGSL zero value for uninitialised `var`; `demote` keyword and extension name; robust buffer access 2 in the Vulkan spec; GPU-AV description. Removed as unconfirmed: vendor-specific uninitialised-value behaviour, the DXC `-Wuninitialized` remark, D3D12 out-of-bounds-returns-zero, 'integer division by zero can hang', the `acos`/`sqrt` NaN lines and the VK_VALIDATION_FEATURE enum name.

Method: documentation only; no commands were run.
