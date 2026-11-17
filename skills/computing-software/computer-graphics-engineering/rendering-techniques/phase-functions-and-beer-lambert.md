---
id: computing-software.computer-graphics-engineering.rendering-techniques.phase-functions-and-beer-lambert
name: phase-functions-and-beer-lambert
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetrics, phase-function, beer-lambert, henyey-greenstein, participating-media, extinction, scattering]
level: advanced
status: docs-checked
description: "Model participating media: absorption, scattering and extinction coefficients, Beer-Lambert transmittance, and Henyey-Greenstein and Cornette-Shanks phase functions."
sources: ["https://pbr-book.org/4ed/Volume_Scattering", "https://sebh.github.io/publications/egsr2020.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phase functions and Beer-Lambert extinction

## 1. Coefficients (per unit distance, can vary with wavelength and position)
- `sigma_a` absorption coefficient: probability density of absorption per unit distance.
- `sigma_s` scattering coefficient; `sigma_t = sigma_a + sigma_s` is the attenuation (extinction)
  coefficient.
- Single-scattering albedo `rho = sigma_s / sigma_t`: the probability of scattering rather than
  absorption at a scattering event; between 0 and 1 under radiometric assumptions. A cloud with no
  absorption has albedo 1 and scatters many times, looking very different from an absorbing medium.
- Absorption alone gives `L(p) -> L * exp(-integral of sigma_a dt)` along the ray (pbrt-v4 eq.
  for the absorption-only case). With out-scattering as well, the loss uses `sigma_t`: the
  transmittance over distance d is `T = exp(-integral of sigma_t dt)`, which for a homogeneous
  medium reduces to `exp(-sigma_t * d)` (Beer-Lambert). The same form is Equation 2 in Hillaire's
  EGSR 2020 atmosphere paper (`T(xa, xb) = exp(-integral of sigma_t(x) dx)`).
- Scattering adds radiance back into a ray (in-scattering, weighted by the albedo and the phase
  function); there is no cosine term because the phase function acts on radiance.

## 2. Phase functions
A phase function is the volumetric analogue of a BSDF; it is a probability distribution over
scattered directions and integrates to 1 over the sphere.
- Isotropic: `1 / (4 PI)`.
- **Henyey-Greenstein** with asymmetry `g`, designed to be easy to fit to measured data. pbrt-v4
  writes it with its own direction convention (both directions point away from the point), which
  flips the sign of the `2 g cos` term relative to the scattering literature:
```cpp
// pbrt-v4 convention
float HenyeyGreenstein(float cosTheta, float g) {
    float denom = 1 + g * g + 2 * g * cosTheta;
    return (1 / (4 * PI)) * (1 - g * g) / (denom * sqrt(max(0.f, denom)));
}
```
  If you use the literature convention (cosine between the travel direction and the scatter
  direction), the denominator is `1 + g^2 - 2 g cosTheta`. Check which one your code uses.
  The asymmetry parameter g is the mean cosine of the scattering direction; one value alone does
  not uniquely describe a distribution, and pbrt notes that more complex phase functions can be
  modelled as a weighted sum of Henyey-Greenstein functions with different g.
- **Cornette-Shanks** (used by Hillaire 2020 for aerosols/Mie, default g = 0.8):
  `3/(8 PI) * (1 - g^2)(1 + cos^2) / ((2 + g^2)(1 + g^2 - 2 g cos)^(3/2))`.
  The paper says the simpler Henyey-Greenstein function is also appropriate.

## 3. Multiple scattering (atmospheres)
Hillaire's paper computes second-order scattering and a multiple-scattering factor from a small
2D LUT, approximating the infinite series of scattering orders as a geometric series
`F_ms = 1 / (1 - f_ms)`, and recommends the analytic solution of the integral to keep the transfer
factor in [0, 1].

## Gotchas
- Phase function sign conventions differ between sources (see HG above).
- Use the same wavelength-dependent coefficients for transmittance and in-scattering, or the
  medium will not conserve energy.

## Verify
- [ ] A medium with albedo 1 and no emission loses no energy (all out-scattered light appears as in-scattering).
- [ ] The phase function integrates to 1 numerically over the sphere for several g.
- [ ] Forward scattering (g > 0) brightens the medium when viewed toward the light under your chosen convention.

## Checked
2026-11-09. Read: pbr-book 4th edition Volume Scattering chapter pages "Volume Scattering
Processes" (absorption, out-scattering, attenuation coefficient sigma_a + sigma_s, albedo,
absorption transmittance formula) and "Phase Functions" (Henyey-Greenstein formula, convention
footnote, weighted sums of HG), and Hillaire, "A Scalable and Production Ready Sky and
Atmosphere Rendering Technique" (EGSR 2020: Beer-Lambert Equation 2, isotropic and
Cornette-Shanks phase, multiple scattering LUT and geometric series). Removed: the Schlick HG
approximation, the Rayleigh phase formula, the per-step energy-conserving integration code
(not confirmed on pages read), Wrenninge octaves, dual-lobe cloud advice, and the Frostbite page
source (not read). Corrected: the HG cosine sign now notes pbrt's convention.
Method: docs-checked 2026-11-09 against the pbr-book Volume Scattering pages and Hillaire's EGSR 2020 paper.
