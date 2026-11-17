---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.speckle-resolution
name: speckle-resolution
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [speckle, ultrasound-speckle, speckle-reduction, compounding, speckle-tracking]
level: practitioner
status: draft
description: "Understand ultrasound speckle: origin, statistics, relationship to resolution cell, contrast detectability, compounding and filtering, and speckle tracking uses."
sources: ["Wagner et al., Statistics of speckle in ultrasound B-scans (IEEE Trans Sonics Ultrason, 1983)", "Szabo, Diagnostic Ultrasound Imaging: Inside Out", "https://www.ieee-uffc.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Speckle and resolution

**Goal:** know why ultrasound images look granular and how that limits detection and measurement.

## Facts
- **Origin:** many sub-resolution scatterers in the resolution cell produce echoes that interfere constructively and destructively, giving a granular pattern that depends on system and tissue microstructure, not directly on individual structures.
- **Size:** the speckle grain is about the size of the point-spread function: lateral width about wavelength times the f-number and axial length about half the pulse length.
- **Statistics:** for fully developed speckle the envelope follows a Rayleigh distribution; the amplitude mean-to-standard-deviation ratio is about 1.91, a quick test of whether a region is fully developed speckle.
- **Effect on detectability:** speckle noise limits low-contrast lesion detection; contrast-to-noise ratio depends on lesion size relative to the speckle grain.

## Reduction
- **Spatial and frequency compounding** (averaging images from different steering angles or frequency bands) reduces speckle variance roughly by the square root of the number of independent images, at some cost to resolution and frame rate.
- **Filtering** (median, anisotropic diffusion, wavelet) and adaptive methods; use with caution because they alter image texture used in diagnosis.

## Uses
- **Speckle tracking:** follows the pattern between frames to estimate tissue motion and strain (for example myocardial strain), valid because the pattern is stable over short motion.

## Verify
- [ ] Measure speckle SNR in a uniform phantom against the 1.91 value.
- [ ] Compounding effect on resolution and frame rate documented.
- [ ] Image processing validated not to remove diagnostic information.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
