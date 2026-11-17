---
id: computing-software.computer-graphics-engineering.opengl.vulkan-hdr-swapchain-colour-spaces
name: vulkan-hdr-swapchain-colour-spaces
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-swapchain, hdr-swapchain, vk-color-space, hdr10, scrgb, vk-ext-hdr-metadata]
level: advanced
status: docs-checked
description: "Output HDR from Vulkan: pick HDR10 ST2084 or scRGB swapchain formats, set HDR metadata, encode PQ correctly and fall back to SDR."
sources: ["https://docs.vulkan.org/spec/latest/chapters/VK_KHR_surface/wsi.html", "https://docs.vulkan.org/spec/latest/appendices/VK_EXT_hdr_metadata.html", "https://docs.vulkan.org/spec/latest/appendices/VK_EXT_swapchain_colorspace.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDR swapchain colour spaces in Vulkan

**Goal:** present real HDR to an HDR display, with a correct SDR fallback.

## 1. Enable and enumerate
Instance extension `VK_EXT_swapchain_colorspace` (exposes the extended colour spaces), device
extension `VK_EXT_hdr_metadata`. Then `vkGetPhysicalDeviceSurfaceFormatsKHR` and look for:
| Format | Colour space | Encode in shader |
|---|---|---|
| `A2B10G10R10_UNORM_PACK32` | `HDR10_ST2084_EXT` | Rec.2020 primaries (0.708,0.292 / 0.170,0.797 / 0.131,0.046, D65 white), ST 2084 PQ transfer function |
| `R16G16B16A16_SFLOAT` | `EXTENDED_SRGB_LINEAR_EXT` (extended sRGB, linear) | Rec.709/sRGB primaries, linear transfer, values above 1 and below 0 allowed |
| `B8G8R8A8_SRGB` | `SRGB_NONLINEAR_KHR` | SDR fallback |
The spec does not say which formats pair with which colour space: only offer HDR when the surface reports such a pair, and
re-enumerate on swapchain recreation (the supported list is per surface and can change).

## 2. Metadata
```cpp
VkHdrMetadataEXT md{VK_STRUCTURE_TYPE_HDR_METADATA_EXT};
md.displayPrimaryRed = {0.708f, 0.292f}; md.displayPrimaryGreen = {0.170f, 0.797f};
md.displayPrimaryBlue = {0.131f, 0.046f}; md.whitePoint = {0.3127f, 0.3290f};   // Rec.2020 primaries, D65
md.maxLuminance = masterPeakNits; md.minLuminance = masterMinNits;               // display used to optimise the content, in nits
md.maxContentLightLevel = contentMaxNits; md.maxFrameAverageLightLevel = contentAvgNits;   // 0 = unknown
vkSetHdrMetadataEXT(device, 1, &swapchain, &md);
```
The structure describes the display the content was optimised for (SMPTE 2086 style) plus content light levels (CTA 861.3), all in nits; unknown values may be 0.
Query the actual display's peak through the platform API and expose a peak-brightness setting; tone map to that peak.

## 3. Output transform
Scene-linear (Rec.709/sRGB primaries) -> tone map with HDR peak -> convert primaries to
Rec.2020 (3x3 matrix) -> PQ-encode absolute luminance with the SMPTE ST 2084 inverse EOTF (confirm the constants and the
normalisation in ST 2084 itself, which is paywalled).
For extended sRGB linear skip PQ and the primaries change; the mapping from linear values to display nits is set by the platform compositor, so confirm its paper-white reference in the platform documentation.

## Gotchas
- UI composited in HDR needs its own paper-white scale or it looks dim/grey.
- `A2B10G10R10` with `SRGB_NONLINEAR` is plain 10-bit SDR, not HDR.
- Screenshots/video capture of PQ output look washed out in SDR tools; that is expected.

## Verify
- [ ] HDR output enabled in the OS: a bright test patch is visibly brighter than UI white.
- [ ] HDR output disabled: swapchain recreation picks the SDR format and the image looks unchanged in SDR.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/VK_KHR_surface/wsi.adoc colour-space table and VkHdrMetadataEXT, appendices/VK_EXT_swapchain_colorspace.adoc, VK_EXT_hdr_metadata.adoc, xml/vk.xml).
Confirmed: VK_EXT_swapchain_colorspace is an instance extension and VK_EXT_hdr_metadata a device extension depending on VK_KHR_swapchain; Rec.2020 primaries and white point for HDR10_ST2084; extended sRGB linear definition; VkHdrMetadataEXT members, nits units and 0-for-unknown rule; format and colour-space pairing is not specified by the spec.
Removed: scRGB 80-nit scale, Windows-specific claims and the example metadata values. The PQ curve constants are left to SMPTE ST 2084 (paywalled; confirm the exact values there).
Method: documentation only; no commands were run.
