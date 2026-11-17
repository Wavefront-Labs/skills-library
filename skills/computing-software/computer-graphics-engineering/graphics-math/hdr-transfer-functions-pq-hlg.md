---
id: computing-software.computer-graphics-engineering.graphics-math.hdr-transfer-functions-pq-hlg
name: hdr-transfer-functions-pq-hlg
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, hlg, transfer-functions, pq, hdr10, rec2100]
level: advanced
status: verified
description: "Encode and decode HDR video signals: SMPTE ST 2084 PQ and ARIB/BBC HLG formulas, absolute vs relative luminance, Rec.2020 primaries, metadata (MaxCLL), and display tone mapping."
sources: ["https://www.itu.int/rec/R-REC-BT.2100", "https://www.itu.int/pub/R-REP-BT.2390", "https://pub.smpte.org/latest/st2084/st2084-2014.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDR transfer functions (PQ, HLG)

## PQ (SMPTE ST 2084), absolute luminance up to 10,000 nits
```glsl
const float m1 = 2610.0/16384.0, m2 = 2523.0/4096.0*128.0;
const float c1 = 3424.0/4096.0, c2 = 2413.0/4096.0*32.0, c3 = 2392.0/4096.0*32.0;
vec3 pqEncode(vec3 nits) {                     // linear cd/m2 -> signal 0..1
    vec3 y = pow(nits / 10000.0, vec3(m1));
    return pow((c1 + c2 * y) / (1.0 + c3 * y), vec3(m2));
}
vec3 pqDecode(vec3 e) {
    vec3 p = pow(e, vec3(1.0 / m2));
    return 10000.0 * pow(max(p - c1, 0.0) / (c2 - c3 * p), vec3(1.0 / m1));
}
```
- Code value maps to absolute nits: 100 nits is 0.508 signal, 1000 nits 0.752 (computed).
- Used by HDR10 and others; paired with Rec.2020 primaries (BT.2100).
- Static metadata: MaxCLL, MaxFALL, mastering display (SMPTE ST 2086) guide display tone mapping.

## HLG (ARIB STD-B67 / BT.2100), relative, broadcast-friendly
OETF for scene-linear E in [0,1]:
`E' = sqrt(3E)` for `E <= 1/12`, else `a ln(12E - b) + c` with a = 0.17883277, b = 0.28466892,
c = 0.55991073. Display applies an OOTF with system gamma 1.2 at 1000 nits (adjusted for other peak
luminances: `gamma = 1.2 + 0.42 log10(Lw/1000)`). Backward compatible-ish with SDR displays; no
metadata needed.

## Rendering to HDR displays
- Swapchains: DXGI `DXGI_COLOR_SPACE_RGB_FULL_G2084_NONE_P2020` with R10G10B10A2 (encode PQ yourself),
  or scRGB FP16 (`..._G10_NONE_P709`, linear; 1.0 is conventionally 80 nits, confirm in Microsoft's HDR docs; values above 1 and negative for wide
  gamut). Vulkan: `VK_COLOR_SPACE_HDR10_ST2084_EXT`.
- Convert Rec.709/sRGB primaries to Rec.2020 with a 3x3 matrix in linear light before PQ encoding.
- Paper white: map UI/SDR white to a user-set nits value (e.g. 200), not 10,000.
- Query display peak luminance (DXGI output desc / platform APIs) and tone map to it.

## Gotchas
- Applying PQ twice or interpreting PQ content as sRGB gives washed-out or crushed images.
- Never blend in PQ space; blend in linear light.

## Verify
Encode-decode round trip within 1e-4 relative; display test patterns (PQ ramps at known nits) on a
calibrated HDR monitor.
