---
id: computing-software.computer-graphics-engineering.directx.d3d11-compute-shaders
name: d3d11-compute-shaders
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d11, d3d11-compute, dispatchindirect-d3d11, append-consume-buffers]
level: practitioner
status: docs-checked
description: "Run compute shaders in D3D11: cs_5_0 dispatch, SRV/UAV binding and unbinding, implicit synchronisation, DispatchIndirect, append/consume buffers and FL 10.x limits."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/direct3d-11-advanced-stages-compute-shader", "https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-devices-downlevel-compute-shaders", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-dispatchindirect", "https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-id3d11devicecontext-omsetrendertargetsandunorderedaccessviews", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sm5-object-appendstructuredbuffer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D11 compute shaders

## Dispatch
```cpp
ctx->CSSetShader(cs.Get(), nullptr, 0);
ctx->CSSetConstantBuffers(0, 1, cb.GetAddressOf());
ctx->CSSetShaderResources(0, 1, inputSrv.GetAddressOf());
ctx->CSSetUnorderedAccessViews(0, 1, outputUav.GetAddressOf(), nullptr);
ctx->Dispatch((w + 7) / 8, (h + 7) / 8, 1);
// unbind so the output can be read as SRV elsewhere (runtime hazard tracking)
ID3D11UnorderedAccessView* nullUav = nullptr; ID3D11ShaderResourceView* nullSrv = nullptr;
ctx->CSSetUnorderedAccessViews(0, 1, &nullUav, nullptr);
ctx->CSSetShaderResources(0, 1, &nullSrv);
```
```hlsl
Texture2D<float4> Input : register(t0);
RWTexture2D<float4> Output : register(u0);
[numthreads(8, 8, 1)]
void CSMain(uint3 id : SV_DispatchThreadID) {
    uint w, h; Output.GetDimensions(w, h);
    if (id.x >= w || id.y >= h) return;
    Output[id.xy] = Input[id.xy] * 0.5;
}
```

## No explicit barriers
D3D11 has no resource-barrier API; you only manage bindings. A resource cannot stay bound for
read (SRV) and write (UAV/RTV) at once: `OMSetRenderTargetsAndUnorderedAccessViews` unbinds
conflicting SRVs, compute-shader UAVs and stream-output targets. Unbind the UAV yourself
before binding the same resource as an SRV.

## GPU-driven work
- `DispatchIndirect(argsBuffer, offset)`: the buffer holds the `Dispatch` arguments (three UINTs)
  and is created with `D3D11_RESOURCE_MISC_DRAWINDIRECT_ARGS`. Not supported on downlevel
  (feature level 10.x) hardware.
- Append/consume buffers: `AppendStructuredBuffer<T>` with a UAV flagged
  `D3D11_BUFFER_UAV_FLAG_APPEND`; set initial counter in `CSSetUnorderedAccessViews`;
  `CopyStructureCount(dstBuf, offset, uav)` writes the hidden counter into an args/constant buffer
  (e.g. instance count for `DrawInstancedIndirect`).

## Feature levels
- FL 11.0+: full cs_5_0 (1024 threads/group, 32 KB groupshared, typed UAVs).
- FL 10.x: cs_4_x only if `ComputeShaders_Plus_RawAndStructuredBuffers_Via_Shader_4_x` is set
  (`D3D11_FEATURE_D3D10_X_HARDWARE_OPTIONS`): 768 threads/group, 16 KB groupshared, a single
  UAV bound at a time, raw/structured UAVs only (no typed UAVs), dispatch Z must be 1, no
  `DispatchIndirect`, no pixel-shader UAVs.

## Gotchas
- Unbind the UAV before binding the same resource as an SRV (see above).
- Dispatch group counts must be at most 65535 in each of X, Y and Z.
- Timing compute with queries: `D3D11_QUERY_TIMESTAMP` inside a `TIMESTAMP_DISJOINT` query.

## Verify
- [ ] Output matches a CPU reference; debug layer shows no hazard warnings.

## Checked

2026-10-26. Checked against the Microsoft Learn D3D11 compute shader and downlevel compute shader pages and the Dispatch,
DispatchIndirect, CSSetUnorderedAccessViews and OMSetRenderTargetsAndUnorderedAccessViews reference pages (sdk-api
repository, commits to 2026-10). Confirmed: 1024 threads and 32 KB groupshared on D3D11 hardware, 768 threads, 16 KB,
single UAV and no typed UAVs on downlevel, Dispatch limit 65535 per dimension, DispatchIndirect unsupported on
downlevel, the -1 initial-count rule. Removed the unconfirmed NVAPI/AGS UAV-overlap and automatic-flush claims.
Method: documentation only; no commands were run.
