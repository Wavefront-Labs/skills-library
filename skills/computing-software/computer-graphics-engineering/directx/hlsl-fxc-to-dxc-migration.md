---
id: computing-software.computer-graphics-engineering.directx.hlsl-fxc-to-dxc-migration
name: hlsl-fxc-to-dxc-migration
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, hlsl, fxc-to-dxc, dxc, shader-model-5-to-6]
level: advanced
status: docs-checked
description: "Migrate shaders from FXC (SM 5.x DXBC) to DXC (SM 6.x DXIL): command-line mapping, behaviour differences, D3D11 limits, warnings and validation."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3dtools/dx-graphics-tools-fxc-syntax", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/include/dxc/Support/HLSLOptions.td", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/docs/ReleaseNotes.md", "https://github.com/microsoft/DirectXShaderCompiler/blob/main/include/dxc/dxcapi.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FXC to DXC migration

FXC targets Shader Models up to 5.1 (for example `cs_5_1`, per the fxc syntax page) and produces DXBC.
DXC (Clang/LLVM based) compiles SM 6.0+ to DXIL (and SPIR-V). Keep FXC for D3D11 paths.

## Command-line mapping
| FXC | DXC |
|---|---|
| `/T ps_5_0` | `-T ps_6_0` (or higher) |
| `/E main` | `-E main` |
| `/Fo out.cso` | `-Fo out.cso` |
| `/Zi /Fd` | `-Zi -Fd out.pdb` (or `-Qembed_debug`) |
| `/O3` (FXC default is `/O1`) | `-O3` |
| `/Gec` | (unsupported in DXC) |
| `/WX` | `-WX` |
| `/D NAME=1` | `-D NAME=1` |
| `/Qstrip_reflect` | `-Qstrip_reflect` |
API: `D3DCompile` -> `IDxcCompiler3::Compile` (created with `DxcCreateInstance`); a default include
handler comes from `IDxcUtils::CreateDefaultIncludeHandler`.

## Behaviour differences
- `-enable-16bit-types` enables 16-bit types and disables `min16*` types; results can change in
  precision-sensitive code.
- Shader performance can change either way after migration: profile per pass.
- Default matrix packing is column-major in both; `-Zpr`/`-Zpc` exist in both compilers.
- DXC defaults to HLSL 2021 (`-HV`), which changes vector `&&`, `||` and `?:` semantics (see the HLSL 2021 skill).

## Validation and signing
DXIL is validated when compiled. Since DXC 1.8.2505 the compiler always uses its internal validator
instead of searching for an external `dxil.dll` (older releases looked for `dxil.dll` next to
`dxcompiler.dll`). `-Vd` disables validation; use it only for testing. Ship compiled blobs, not the
compiler, where possible.

## Gotchas
- Shader reflection goes through `IDxcUtils::CreateReflection` (usable with `ID3D12ShaderReflection`).
- Debug info: `-Zi` with `-Fd <file>` writes the PDB; `-Qembed_debug` embeds it.

## Verify
- [ ] Every shader compiles with DXC `-WX`; image diffs vs FXC builds within tolerance; GPU timings compared per pass.

## Checked

2026-10-26. Checked against the Microsoft Learn fxc syntax page (supported targets up to _5_1, /O1 default, /Gec, /Zpr, /Qstrip_reflect,
/WX, /Fd), include/dxc/Support/HLSLOptions.td (-HV default 2021, -Zpr/-Zpc, -Qembed_debug, -Vd, Gec marked unsupported,
-enable-16bit-types), docs/ReleaseNotes.md (internal validator since 1.8.2505) and include/dxc/dxcapi.h
(CreateReflection, CreateDefaultIncludeHandler) in the DXC repository (commits to 2026-10). Removed the unconfirmed
claims about FXC being slow, DXC strictness examples, unroll heuristics, FXC effects support and the old dxil.dll
signing requirement.
Method: documentation only; no commands were run.
