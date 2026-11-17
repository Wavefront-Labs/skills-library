---
id: computing-software.computer-graphics-engineering.directx.d3d11-shaders-and-input-layouts
name: d3d11-shaders-and-input-layouts
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d11, input-layout, d3d11-shaders, d3dcompile]
level: practitioner
status: docs-checked
description: "Create D3D11 shaders from compiled bytecode, build input layouts that match vertex shader signatures, and bind vertex/index buffers and topology correctly."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-input-assembler-stage-getting-started", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11device-createinputlayout", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/how-to--compile-a-shader", "https://learn.microsoft.com/en-us/windows/win32/direct3dtools/dx-graphics-tools-fxc-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D11 shaders and input layouts

## Compile and create
```cpp
ComPtr<ID3DBlob> vsBlob, err;
HRESULT hr = D3DCompileFromFile(L"basic.hlsl", nullptr, D3D_COMPILE_STANDARD_FILE_INCLUDE,
    "VSMain", "vs_5_0", D3DCOMPILE_ENABLE_STRICTNESS | D3DCOMPILE_DEBUG, 0, &vsBlob, &err);
if (FAILED(hr)) OutputDebugStringA((char*)err->GetBufferPointer());
device->CreateVertexShader(vsBlob->GetBufferPointer(), vsBlob->GetBufferSize(), nullptr, &vs);
```
Prefer offline compilation (`fxc /T vs_5_0 /E VSMain /Fo vs.cso`) and load the compiled files in
release; the D3D11 how-to compiles with FXC (`D3DCompileFromFile`).

## Input layout
```cpp
D3D11_INPUT_ELEMENT_DESC layout[] = {
  { "POSITION", 0, DXGI_FORMAT_R32G32B32_FLOAT, 0, 0,                            D3D11_INPUT_PER_VERTEX_DATA, 0 },
  { "NORMAL",   0, DXGI_FORMAT_R10G10B10A2_UNORM, 0, D3D11_APPEND_ALIGNED_ELEMENT, D3D11_INPUT_PER_VERTEX_DATA, 0 },
  { "TEXCOORD", 0, DXGI_FORMAT_R16G16_FLOAT,     0, D3D11_APPEND_ALIGNED_ELEMENT, D3D11_INPUT_PER_VERTEX_DATA, 0 },
  { "INSTANCE_XFORM", 0, DXGI_FORMAT_R32G32B32A32_FLOAT, 1, 0,  D3D11_INPUT_PER_INSTANCE_DATA, 1 },   // slot 1, per instance
};
device->CreateInputLayout(layout, _countof(layout), vsBlob->GetBufferPointer(), vsBlob->GetBufferSize(), &inputLayout);
```
The layout is validated against the VS input signature at creation (a data-type mismatch produces a
warning because the data may be reinterpreted). A layout can be reused with any shader whose input
signature, semantics included, is identical, so cache one layout per (vertex format, signature).

## Binding
```cpp
ctx->IASetInputLayout(inputLayout.Get());
UINT strides[] = { sizeof(Vertex), sizeof(InstanceData) }, offsets[] = { 0, 0 };
ID3D11Buffer* vbs[] = { vb.Get(), instanceVb.Get() };
ctx->IASetVertexBuffers(0, 2, vbs, strides, offsets);
ctx->IASetIndexBuffer(ib.Get(), DXGI_FORMAT_R16_UINT, 0);
ctx->IASetPrimitiveTopology(D3D11_PRIMITIVE_TOPOLOGY_TRIANGLELIST);
ctx->VSSetShader(vs.Get(), nullptr, 0); ctx->PSSetShader(ps.Get(), nullptr, 0);
ctx->DrawIndexedInstanced(indexCount, instanceCount, 0, 0, 0);
```

## Gotchas
- Matrices per instance need 4 elements (`INSTANCE_XFORM` 0..3), each a float4.
- Vertex pulling (no input layout, SV_VertexID + StructuredBuffer) avoids layout permutations
  and works well on D3D11 too.
- Use `D3DCOMPILE_DEBUG` and `D3DCOMPILE_SKIP_OPTIMIZATION` only in debug builds.

## Verify
- [ ] Debug layer shows no input-assembler warnings.

## Checked

2026-10-26. Checked against Microsoft Learn: CreateInputLayout, D3D11_INPUT_ELEMENT_DESC, the compile-a-shader how-to and the fxc
syntax page (win32 and sdk-api repositories, commits to 2026-10). Confirmed: signature validation and reuse rule,
type mismatch is a warning, D3D11_APPEND_ALIGNED_ELEMENT, fxc /T /E /Fo options. Removed the unconfirmed
E_INVALIDARG-means-semantic-mismatch claim and the no-DXIL statement.
Method: documentation only; no commands were run.
