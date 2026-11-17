---
id: computing-software.computer-graphics-engineering.directx.hlsl-2021-language-features
name: hlsl-2021-language-features
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, hlsl, hlsl-2021, hlsl-templates, short-circuit-operators]
level: advanced
status: docs-checked
description: "Adopt HLSL 2021 in DXC: templates, operator overloading, bitfields, logical-operator short-circuiting changes, strict casting rules, and migration pitfalls."
sources: ["https://github.com/microsoft/DirectXShaderCompiler/wiki/HLSL-2021", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/ReleaseNotes.md", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/include/dxc/Support/HLSLOptions.td"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HLSL 2021

DXC's default language version is HLSL 2021 (enabled by default since DXC 1.7.2308; the `-HV`
option accepts 2016, 2017, 2018 and 2021, so older code may need `-HV 2018`).

## New features
**Templates**
```hlsl
template<typename T>
T Square(T x) { return x * x; }

template<typename C, typename W>
struct Blender {
  C src; W weight;
  C scaled() { return src * weight; }
};
```
**Operator overloading** (restricted to non-assignment arithmetic, boolean and bitwise operators):
```hlsl
struct Complex { float re, im;
  Complex operator*(Complex b) { Complex r; r.re = re*b.re - im*b.im; r.im = re*b.im + im*b.re; return r; } };
```
**Bitfields** in structs: `struct Packed { uint a : 10; uint b : 10; uint c : 12; };`
**Member functions** on structs.

## Breaking changes
1. **Logical operators short-circuit and require scalars**: `&&`, `||`, `?:` on vectors are errors.
   Use `and(a, b)`, `or(a, b)`, `select(cond, a, b)` for element-wise vector logic.
   ```hlsl
   // 2018: float3 r = (mask > 0) ? a : b;
   float3 r = select(mask > 0, a, b);
   bool3 both = and(x > 0, y > 0);
   ```
   Short-circuiting also means side effects (function calls) on the right side may not run.
2. C++-style function overloading: a struct is no longer implicitly cast to another struct with the same
   member layout, so such conversions (and calls relying on them) become errors; add an explicit cast
   or write a dedicated overload.

## Migration
- Compile the codebase with `-HV 2021`; fix errors (mostly vector ternaries/logic).
- Keep `-HV 2018` temporarily for third-party shaders while migrating.
- `and()`, `or()` and `select()` are available in all language modes since DXC 1.7.2212.
- Templates replace macro-heavy generic code (e.g. reduction helpers for float/uint).

## Gotchas
- The DXC project describes HLSL 2021 as beta-quality; check open issues labelled `hlsl2021`.
- HLSL 2021 is a DXC compiler feature; keep FXC-compiled (D3D11) shaders on the FXC feature set.

## Verify
- [ ] Entire shader library compiles with `-HV 2021 -WX`; image diffs unchanged after migration.

## Checked

2026-10-26. Checked against the DXC wiki page "HLSL 2021", docs/ReleaseNotes.md (1.7.2212 intrinsics in all modes, 1.7.2308
default) and include/dxc/Support/HLSLOptions.td (-HV help text: default is 2021) in microsoft/DirectXShaderCompiler
(commits to 2026-10). Confirmed: templates, bitfields, operator-overloading restriction, vector logic operator error
and short-circuit rules, struct implicit-cast change, and()/or()/select(). Removed the unconfirmed for-loop scope
and implicit-truncation claims, the spirv-val advice and the RingBuffer template example.
Method: documentation only; no commands were run.
