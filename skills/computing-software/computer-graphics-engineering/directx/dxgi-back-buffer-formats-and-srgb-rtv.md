---
id: computing-software.computer-graphics-engineering.directx.dxgi-back-buffer-formats-and-srgb-rtv
name: dxgi-back-buffer-formats-and-srgb-rtv
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, back-buffer-format, srgb-rtv, flip-model-srgb]
level: practitioner
status: docs-checked
description: "Pick DXGI back buffer formats for flip-model swap chains (UNORM, R10G10B10A2, FP16) and get sRGB output via an _SRGB render target view, not an sRGB swap chain."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/dxgi-flip-model", "https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/for-best-performance--use-dxgi-flip-model", "https://learn.microsoft.com/en-us/windows/win32/direct3darticles/high-dynamic-range", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/swap-chains"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Back buffer formats and sRGB RTVs

## Allowed flip-model formats
The flip-model page lists `R16G16B16A16_FLOAT`, `B8G8R8A8_UNORM` and `R8G8B8A8_UNORM`; the flip-model performance page
also names `R10G10B10A2_UNORM` for HDR content. `*_UNORM_SRGB` is not in these lists, so create the swap chain
with the UNORM format and apply sRGB through the view.

## sRGB encoding with an sRGB view
Create the swap chain as UNORM and the render target view as SRGB:
```cpp
DXGI_SWAP_CHAIN_DESC1 sd = {};
sd.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
sd.SwapEffect = DXGI_SWAP_EFFECT_FLIP_DISCARD; sd.BufferCount = 3; sd.SampleDesc.Count = 1;
// ...
D3D12_RENDER_TARGET_VIEW_DESC rtv = {};
rtv.Format = DXGI_FORMAT_R8G8B8A8_UNORM_SRGB;            // hardware linear->sRGB on write
rtv.ViewDimension = D3D12_RTV_DIMENSION_TEXTURE2D;
device->CreateRenderTargetView(backBuffer.Get(), &rtv, rtvHandle);
```
Shader output is linear; blending happens in linear space. If you tone-map and encode in the
shader yourself, use a UNORM RTV instead (never both, or the image is double-gamma bright).

## Which format
| Format | When |
|---|---|
| `R8G8B8A8_UNORM` / `B8G8R8A8_UNORM` | SDR default (`B8G8R8A8_UNORM` is the sample format in the DXGI docs) |
| `R10G10B10A2_UNORM` | SDR with less banding, or HDR10 with `DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020` |
| `R16G16B16A16_FLOAT` | scRGB HDR (`DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709`), linear values, 1.0 = 80 nits (Windows nominal reference white) |

MSAA swap chains are not supported in flip model (`Count` 1, `Quality` 0): render to an MSAA target and resolve
into the back buffer before `Present`.

## Resize
`ResizeBuffers(0, w, h, DXGI_FORMAT_UNKNOWN, flags)` keeps the format; all back buffer references
and RTVs must be released first, and `ALLOW_TEARING` must be passed again if it was used at creation.

## Gotchas
- D3D12: the back buffer must be in `D3D12_RESOURCE_STATE_PRESENT` when `Present` is called, so transition to `RENDER_TARGET` for drawing and back.
- Readback/screenshots of an sRGB-view-rendered back buffer: bytes are already sRGB encoded; save directly.
- UI drawn after tone mapping into the same target must also be in the same encoding convention.

## Verify
- [ ] Mid-gray (0.5 linear) renders as ~188/255 in a screenshot with the sRGB RTV; validation clean on resize.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: flip-model format lists, no MSAA, ResizeBuffers/ALLOW_TEARING flag rule, 80 nits nominal reference white for scRGB, PRESENT-state requirement in D3D12. Mid-gray 0.5 linear encodes to about 188/255 (computed from the sRGB transfer function). Removed: the specific error code for an sRGB swap-chain format and the BGRA composition-path claim, which no page states.
Method: documentation only; no commands were run.
