---
id: computing-software.computer-graphics-engineering.rendering-techniques.hdr-ui-compositing
name: hdr-ui-compositing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, hdr-tonemapping, hdr-ui-compositing, hdr10, scrgb, paper-white, pq-st2084, display-output]
level: advanced
status: docs-checked
description: "Composite SDR UI into HDR output on Windows: swap-chain formats, SDR reference white scaling, blending in linear light, and when the OS composites for you."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3darticles/high-dynamic-range"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UI compositing in HDR (Windows DXGI)

## 1. Output modes
- **scRGB (recommended for general-purpose apps)**: `DXGI_FORMAT_R16G16B16A16_FLOAT`. A float
  swap chain is treated as `DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709` (linear, BT.709 primaries),
  the same format and space the DWM composes in. `(1, 1, 1)` is D65 white at 80 nits and
  `(12.5, 12.5, 12.5)` is 1000 nits; values outside [0, 1] represent brighter or wider-gamut colour.
  It costs 64 bits per pixel. Use a flip-model swap effect
  (`DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL` or `FLIP_DISCARD`).
- **HDR10 (optimisation)**: `DXGI_FORMAT_R10G10B10A2_UNORM` plus an explicit
  `IDXGISwapChain3::SetColorSpace1(DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020)`. It is only
  available when the target is an HDR display, the API is Direct3D 11 or 12, and the swap chain does
  not need alpha blending; otherwise use scRGB. It is 32 bits per pixel.
- On an SDR display the DWM clips an HDR swap chain to [0, 1]. For SDR displays, `1.0` means
  the maximum white the display can reproduce.

## 2. SDR reference white ("paper white")
On HDR displays, `1.0` in scRGB is nominal reference white at 80 nits, but the user sets the SDR
reference white level in Windows (typically around 200 nits on desktop HDR monitors). Diffuse
white and SDR UI must map to that level:
- Read it with `DISPLAYCONFIG_SDR_WHITE_LEVEL` and `QueryDisplayConfig` (desktop) or
  `AdvancedColorInfo.SdrWhiteLevelInNits` (UWP).
- In linear gamma (scRGB), multiply the SDR colour by `SdrWhiteLevelInNits / 80`
  (Direct2D exposes `D2D1_SCENE_REFERRED_SDR_WHITE_LEVEL` = 80).
- In a nonlinear space such as HDR10 the adjustment is harder: convert to linear in the pixel shader,
  apply it, then re-encode. Windows notes scRGB (1,1,1) and HDR10 (497,497,497) both encode 80 nits.
- Your HDR app must either let the user choose the level or read the system value.

## 3. Who composites
- If SDR and HDR content are on separate surfaces and the OS composes them (for example HDR in its
  own XAML `SwapChainPanel`), Windows boosts the SDR content to the desired white level.
- If the app composites SDR and HDR into one surface, the app must apply the reference-white
  adjustment itself, or the SDR content appears too dim.
- Blend in a linear space: Microsoft notes BT.2100 ST.2084 (PQ) is not well suited to rendering
  and blending operations, while FP16 linear gives excellent blending precision. Blend UI over the
  tone-mapped scene in linear light, then encode for the output format.

## 4. Display capabilities and tone mapping
- Detect the display on each change: `IDXGIOutput6::GetDesc1` (`DXGI_OUTPUT_DESC1`) gives the
  colour space (`G2084_NONE_P2020` for HDR, `G22_NONE_P709` for SDR) and luminance range; poll
  `IDXGIFactory1::IsCurrent` each frame and pick the output with the greatest overlap with the
  window (do not use `GetContainingOutput`).
- Tone-map HDR content to the display's maximum luminance; Windows says there is no single standard
  algorithm (ACES Filmic, Reinhard and ITU-R BT.2390-3 EETF are common).
- Capture APIs (`Windows.Graphics.Capture`, `IDXGIOutput5::DuplicateOutput1`) return HDR
  pixels; an SDR screenshot needs HDR-to-SDR tone mapping afterwards.

## Verify
- [ ] UI brightness matches the Windows SDR content brightness setting.
- [ ] On an SDR display with an scRGB swap chain, values above 1.0 are clipped as documented; check the SDR fallback looks right.

## Checked
2026-11-08. Read in full: Microsoft Learn "Use DirectX with Advanced Color on high/standard dynamic
range displays". Confirmed: swap-chain formats and colour spaces, HDR10 conditions, 80 nit scRGB
mapping and 1000 nit example, reference white APIs and scaling, who composites, PQ-versus-linear
blending note, output detection, tone mapping and capture notes. Removed claims that page does not
make: Vulkan colour-space enums, 100-300 nit range, per-step UI buffer recipe, OLED and readability
advice, translucent-UI gamma blending. Removed two sources: the AMD FreeSync page covers only
FreeSync HDR setup, and the GDC Vault URL is a Destiny 2 session page behind a login wall, not a Call
of Duty talk.
Method: documentation only; no commands were run.
