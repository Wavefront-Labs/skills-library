---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.mtf-measurement
name: mtf-measurement
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [modulation-transfer-function, digital-radiography, dqe, mtf, slanted-edge, edge-spread-function, line-spread-function, presampled-mtf]
level: advanced
status: gated
description: "Measure presampled MTF with the slanted-edge method: edge device, angle, oversampled ESF, LSF and Fourier transform, limits like Nyquist, and typical errors."
sources: ["IEC 62220-1-1:2015 Characteristics of digital X-ray imaging devices - Determination of the detective quantum efficiency (https://webstore.iec.ch/en/publication/21937)", "Samei, Flynn and Reimann, A method for measuring the presampled MTF of digital radiographic systems using an edge test device (Med Phys 1998;25:102-113)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Presampled MTF with the slanted-edge method

**Goal:** the modulation transfer function (spatial-frequency response) of an imaging detector, free of aliasing.

## Equipment
An edge test device (tungsten or stainless-steel plate about 1 mm thick, with a polished, straight edge (gated: unconfirmed, source is paywalled or blocked)), mounted close to the detector surface and tilted by a small angle (about 1.5-3 degrees (gated: unconfirmed, source is paywalled or blocked)) relative to the pixel columns.

## Procedure
1. Acquire flat-field-corrected, linearised images with the edge at the detector centre and again rotated 90 degrees for the other axis; use a radiation quality given by the standard (for example RQA5) and adequate exposure to keep noise low.
2. Locate the edge position per row by fitting; compute the angle precisely.
3. Project pixel values onto the axis perpendicular to the edge, giving an **oversampled edge spread function (ESF)** with sub-pixel binning (for example bins of 1/10 pixel).
4. Differentiate the ESF to get the **line spread function (LSF)** (apply smoothing or fit-based methods that suppress noise).
5. Fourier transform the LSF; normalise to 1 at zero frequency to give MTF(f).
6. Report MTF at standard frequencies (for example 0.5, 1, 2, 3 cycles/mm) and the frequency at 50% and 10%.

## Limits and checks
- Presampled MTF can extend beyond the Nyquist frequency (1 / (2 x pixel pitch)); for a 0.15 mm pitch, Nyquist is 3.33 cycles/mm (computed: 1 / (2 x 0.15)).
- Edge quality matters (nicks, roughness give false drops); the edge must be opaque with negligible transmission and positioned flush with the detector.
- Tube focal spot blur and scatter lower the result; use a small focal spot and a long source-to-detector distance, and check with the scatter conditions the standard sets.
- Detector corrections (gain, offset) and post-processing must be off or documented.

## Verify
- [ ] Repeat measurements agree within a few percent at 1 cycle/mm.
- [ ] Horizontal and vertical MTFs reported; compare against the vendor specification.
- [ ] Software verified against a simulated edge of known MTF.
