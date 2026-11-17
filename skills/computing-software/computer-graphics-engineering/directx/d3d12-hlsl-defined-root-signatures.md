---
id: computing-software.computer-graphics-engineering.directx.d3d12-hlsl-defined-root-signatures
name: d3d12-hlsl-defined-root-signatures
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, root-signature, hlsl-root-signature, rootsig-1-1, dxc-rootsig]
level: practitioner
status: docs-checked
description: "Define D3D12 root signatures in HLSL with the [RootSignature] attribute or a standalone rootsig target, compile with DXC, and extract them at runtime."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/specifying-root-signatures-in-hlsl", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/creating-a-root-signature", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/root-signature-version-1-1", "https://microsoft.github.io/DirectX-Specs/d3d/HLSL_SM_6_6_DynamicResources.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root signatures defined in HLSL

Keeping the root signature next to the shaders keeps register bindings and layout in one place,
and lets shader authors change bindings without C++ edits.

## Syntax
```hlsl
#define MyRS \
    "RootFlags(ALLOW_INPUT_ASSEMBLER_INPUT_LAYOUT | DENY_HULL_SHADER_ROOT_ACCESS), " \
    "RootConstants(num32BitConstants=16, b0), " \
    "CBV(b1, flags=DATA_STATIC_WHILE_SET_AT_EXECUTE), " \
    "DescriptorTable(SRV(t0, numDescriptors=unbounded, flags=DESCRIPTORS_VOLATILE), visibility=SHADER_VISIBILITY_PIXEL), " \
    "StaticSampler(s0, filter=FILTER_ANISOTROPIC, maxAnisotropy=16, addressU=TEXTURE_ADDRESS_WRAP, addressV=TEXTURE_ADDRESS_WRAP)"

[RootSignature(MyRS)]
float4 PSMain(VSOut i) : SV_Target { ... }
```
For SM 6.6 bindless the spec uses `"RootFlags(CBV_SRV_UAV_HEAP_DIRECTLY_INDEXED | SAMPLER_HEAP_DIRECTLY_INDEXED)"`.
`borderColor` in a static sampler is restricted to the `D3D12_STATIC_BORDER_COLOR` enum names.

## Compile
```sh
# documented fxc forms (embedded signature; standalone blob from a #define; strip and combine):
fxc /T ps_5_1 shaderWithRootSig.hlsl /Fo rs1.fxo
fxc /T rootsig_1_1 MyRS1.hlsl /E MyRS1 /Fo MyRS1.fxo
fxc /dumpbin rs1.fxo /Qstrip_rootsignature /Fo rs1.stripped.fxo
# dxc also has -Qstrip_rootsignature (must be used with -Fo); other dxc options are not covered by the pages read
```
Newer HLSL compilers compile root signatures at version 1.1 by default; old compilers support only 1.0, and 1.1
signatures do not work on operating systems without root signature 1.1 support.

## Use at runtime
- PSO creation: if you pass a root signature, it is validated against every shader and replaces any signature
  embedded in the shaders. If you do not pass one, every shader must contain a root signature and they must
  match; that signature is given to the driver. Setting a PSO does not change the command list's root
  signature: you still call `SetGraphicsRootSignature` or `SetComputeRootSignature`.
- `CreateRootSignature` takes a serialized root signature (for example the `rootsig_1_1` blob above).
- Reflect parameters: `D3D12CreateRootSignatureDeserializer` can be called on a serialized
  root signature or on a compiled shader that contains one, to map parameter indices to names in your binding code
  (use the versioned deserializer for 1.1 signatures).

## Rules
- The root signature should be identical across all shaders of one PSO.
- Use version 1.1 syntax for the range and descriptor `flags`; a 1.0 signature behaves like
  `DESCRIPTORS_VOLATILE | DATA_VOLATILE`.
- Keep the definitions in a shared header so C++ and HLSL agree on root parameter order.

## Verify
- [ ] PSO creation succeeds with a null root signature in the PSO description; the debug layer reports no root
  signature mismatch between stages.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Specifying root signatures in HLSL", "Creating a root signature",
"Root signature version 1.1" (MicrosoftDocs/win32, last commit 2026-10-08), DirectX-Specs HLSL SM 6.6 dynamic
resources spec (2026-10-22), and the DirectXShaderCompiler `HLSLOptions.td` for `-Qstrip_rootsignature`. Confirmed:
clause syntax and parameter names, the `RootFlags` names for SM 6.6, PSO root-signature replacement rules, 1.1 default
compilation, 1.0 equals fully volatile. Removed unconfirmed claims: creating a root signature straight from a
whole shader blob "because the runtime finds RTS0", and the dxc wiki source link (not read).
Method: documentation only; no commands were run.
