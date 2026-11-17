---
id: computing-software.computer-graphics-engineering.rendering-techniques.spectral-rendering
name: spectral-rendering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, spectral-rendering, hero-wavelength, spectral-uplifting, dispersion, colour-science, path-tracing]
level: advanced
status: docs-checked
description: "Render spectrally instead of RGB: hero-wavelength sampling (Wilkie et al.), pbrt spectrum types, and how Dirac and dispersive events affect the extra wavelengths."
sources: ["https://pbr-book.org/4ed/Radiometry,_Spectra,_and_Color/Representing_Spectral_Distributions", "https://jo.dreggn.org/home/2014_herowavelength.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spectral rendering

## 1. Hero wavelength sampling (Wilkie, Nawaz, Droske, Weidlich, Hanika 2014)
Single-wavelength path sampling is unbiased and handles wavelength-dependent phenomena, but its
colour noise is "highly objectionable" and hard to remove in post-processing. Hero wavelength
sampling keeps the single-wavelength sampler as the base:
- The first, randomly sampled wavelength is the **hero wavelength** and drives all path
  propagation (directional sampling) decisions, so no extra random numbers are needed.
- The remaining wavelengths are not random: they sit at equidistant locations around the hero
  wavelength (using a rotation of the hero within the visible range) so the visible spectrum is
  covered evenly (stratified).
- Each of the C wavelengths could have been the hero, so each counts as a different sampling
  technique, and the estimator combines them with multiple importance sampling over those rotated
  techniques (the paper's joint MIS also extends to other techniques such as bidirectional path
  tracing and next-event estimation).
- Reported cost: 3 to 10 percent extra wall-clock time against single wavelength at similar
  sample counts, with much less colour noise at low sample counts.
- Replacing scalars with SSE-style 4-vectors is not enough: all sampling decisions must use the
  hero wavelength's pdfs.

## 2. Dirac (specular) events
Paths that are possible only for the hero wavelength (for example wavelength-dependent refraction
through a Dirac interface) use only the first spectral channel and the other contributions are
blanked out, so the render falls back to single-wavelength behaviour there. Dirac contributions
aligned for other wavelengths are still distributed over all channels.

## 3. pbrt-v4 representation
- Wavelengths are in nanometres; the visible range constants are `Lambda_min = 360` and
  `Lambda_max = 830`.
- `Spectrum` is a tagged pointer over `ConstantSpectrum`, `DenselySampledSpectrum`,
  `PiecewiseLinearSpectrum`, `RGBAlbedoSpectrum`, `RGBUnboundedSpectrum`,
  `RGBIlluminantSpectrum` and `BlackbodySpectrum`.
- `NSpectrumSamples = 4` wavelengths are carried per path in `SampledSpectrum` and
  `SampledWavelengths`.
- RGB inputs are turned into spectra by the three RGB spectrum types listed above (the page only
  names them; their construction is described in the book's Color chapter, which was not read).

## Gotchas
- Using a plain box spectrum per RGB channel is not what pbrt does; it has dedicated RGB-to-spectrum
  classes.
- Do not reuse single-wavelength sampling code that makes decisions on a non-hero wavelength.

## Verify
- [ ] A neutral scene renders with no colour cast after conversion to RGB.
- [ ] Low-spp colour noise is lower than a single-wavelength baseline on coloured area lights.

## Checked
2026-11-09. Read: Wilkie et al. 2014 "Hero Wavelength Spectral Sampling" (sections 3 and the
joint MIS discussion, the Dirac paragraph, figure captions and the 3 to 10 percent timing) and
the pbr-book "Representing Spectral Distributions" section (wavelength range constants, the
Spectrum type list, NSpectrumSamples). Removed: the Jakob and Hanika 2019 sigmoid-polynomial
details (the source page was only an abstract landing page), XYZ accumulation and output
matrices, Sellmeier and Cauchy advice, the CIE importance-sampling claim, `SampleVisible` and
`TerminateSecondary` details, and the renderer list (Manuka and Mitsuba).
Method: docs-checked 2026-11-09 against the Wilkie et al. hero wavelength paper and the pbr-book Representing Spectral Distributions section.
