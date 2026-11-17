---
id: computing-software.computer-graphics-engineering.directx.d3d12-executeindirect-command-signatures
name: d3d12-executeindirect-command-signatures
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12, command-list, executeindirect, command-signature, indirect-arguments, gpu-culling, count-buffer, gpu-driven-rendering]
level: advanced
status: docs-checked
description: "Drive Direct3D 12 draws from the GPU with ExecuteIndirect: command signatures with root constants or VB views, compute-culled argument buffers and a count buffer."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/indirect-drawing", "https://microsoft.github.io/DirectX-Specs/d3d/IndirectDrawing.html", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-executeindirect", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_indirect_argument_type"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 ExecuteIndirect and command signatures

**Goal:** a compute pass decides what to draw (culling, LOD) and writes draw arguments;
one `ExecuteIndirect` issues them all with per-draw constants.

## 1. Define the argument layout
```cpp
struct IndirectCmd {
    UINT objectIndex;                              // root constant (32-bit)
    D3D12_DRAW_INDEXED_ARGUMENTS draw;             // IndexCountPerInstance, InstanceCount, StartIndex, BaseVertex, StartInstance
};
D3D12_INDIRECT_ARGUMENT_DESC args[2] = {};
args[0].Type = D3D12_INDIRECT_ARGUMENT_TYPE_CONSTANT;
args[0].Constant = { /*RootParameterIndex*/ 0, /*DestOffsetIn32BitValues*/ 0, /*Num32BitValuesToSet*/ 1 };
args[1].Type = D3D12_INDIRECT_ARGUMENT_TYPE_DRAW_INDEXED;   // the draw/dispatch entry must come last
D3D12_COMMAND_SIGNATURE_DESC sd{ sizeof(IndirectCmd), 2, args, 0 };
device->CreateCommandSignature(&sd, rootSig.Get(), IID_PPV_ARGS(&cmdSig));
```
The root signature must be specified if and only if the command signature changes a root argument. Arguments for one
draw or dispatch are tightly packed in the argument buffer, but the app may use any byte stride between commands
(`ByteStride` must be 4-byte aligned).

Argument types: `DRAW`, `DRAW_INDEXED`, `DISPATCH`, `VERTEX_BUFFER_VIEW`, `INDEX_BUFFER_VIEW`, `CONSTANT`,
`CONSTANT_BUFFER_VIEW`, `SHADER_RESOURCE_VIEW`, `UNORDERED_ACCESS_VIEW`, plus `DISPATCH_MESH` (mesh shader
spec), `DISPATCH_RAYS` (raytracing spec) and `INCREMENTING_CONSTANT` (in `d3d12.h`).

## 2. Fill from compute
```hlsl
AppendStructuredBuffer<IndirectCmd> OutCmds : register(u0);   // counter = draw count
[numthreads(64,1,1)] void Cull(uint id : SV_DispatchThreadID) {
    if (id >= ObjectCount || !FrustumVisible(id)) return;
    IndirectCmd c; c.objectIndex = id; c.draw = Meshes[Objects[id].mesh].draw;
    OutCmds.Append(c);
}
```
Reset the UAV counter to 0 each frame (for example with a copy from a zeroed buffer).

## 3. Execute with a count buffer
```cpp
// argument buffer and count buffer: UNORDERED_ACCESS -> INDIRECT_ARGUMENT
cmd->ExecuteIndirect(cmdSig.Get(), MaxDraws, argBuf.Get(), 0, countBuf.Get(), countOffset);
```
With a non-null count buffer, `MaxCommandCount` is a maximum: the executed count is
`min(MaxCommandCount, UINT32 read from the count buffer at CountBufferOffset)`. With a null count buffer,
`MaxCommandCount` is the exact count.

## Gotchas
- The debug layer errors if the argument buffer or count buffer is not in `D3D12_RESOURCE_STATE_INDIRECT_ARGUMENT`.
  Offsets must be 4-byte aligned and the range implied by `MaxCommandCount` and the stride must fit the buffer.
- The command list's root signature must match the one given to the command signature.
- `ExecuteIndirect` inside a bundle is allowed only with a null count buffer and a command signature that has
  exactly one operation (so no root-argument or VB/IB changes).
- `SV_InstanceID` does not carry the object index you want: pass it as a root constant (as above) or, with
  Shader Model 6.8, read `StartInstanceLocation` through `SV_StartInstanceLocation`.

## Verify
- [ ] A capture shows one ExecuteIndirect expanding into the expected visible draws.
- [ ] Debug view: culled objects absent; count buffer value equals the visible count.
- [ ] CPU time independent of object count.

## Checked
Date: 2026-10-26. Documentation: Microsoft Learn "Indirect drawing", `ID3D12GraphicsCommandList::ExecuteIndirect`,
`D3D12_INDIRECT_ARGUMENT_TYPE` (MicrosoftDocs/win32 and sdk-api, last commit 2026-10-08), DirectX-Specs
IndirectDrawing, MeshShader, Raytracing and HLSL Shader Model 6.8 specs (2026-10-22). Confirmed: draw/dispatch last;
root-signature-iff rule; tight packing with arbitrary stride and 4-byte alignment; the min(count, max) formula; state
requirement; bundle restriction; argument type names; `SV_StartInstanceLocation` in SM 6.8. Removed unconfirmed
claims: "fewer argument changes is faster on most hardware" and the `SV_InstanceID` explanation of
`StartInstance` (restated as advice only).
Method: documentation only; no commands were run.
