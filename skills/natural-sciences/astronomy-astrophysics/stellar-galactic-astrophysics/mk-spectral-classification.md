---
id: natural-sciences.astronomy-astrophysics.stellar-galactic-astrophysics.mk-spectral-classification
name: mk-spectral-classification
category: natural-sciences
field: astronomy-astrophysics
product: stellar-galactic-astrophysics
tags: [stellar-galactic-astrophysics, stellar-spectra, spectral-classification, mk-system, morgan-keenan, obafgkm, luminosity-class, balmer-lines, hydrogen-lines, helium-lines, ca-ii-k, tio-bands, g-band, standard-stars, spectral-atlas, rectification, continuum-normalisation, hr-diagram, effective-temperature, surface-gravity, mkclass, peculiar-stars, white-dwarfs]
level: practitioner
status: gated
description: "Classify stellar spectra on the MK system: normalise the spectrum, compare with standards, read temperature lines (H, He, Ca II, TiO) and gravity-sensitive luminosity criteria."
sources: ["Gray & Corbally, Stellar Spectral Classification (Princeton)", "Gray & Corbally MKCLASS program documentation", "Jacoby, Hunter & Christian 1984 spectral library"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MK spectral classification

**Goal:** assign a spectral type and luminosity class (e.g. G2 V, K3 III, B1.5 Ib) by
direct comparison with standards — the MK system is defined by its standard stars, not
by physical formulae.

## 1. Data requirements
- Classic MK classification uses blue-violet spectra (~3800–4800 Å) at ~1–3 Å resolution.
  Many diagnostics are there; red-only spectra need different criteria (good for M stars).
- S/N ≳ 50 for reliable luminosity criteria (*rule of thumb* (gated: unconfirmed, source is paywalled or blocked)).
- **Standards observed with the same setup** are ideal; otherwise degrade library spectra
  to your resolution before comparing.

## 2. Prepare the spectrum
1. Wavelength-calibrate and shift to rest frame (radial velocity) — a 100 km/s offset
   misaligns lines by ~1.43 Å at 4300 Å (computed: 4300 × 100 / 299792.458).
2. **Rectify** (normalise the continuum) consistently with the standards. For cool stars
   the true continuum is hidden by lines — classifiers often compare un-normalised flux
   shape instead. Be consistent.
3. Plot your star between candidate standards, same scale.

## 3. Temperature class — the sequence of key features
- **O:** He II lines (4541, 4686 Å (gated: unconfirmed, source is paywalled or blocked)) present; He II 4541 vs He I 4471 ratio sets subtype.
- **B:** He I strong (peaks ~B2), no He II after ~B0.5; H lines strengthening.
- **A:** Balmer lines peak at ~A0–A2; Ca II K grows through the A types.
- **F:** Balmer weakening, Ca II H&K strong; metallic lines and the G band (CH, 4300 Å)
  appear.
- **G:** G band strong; Ca I 4226 grows; Balmer ~equal to nearby metal lines.
- **K:** Ca I 4226 strong; molecular features begin; blue flux falling.
- **M:** TiO bands dominate (e.g. heads near 4954, 5167, 6159, 7054 Å (gated: unconfirmed, source is paywalled or blocked)).
Use **line ratios** of features with opposite temperature trends (e.g. He I 4471/Mg II 4481
in B–A stars (gated: unconfirmed, source is paywalled or blocked)), which are insensitive to S/N and normalisation.

## 4. Luminosity class (I–V)
Lower surface gravity (giants, supergiants) → narrower pressure-broadened lines and
changed ionisation balance:
- **B–A stars:** Balmer line *wings* narrower in supergiants.
- **F–G stars:** ratios such as Sr II 4077/Fe I 4045 (gated: unconfirmed, source is paywalled or blocked) and the strength of the Y II/Fe II
  blends rise with luminosity.
- **G–K stars:** CN band at ~4215 Å (gated: unconfirmed, source is paywalled or blocked) and Sr II 4077 strengthen in giants.
- **M stars:** shape of molecular bands; Na I and Ca II IR triplet in the red.

## 5. Flags and peculiarities
Note anything non-standard: emission (e), metal-weak/strong, Am/Ap (peculiar
abundances), carbon stars, composite spectra (two components — check line doubling). Write
the type with uncertainty, e.g. "K1–2 III" or "B3 V:" (colon = uncertain).

## 6. Automated help
MKCLASS (Gray & Corbally; named from memory (gated: unconfirmed, source is paywalled or blocked)) reproduces expert classification by comparing with standard
libraries; ML classifiers on survey spectra (LAMOST, SDSS) assign types at scale. Use them
as a first guess and inspect a subset by eye.

## Gotchas
- Interstellar reddening changes continuum slope — classify on lines, not colour.
- Rapid rotation broadens and weakens lines, mimicking higher luminosity or earlier type.
- Low metallicity makes stars look earlier (weaker metal lines).
- Mismatched resolution between object and standards.
- *Uncertainty note:* exact wavelengths and criteria above are summary-level; consult a
  spectral atlas for the precise definitions per subtype.

## Verify
- [ ] Spectrum at rest wavelength, resolution matched to standards.
- [ ] Type based on at least two ratio criteria, not one line strength.
- [ ] Luminosity class supported by gravity-sensitive criteria.
- [ ] Peculiarities and uncertainty noted in the type string.
- [ ] Type is consistent with independent data (colours, Gaia absolute magnitude).
