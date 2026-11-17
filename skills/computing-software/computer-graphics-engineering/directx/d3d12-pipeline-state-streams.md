---
id: computing-software.computer-graphics-engineering.directx.d3d12-pipeline-state-streams
name: d3d12-pipeline-state-streams
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-advanced, pipeline-state-stream, createpipelinestate, pso-subobjects]
level: advanced
status: docs-checked
description: "Create D3D12 PSOs with pipeline state streams (CreatePipelineState): subobject layout, d3dx12 stream helpers, mesh shader PSOs, view instancing and PSO caching."
sources: ["https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device2-createpipelinestate", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ne-d3d12-d3d12_pipeline_state_subobject_type", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device1-createpipelinelibrary", "https://microsoft.github.io/DirectX-Specs/d3d/MeshShader.html", "https://microsoft.github.io/DirectX-Specs/d3d/ViewInstancing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline state streams

`D3D12_GRAPHICS_PIPELINE_STATE_DESC` is fixed and cannot express newer state (mesh and amplification shaders,
view instancing, depth bounds). `ID3D12Device2::CreatePipelineState` takes a **stream** of typed subobjects
(`D3D12_PIPELINE_STATE_STREAM_DESC`) instead.

## Mesh shader PSO with d3dx12 helpers
```cpp
struct MeshPsoStream {
    CD3DX12_PIPELINE_STATE_STREAM_ROOT_SIGNATURE        RootSig;
    CD3DX12_PIPELINE_STATE_STREAM_AS                    AS;
    CD3DX12_PIPELINE_STATE_STREAM_MS                    MS;
    CD3DX12_PIPELINE_STATE_STREAM_PS                    PS;
    CD3DX12_PIPELINE_STATE_STREAM_RENDER_TARGET_FORMATS RTFormats;
    CD3DX12_PIPELINE_STATE_STREAM_DEPTH_STENCIL_FORMAT  DSFormat;
    CD3DX12_PIPELINE_STATE_STREAM_RASTERIZER            Raster;
    CD3DX12_PIPELINE_STATE_STREAM_DEPTH_STENCIL1        DepthStencil;
    CD3DX12_PIPELINE_STATE_STREAM_BLEND_DESC            Blend;
} s;
s.RootSig = rootSig.Get();
s.AS = CD3DX12_SHADER_BYTECODE(asBlob.data(), asBlob.size());
s.MS = CD3DX12_SHADER_BYTECODE(msBlob.data(), msBlob.size());
s.PS = CD3DX12_SHADER_BYTECODE(psBlob.data(), psBlob.size());
D3D12_RT_FORMAT_ARRAY rt = {}; rt.NumRenderTargets = 1; rt.RTFormats[0] = DXGI_FORMAT_R11G11B10_FLOAT;
s.RTFormats = rt; s.DSFormat = DXGI_FORMAT_D32_FLOAT;
s.Raster = CD3DX12_RASTERIZER_DESC(D3D12_DEFAULT);
s.DepthStencil = CD3DX12_DEPTH_STENCIL_DESC1(D3D12_DEFAULT);
s.Blend = CD3DX12_BLEND_DESC(D3D12_DEFAULT);
D3D12_PIPELINE_STATE_STREAM_DESC sd = { sizeof(s), &s };
device2->CreatePipelineState(&sd, IID_PPV_ARGS(&pso));
```
Each helper is a subobject-type tag plus payload; the d3dx12 parser reports duplicate subobjects as an error.

## Other subobjects worth knowing
- `VIEW_INSTANCING` (view instancing, at most `D3D12_MAX_VIEW_INSTANCE_COUNT` = 4 views).
- `DEPTH_STENCIL1` adds `DepthBoundsTestEnable`; `DEPTH_STENCIL2` uses per-face stencil op descriptions
  (`D3D12_DEPTH_STENCILOP_DESC1`) with their own masks.
- `CACHED_PSO`, `FLAGS`, `NODE_MASK`, `SAMPLE_DESC`, `SAMPLE_MASK`.
- `RASTERIZER1` (float `DepthBias`) and `RASTERIZER2` (adds `LineRasterizationMode`) exist in `d3d12.h`.

## PSO caching
- `ID3D12PipelineLibrary` stores PSOs by name in a serialisable blob (`StorePipeline`, `LoadGraphicsPipeline`,
  `LoadComputePipeline`; `ID3D12PipelineLibrary1::LoadPipeline` takes a stream description). Creating a library
  from a stored blob (`ID3D12Device1::CreatePipelineLibrary`) returns `D3D12_ERROR_DRIVER_VERSION_MISMATCH` if the
  data came from an older driver or runtime, `D3D12_ERROR_ADAPTER_NOT_FOUND` if it came from different hardware,
  and `E_INVALIDARG` for a corrupt or unrecognised blob. Rebuild the library on any of these.

## Gotchas
- `E_INVALIDARG` without detail: enable the debug layer for the explanation.
- Mesh shaders do not use index buffers or input layouts (mesh shader spec); check `MeshShaderTier` first.

## Verify
- [ ] PSO creation succeeds with the debug layer clean; a second launch loads from the library.

## Checked
Date: 2026-10-26. Documentation: `ID3D12Device2::CreatePipelineState`, `D3D12_PIPELINE_STATE_SUBOBJECT_TYPE`,
`ID3D12Device1::CreatePipelineLibrary`, `ID3D12PipelineLibrary1::LoadPipeline` (MicrosoftDocs/sdk-api, last commit
2026-10-08), DirectX-Specs MeshShader and ViewInstancing specs (2026-10-22), `d3d12.h` from DirectX-Headers.
Confirmed: stream structure, subobject names, view-instancing limit, DEPTH_STENCIL1/2 and RASTERIZER1/2 existence,
library error codes and where they are returned. Removed unconfirmed claims: default values for omitted subobjects
(sample count 1, mask 0xffffffff), driver disk-cache remarks, "mesh PSOs must not include VS" (restated from the
spec as no input layouts), and the managing-pipeline-state link (not used).
Method: documentation only; no commands were run.
