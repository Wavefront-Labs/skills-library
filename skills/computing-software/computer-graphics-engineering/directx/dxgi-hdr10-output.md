---
id: computing-software.computer-graphics-engineering.directx.dxgi-hdr10-output
name: dxgi-hdr10-output
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, dxgi, dxgi-hdr, setcolorspace1, hdr10, pq-encoding, scrgb, rec2020, st2084, hdr-display, paper-white]
level: advanced
status: gated
description: "Output HDR from D3D12/D3D11: detect HDR displays, choose HDR10 (PQ Rec.2020) or scRGB, set the swap chain colour space and encode with paper-white and max-nits controls."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3darticles/high-dynamic-range", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_6/nf-dxgi1_6-idxgioutput6-getdesc1", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/nf-dxgi1_4-idxgiswapchain3-setcolorspace1", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/nf-dxgi1_4-idxgiswapchain3-checkcolorspacesupport", "https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/ne-dxgi1_4-dxgi_swap_chain_color_space_support_flag", "https://github.com/microsoft/DirectX-Graphics-Samples/tree/master/Samples/Desktop/D3D12HDR"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DXGI HDR10 output

**Goal:** correct HDR on HDR monitors, correct SDR everywhere else, with user controls
for paper white and peak brightness.

## 1. Detect the display
```cpp
ComPtr<IDXGIOutput> out = FindOutputByWindowBounds(hwnd);  // Microsoft advises enumerating outputs by window bounds; GetContainingOutput can return a stale output once IsCurrent() is FALSE
ComPtr<IDXGIOutput6> out6; out.As(&out6);
DXGI_OUTPUT_DESC1 d; out6->GetDesc1(&d);
bool hdrOn = d.ColorSpace == DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020;   // Windows HDR enabled
float maxNits = d.MaxLuminance, minNits = d.MinLuminance;                  // SMPTE ST.2086 panel values; let users override
```

## 2. Two output formats
| swap chain format | colour space | shader output |
|---|---|---|
| `R10G10B10A2_UNORM` | `DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020` (HDR10) | Rec.2020 primaries, PQ-encoded |
| `R16G16B16A16_FLOAT` | `DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709` (scRGB) | linear Rec.709, 1.0 = 80 nits, values >1 and <0 allowed |
```cpp
UINT support; sc3->CheckColorSpaceSupport(cs, &support);
if (support & DXGI_SWAP_CHAIN_COLOR_SPACE_SUPPORT_FLAG_PRESENT) sc3->SetColorSpace1(cs);
```
To change format, call `ResizeBuffers` with the new format (all back-buffer references released), then `SetColorSpace1`.

## 3. Encoding HDR10 in the final pass
```hlsl
float3 PQ(float3 nits) {                  // SMPTE ST 2084 inverse EOTF, input in nits (gated: unconfirmed, source is paywalled or blocked)
    float3 y = nits / 10000.0;
    const float m1 = 0.1593017578125, m2 = 78.84375, c1 = 0.8359375, c2 = 18.8515625, c3 = 18.6875;
    float3 p = pow(y, m1);
    return pow((c1 + c2 * p) / (1 + c3 * p), m2);
}
float3 rec709ToRec2020(float3 c) {   // matrix values (gated: unconfirmed, source is paywalled or blocked)
    return mul(float3x3(0.6274, 0.3293, 0.0433,
                        0.0691, 0.9195, 0.0114,
                        0.0164, 0.0880, 0.8956), c);
}
// scene linear (Rec.709) -> HDR tonemap to [0, maxNits] with paperWhite scaling for UI
out = PQ(rec709ToRec2020(tonemapHDR(scene) * paperWhiteNits));
```
UI: render in SDR and composite at the user's SDR reference white, not at 80 nits or at peak. Windows reports it as
`AdvancedColorInfo.SdrWhiteLevelInNits`; for linear scRGB multiply SDR values by `SdrWhiteLevelInNits / 80`.

## 4. SDR fallback
When the display isn't in HDR mode, keep the SDR pipeline (UNORM + sRGB) — don't output
HDR10 and let Windows tonemap it.

## Gotchas
- Offer a user override for peak brightness in case the reported luminance does not suit the display.
- Tone mapper must target the display peak; an SDR curve scaled up looks flat.
- If the display is SDR, DWM clips scRGB values outside [0, 1]; HDR content on an SDR display is down-converted by numeric clipping.
- SDR displays with Advanced Color are also reported as `DXGI_COLOR_SPACE_RGB_FULL_G22_NONE_P709`; DXGI cannot tell them apart.

## Verify
- [ ] On an HDR display: highlights exceed SDR white, UI brightness matches user setting.
- [ ] Toggling Windows HDR while running switches paths without restart (query `IDXGIFactory1::IsCurrent` each frame and re-read `DXGI_OUTPUT_DESC1` when it is FALSE; handle `WM_SIZE` for moves between displays).
- [ ] SDR display output identical to the pre-HDR build.

## Checked

Checked 2026-10-26 against the Microsoft Learn Win32 documentation sources (MicrosoftDocs/win32 and MicrosoftDocs/sdk-api, repositories current to 2026-10) and the PresentMon console README. Confirmed: DXGI_OUTPUT_DESC1 fields (ColorSpace, Min/MaxLuminance), G2084_NONE_P2020 for an HDR display and G22_NONE_P709 for SDR, 1.0 = 80 nits nominal reference white, SdrWhiteLevelInNits scaling, IsCurrent and WM_SIZE guidance and the warning about GetContainingOutput, SetColorSpace1/CheckColorSpaceSupport and the PRESENT support flag, R10G10B10A2/R16G16B16A16 HDR formats. The PQ constants (SMPTE ST 2084) and the Rec.709 to Rec.2020 matrix (ITU-R BT.2087) are marked as gated in the code: the standards are paywalled or blocked, so confirm the exact values there. Removed: the 200 nit default, 'monitors often report wrong' and the SDR-slider claims.
Method: documentation only; no commands were run.
