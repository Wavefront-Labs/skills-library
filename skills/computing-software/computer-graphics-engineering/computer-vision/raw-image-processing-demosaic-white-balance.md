---
id: computing-software.computer-graphics-engineering.computer-vision.raw-image-processing-demosaic-white-balance
name: raw-image-processing-demosaic-white-balance
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, computational-imaging, raw-processing, demosaicing, white-balance, bayer-pattern, black-level, color-correction-matrix, rawpy, libraw, isp]
level: advanced
status: gated
description: "Process camera RAW like an ISP: black/white levels, Bayer pattern and demosaicing, white balance, colour correction matrix to sRGB, and when to keep linear data for vision tasks."
sources: ["https://szeliski.org/Book/", "https://letmaik.github.io/rawpy/api/", "https://www.libraw.org/docs", "https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html#color_convert_bayer", "https://www.adobe.com/content/dam/acom/en/products/photoshop/pdfs/dng_spec_1.6.0.0.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAW processing: demosaic and white balance

**Goal:** turn sensor RAW data into correct linear or display-referred RGB, under your
control — for computational photography, accurate colour, or ML on minimally processed data
(Szeliski 2e §2.3.2, §10.3).

## 1. Pipeline order
1. **Black level** subtraction (per channel, from metadata) and normalise by white level:
   `x = (raw - black) / (white - black)`, clip [0,1].
2. (Optional) lens shading / flat-field correction, defect pixel correction.
3. **White balance**: multiply R, G, B Bayer sites by gains (as-shot from metadata, or
   estimated); do this *before* demosaicing to reduce colour artefacts.
4. **Demosaic** the CFA (RGGB/BGGR/GRBG/GBRG) to full RGB.
5. **Colour correction**: camera RGB → XYZ → linear sRGB/Rec.709 with the camera's colour
   matrix (DNG `ColorMatrix`/`ForwardMatrix` or rawpy's `rgb_xyz_matrix`).
6. Linear output for vision/HDR; or tone curve + sRGB OETF + 8-bit for display.

## 2. With rawpy (LibRaw)
```python
import rawpy
with rawpy.imread("img.dng") as raw:
    linear = raw.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16,
                             use_camera_wb=True, demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD,
                             output_color=rawpy.ColorSpace.sRGB)     # linear 16-bit sRGB primaries
    cfa = raw.raw_image_visible.astype(np.float32)                    # raw Bayer mosaic
    pattern = raw.raw_pattern; black = raw.black_level_per_channel; white = raw.white_level
```
`no_auto_bright=True` and `gamma=(1,1)` keep data linear and unscaled — essential for
radiometric work. The rawpy Params docs give the default gamma as (2.222, 4.5) (BT.709) and the default demosaic as AHD; every keyword in the call above is accepted by `rawpy.Params`, but `postprocess` itself was not run on a RAW/DNG file because none is available here (gated: unconfirmed, source is paywalled or blocked).

## 3. Demosaicing choices
- Bilinear: fast, zipper artefacts and colour fringes at edges.
- OpenCV: `cv2.cvtColor(bayer16, cv2.COLOR_BayerRG2BGR_EA)` (edge-aware, works on 16-bit) or
  `_VNG` (8-bit only: 16-bit input fails with `depth == CV_8U` in OpenCV 5.0.0). Mind OpenCV's
  Bayer naming: it names the pattern by the second row/column. On a synthetic RGGB mosaic
  (R at even row/even column) `COLOR_BayerBG2BGR` gave the correct BGR, `COLOR_BayerRG2BGR`
  swapped red and blue, and OpenCV 5.0.0 also has `COLOR_BayerRGGB2BGR`, which matched the true RGGB
  layout. Test with a known colour chart if channels come out swapped.
- AHD/DCB/AMaZE (LibRaw/RawTherapee): higher quality for photos.
- Learned joint demosaic+denoise for low light.
For ML, consider feeding packed 4-channel RGGB at half resolution instead of demosaicing.

## 4. White balance estimation
As-shot gains from metadata are usually best; otherwise grey-world, white-patch, or a grey
card in the scene (gains = mean(G)/mean(channel) on the card).

## Gotchas
- DNG tag names (`ColorMatrix`, `ForwardMatrix`) are from the Adobe DNG specification, which blocked the fetcher (gated: unconfirmed, source is paywalled or blocked).
- Applying the sRGB tone curve before colour matrices or HDR merge breaks linearity.
- Highlights: clipped channels after WB gains turn pink/magenta — clip after WB or use
  highlight reconstruction.
- Different cameras store black levels per channel and even per row/column (masked areas).

## Verify
- [ ] Colour checker shot: processed linear values match reference within ΔE target.
- [ ] Linearity preserved (exposure sweep proportional).
- [ ] No channel swap (test pattern) and no zipper artefacts at edges.

## Checked
OpenCV 5.0.0, rawpy 0.27.1.
- Run: Bayer conversions on a synthetic RGGB mosaic (names, 8 and 16-bit, `_EA`, `_VNG`); `rawpy.Params(...)` with the skill's keywords; checked `RawPy` attributes `black_level_per_channel`, `white_level`, `raw_pattern`, `raw_image_visible`, `rgb_xyz_matrix`, `camera_whitebalance` and the `DemosaicAlgorithm`/`ColorSpace` members exist.
- Fetched: rawpy `Params` API page (defaults, parameter list).
- Not run: `postprocess` on a real RAW/DNG, the DNG spec (403); gated.
