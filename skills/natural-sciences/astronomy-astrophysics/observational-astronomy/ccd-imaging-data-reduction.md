---
id: natural-sciences.astronomy-astrophysics.observational-astronomy.ccd-imaging-data-reduction
name: ccd-imaging-data-reduction
category: natural-sciences
field: astronomy-astrophysics
product: observational-astronomy
tags: [observational-astronomy, data-reduction, ccd, cmos, bias, overscan, dark-current, flat-field, twilight-flats, dome-flats, cosmic-rays, lacosmic, ccdproc, astropy, iraf, fits, image-calibration, photometry, aperture-photometry, zero-point, standard-stars, extinction-coefficient, airmass, astrometry, wcs, astrometry-net]
level: practitioner
status: gated
description: "Reduce optical CCD imaging from raw frames to calibrated science images and photometry: bias/overscan, darks, flats, cosmic rays, astrometry, zero points and extinction."
sources: ["Howell, Handbook of CCD Astronomy (CUP)", "ccdproc and the Astropy CCD Data Reduction Guide (astropy.org)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CCD imaging data reduction

**Goal:** calibrated images whose pixel values are proportional to sky flux, with a WCS
and a photometric zero point — and the calibration steps documented so another person
gets the same answer.

## 1. Get the right calibration frames at the telescope
- **Bias** frames (zero exposure): 10–20 per night.
- **Darks** matching science exposure times and detector temperature, if dark current
  matters (cooled scientific CCDs often have negligible dark; CMOS and warm cameras don't).
- **Flats** per filter (and per binning/readout mode): twilight sky flats are usually best
  for large-scale illumination; dome flats are repeatable. Aim for ~30–50% of full well,
  avoid saturation and the non-linear regime; dither twilight flats to remove stars.
- Science frames **dithered** so bad columns and stars don't sit on the same pixels.
- Log everything: filter, exposure, airmass, seeing, clouds, focus changes.
- Standard-star fields (e.g. Landolt) at a range of airmasses if you need calibrated
  magnitudes rather than relative photometry.

## 2. The reduction chain (ccdproc / Astropy)
```python
import ccdproc as ccdp
from astropy import units as u
# per frame: overscan subtract and trim (detector-specific sections from the FITS header)
img = ccdp.subtract_overscan(raw, fits_section=OVERSCAN, median=True)
img = ccdp.trim_image(img, fits_section=TRIMSEC)
# combine bias with sigma clipping; subtract master bias; scale darks if needed
mbias = ccdp.combine(bias_list, method="average", sigma_clip=True)
img = ccdp.subtract_bias(img, mbias)
img = ccdp.subtract_dark(img, mdark, exposure_time="EXPTIME", exposure_unit=u.s, scale=True)
img = ccdp.flat_correct(img, mflat)   # normalises the flat by its MEAN unless norm_value is given
img = ccdp.cosmicray_lacosmic(img, sigclip=5)
```
`OVERSCAN`, `TRIMSEC`, `mdark`, `mflat` are placeholders for your instrument's sections and
master frames. Order matters: overscan → trim → bias → dark → flat.

## 3. Astrometry
Solve a WCS with astrometry.net (`solve-field`) or match to Gaia DR3 with SCAMP. Check the
residuals (typically well under a pixel for a good solution) and that distortion terms
(SIP) are present for wide fields.

## 4. Photometry
- **Aperture photometry** (photutils): aperture radius ~1–1.5× FWHM for best S/N on
  faint sources; use a larger aperture or aperture corrections for total flux. Measure sky
  in an annulus with sigma-clipped median.
- **PSF photometry** for crowded fields.
- **Zero point and extinction:** m_std = m_inst + ZP − k·X (+ colour term). Fit k
  (extinction) and colour terms from standards across airmass on a photometric night. On
  non-photometric nights, calibrate differentially against catalogue stars in the field
  (e.g. Pan-STARRS, SDSS, Gaia-synthetic photometry), noting the band transformations.
- Report uncertainties including Poisson, read noise, sky and zero-point error.

## Gotchas
- Flats taken with a different filter wheel position or focus — dust donuts move.
- Saturated or non-linear standards silently give wrong zero points; check peak counts.
- Shutter timing effects on very short exposures (centre vs edge exposure differs).
- Fringing in red/near-IR bands on thinned CCDs — needs a fringe frame.
- Mixing up gain (e⁻/ADU) when computing noise; take it from the instrument page, not memory.
- *Uncertainty note:* ccdproc 2.5.1 signatures were checked by import and `inspect.signature` (subtract_overscan, trim_image, combine with sigma_clip, subtract_bias, subtract_dark with exposure_time/exposure_unit/scale, flat_correct, cosmicray_lacosmic with sigclip). Flat fill level (30-50% of full well), aperture radius (1-1.5 x FWHM), bias count and the SCAMP/Gaia/Pan-STARRS advice are (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Master bias is flat and has the expected read noise; master flat has no stars.
- [ ] Flattened sky background is uniform to ~1% across the field.
- [ ] WCS overlays match catalogue stars at the image corners.
- [ ] Zero point stable across the night (or the night flagged non-photometric).
- [ ] A check star's magnitude matches its catalogue value within errors.
