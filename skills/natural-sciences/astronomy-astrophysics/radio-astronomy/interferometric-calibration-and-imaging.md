---
id: natural-sciences.astronomy-astrophysics.radio-astronomy.interferometric-calibration-and-imaging
name: interferometric-calibration-and-imaging
category: natural-sciences
field: astronomy-astrophysics
product: radio-astronomy
tags: [radio-astronomy, interferometry, aperture-synthesis, casa, tclean, clean, uv-coverage, visibilities, flux-calibration, bandpass-calibration, phase-calibration, gain-calibration, self-calibration, rfi, rfi-flagging, flagging, briggs-weighting, robust, primary-beam, vla, alma, meerkat, lofar, measurement-set, synthesized-beam]
level: advanced
status: docs-checked
description: "Calibrate and image radio interferometer data in CASA: flagging RFI, flux/bandpass/phase calibration, tclean weighting and masking, self-calibration and sanity checks."
sources: [https://casadocs.readthedocs.io/en/stable/api/casatasks.html, https://casadocs.readthedocs.io/en/stable/api/tt/casatasks.imaging.tclean.html, https://casadocs.readthedocs.io/en/stable/api/tt/casatasks.flagging.flagdata.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interferometric calibration and imaging

**Goal:** from a raw measurement set to a science image whose fluxes and structure you
trust, with residual errors understood. Examples use CASA task names; the logic carries to
other packages.

## 1. Inspect first
- `listobs` summarises a MeasurementSet: fields, scans, spectral windows, antennas, and
  so which source is the flux, bandpass and phase calibrator.
- Plot amplitude and phase against time, frequency and uv-distance for each calibrator
  in your plotting tool. Look for dead antennas, RFI spikes, shadowing, edge channels.
- Note the **uv coverage**: short snapshots have sparse coverage and image artefacts no
  algorithm fully removes.

## 2. Flag
- `flagdata` modes include `manual` (default), `quack` (start or end of each scan),
  `shadow` (antennas shadowing each other), `elevation`, `clip`, and the automatic
  `tfcrop` (time-frequency outliers against a fitted band shape) and `rflag`
  (sliding-window RMS statistics). `extend` grows existing flags; the docs recommend
  running it after `tfcrop` or `rflag`. `summary` reports counts.
- Inspect after automated flagging. Over-flagging throws away sensitivity;
  under-flagging creates stripes. `flagmanager` saves, restores and lists flag versions
  so you can roll back.

## 3. Calibrate (classic sequence)
1. **Set the flux scale** with `setjy`, which fills the model column with a calibrator's
   expected visibilities (use a standard flux calibrator with a named model for your array).
2. **Initial phase** solution on the bandpass calibrator over a short interval.
3. **Bandpass** (`bandpass`) per antenna and channel.
4. **Gain** (`gaincal`): time-variable gains from calibrator observations; solve phase on
   short intervals and amplitude on longer ones.
5. **Bootstrap fluxes** (`fluxscale`) to transfer the flux density scale from the standard
   calibrators to other sources.
6. `applycal` applies the solutions to the targets with interpolation.
Check solutions in plots: smooth phases, no jumps, sensible amplitude gains.

## 4. Imaging with tclean
- **Image size:** `imsize` must be even and factorizable by 2, 3 and 5 only for efficient
  FFTs (the docs point to `getOptimumSize`). Cover the primary beam, and bright sources in
  sidelobes that would otherwise put ripples into the field.
- **Weighting:** natural gives equal weight to all samples (low noise, coarser
  resolution, higher sidelobes); uniform favours resolution. **Briggs** uses `robust`
  from -2.0 (near uniform) to 2.0 (near natural); the docs say `robust=0` gives a good
  trade-off between resolution and sensitivity.
- **Deconvolver:** `hogbom` and `clark` are adapted classic CLEAN methods; `multiscale`
  suits images with complicated spatial structure and extended emission; `mtmfs` models
  wideband sky brightness with a multi-term Taylor polynomial (set `nterms` above 1).
- **Masking and threshold:** `usemask` can be `user`, `pb` or `auto-multithresh`, whose
  thresholds are set relative to residual statistics (`sidelobethreshold`,
  `noisethreshold`, `lownoisethreshold`). Set the stopping `threshold` (or `nsigma`)
  from the expected noise; cleaning noise biases fluxes.
- **Primary-beam correction:** `pbcor` (default False) applies the correction to the
  output restored image; apply it before quoting off-centre fluxes, and measure noise
  on the uncorrected image.

## 5. Self-calibration
If the target is bright enough to give good signal-to-noise per solution interval, iterate:
image, phase-only `gaincal` on the model, apply, reimage, shortening solution intervals
step by step; amplitude self-cal last and cautiously. Stop when rms and dynamic range stop
improving. Self-cal can **invent** structure from a bad model; keep the clean mask
conservative.

## Gotchas
- Wrong flux model for the calibrator or resolved calibrator on long baselines.
- Phase calibrator too far from the target or too infrequent, so phase errors smear the target.
- Comparing fluxes between images made with different weightings/uv-ranges (missing
  short spacings resolve out extended flux).
- Spectral-line work: Doppler frame and continuum subtraction (`uvcontsub` subtracts
  continuum emission in the uv domain).

## Verify
- [ ] Calibrator fluxes after `fluxscale` match catalogue or monitoring values.
- [ ] Residual image is noise-like with rms near the theoretical (sensitivity calculator) value.
- [ ] No stripes or rings from a few bad baselines or uncleaned bright sources.
- [ ] Off-axis fluxes are primary-beam corrected; beam size and weighting reported.
- [ ] Self-cal improvements tracked (rms and dynamic range per iteration).

## Checked
2026-11-01. Confirmed in the CASA docs: the task list (`listobs`, `flagdata`,
`flagmanager`, `setjy`, `bandpass`, `gaincal`, `fluxscale`, `applycal`, `tclean`,
`uvcontsub`) with their descriptions; the `flagdata` modes; in `tclean`: imsize rule,
weighting options and robust range, `robust=0` statement, deconvolver descriptions,
`usemask` options and thresholds, `pbcor` default. Removed: plotms (not in the task list),
AOFlagger, named flux calibrators, the 3-5 pixels per beam cell rule, robust 0-0.5 and
2-3x rms threshold, self-cal S/N 3-5 rule, 5-10% flux tolerance, and the listed
textbook sources (books, not read).
Method: documentation only; no commands were run.
