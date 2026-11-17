---
id: computing-software.computer-graphics-engineering.graphics-math.icc-profiles-and-display-calibration
name: icc-profiles-and-display-calibration
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, icc-profiles, color-management, display-calibration, littlecms, rendering-intent]
level: practitioner
status: draft
description: "Manage colour across devices with ICC profiles: matrix/TRC vs LUT profiles, rendering intents, LittleCMS conversion, and display calibration with DisplayCAL/ArgyllCMS."
sources: ["https://www.color.org/specification/ICC.1-2022-05.pdf", "https://www.littlecms.com/", "https://www.argyllcms.com/doc/Scenarios.html", "https://displaycal.net/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ICC profiles and display calibration

## What a profile is
A mapping between device values and the profile connection space (PCS: CIE XYZ or Lab, D50).
- **Matrix/TRC** profiles: 3 tone curves + 3x3 matrix (displays, sRGB/Display P3 working spaces).
- **LUT** profiles (A2B/B2A tables): printers, complex devices, gamut mapping.

## Rendering intents
| Intent | Behaviour | Use |
|---|---|---|
| Perceptual | Compress whole gamut | Photos into small gamuts (printing) |
| Relative colorimetric | Clip out-of-gamut, map white to white | Default for most conversions, proofing |
| Saturation | Keep vividness | Charts/graphics |
| Absolute colorimetric | Keep paper white too | Proofing paper simulation |
Black point compensation helps relative colorimetric into devices with lighter blacks.

## Converting in code (LittleCMS)
```python
from PIL import Image, ImageCms
img = Image.open("in.jpg")
src = ImageCms.ImageCmsProfile(io.BytesIO(img.info["icc_profile"])) if "icc_profile" in img.info else ImageCms.createProfile("sRGB")
dst = ImageCms.createProfile("sRGB")
out = ImageCms.profileToProfile(img, src, dst, renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC, outputMode="RGB")
out.save("out.jpg", icc_profile=ImageCms.ImageCmsProfile(dst).tobytes())
```
C: `cmsCreateTransform(hIn, TYPE_RGB_8, hOut, TYPE_RGB_8, INTENT_RELATIVE_COLORIMETRIC, 0)` then
`cmsDoTransform`.
- Images without a profile are assumed sRGB on the web. Stripping profiles from Display P3 phone photos
  desaturates them in colour-managed viewers and oversaturates in others.
- OpenCV `imread` ignores embedded ICC profiles: convert with PIL/LittleCMS first if colour accuracy
  matters.

## Display calibration and profiling
1. **Calibrate**: set white point (D65), luminance (e.g. 120 nits), tone response (gamma 2.2/sRGB)
   with monitor controls + video card LUTs (vcgt tag).
2. **Profile**: measure patches with a colorimeter (DisplayCAL/ArgyllCMS `dispcal`, `dispread`,
   `colprof`), produce an ICC profile, install it in the OS.
Games and many apps are not colour managed: wide-gamut monitors oversaturate sRGB content unless set
to an sRGB mode or the app converts.

## Verify
Verification report in DisplayCAL (mean delta E 2000 below about 1 to 2); for code, convert known patches
(e.g. sRGB red to Display P3) and compare with reference values.
