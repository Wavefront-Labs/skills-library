---
id: computing-software.computer-graphics-engineering.rendering-techniques.ibl-baking-cmgen-iblbaker
name: ibl-baking-cmgen-iblbaker
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, ibl-baking, cmgen, ibl, prefiltered-environment, dfg-lut, irradiance-map]
level: practitioner
status: docs-checked
description: "Bake image-based lighting assets offline: equirect HDR to cubemap, prefiltered specular mips (GGX importance sampled), irradiance/SH, and DFG LUT with Filament cmgen or IBLBaker."
sources: ["https://github.com/google/filament/blob/main/tools/cmgen/README.md", "https://github.com/derkreature/IBLBaker", "https://registry.khronos.org/OpenGL/index_gl.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baking IBL with cmgen / IBLBaker

## 1. What to produce
From one HDR environment (equirect `.hdr`/`.exr`):
1. **Prefiltered specular cubemap**: mip level i = GGX-convolved for roughness `i / (mips - 1)`
   (perceptual roughness mapping must match the runtime).
2. **Diffuse irradiance**: a small cubemap or spherical-harmonics coefficients (3 bands = 9 coefficients per channel).
3. **DFG / BRDF LUT**: 2D texture (NoV, roughness) -> (scale, bias) for the split-sum; environment
   independent, bake once.

## 2. Filament cmgen
```bash
cmgen --format=ktx --size=256 --deploy=out/ studio.hdr      # everything needed for deployment into out/
cmgen --extract=faces/ --extract-blur=0.1 studio.hdr         # write cubemap faces, blurred by a roughness value
cmgen --ibl-samples=1024 --ibl-ld=ld/ studio.hdr             # roughness pre-filter into ld/
cmgen --sh-shader studio.hdr                                 # irradiance SH as shader code
```
Per the cmgen README: input is a latlong or cubemap-cross HDR/PNG/PSD/EXR map; `--format=ktx` writes KTX1 files
(not KTX2) with RGB_10_11_11_REV data; `--size` is the base cubemap size (default 256, also applies to the DFG LUT);
`--ibl-samples` defaults to 1024; `--clamp` clamps the environment before processing. Check `cmgen --help` for the
options of the version you build.

## 3. IBLBaker / custom
IBLBaker (MIT-licensed, Visual Studio/CMake build) uses importance sampling to bake diffuse irradiance and pre-convolved specular cubemaps over roughness mips, shows them with the separable (split-sum) method from Epic's SIGGRAPH 2013 talk, and saves the maps and the BRDF LUT to disk. Many
engines do it in compute at load time: equirect -> cube, then importance-sample GGX per mip with
**filtered importance sampling** (sample lower mips of the source based on PDF) to remove
fireflies at low sample counts.

## 4. Quality settings
- Sample count and base size are tool options (cmgen: `--ibl-samples`, `--size`); raise samples for rough mips or use filtered importance sampling.
- Clamp extreme HDR values (the sun) or remove the sun from the HDRI and add it as a directional
  light, otherwise prefiltered mips get blotchy (cmgen offers `--clamp`).
- Choose the storage format deliberately; cmgen can write rgbm, rgb32f, exr, hdr, png, dds and ktx.

## 5. Runtime consistency
- Same roughness-to-mip mapping in baker and shader (`lod = roughness * (mipCount - 1)` vs other
  curves).
- Same cubemap orientation conventions (+Y up, handedness); test with a labelled cubemap.
- Intensity in physical units consistent with lights (scale factor documented).

## Gotchas
- Seams on prefiltered cube edges in low mips: enable `GL_TEXTURE_CUBE_MAP_SEAMLESS` in OpenGL and filter across faces when baking.
- Using the DFG LUT made for a different roughness parameterisation darkens rough materials.

## Verify
- [ ] Chrome sphere matches the environment; rough sphere blurs smoothly without fireflies.
- [ ] Diffuse SH irradiance matches the convolved cubemap within a few percent.

## Checked

2026-10-26: Filament tools/cmgen/README.md (main, read 2026-10-26), IBLBaker README (MIT licence, importance sampling, saves maps and BRDF LUT), OpenGL-Registry gl.xml (GL_TEXTURE_CUBE_MAP_SEAMLESS exists). Wrong or unconfirmed claims removed: the options --ibl-dfg, --ibl-dfg-multiscatter, --sh=3 and --sh-output are not in the cmgen README; the extract example mixed --deploy with --extract; the *_ibl.ktx file names, the D3D11 label, the source and base cubemap sizes and the 32-64 filtered-sample figure had no documentation. cmgen defaults confirmed: size 256, 1024 IBL samples, KTX1 RGB_10_11_11_REV.

Method: documentation only; no commands were run.
