---
id: natural-sciences.astronomy-astrophysics.ds9.inspecting-images-scaling-regions-and-frames
name: inspecting-images-scaling-regions-and-frames
category: natural-sciences
field: astronomy-astrophysics
product: ds9
tags: [ds9, saoimage-ds9, fits-viewer, image-display, scaling, zscale, minmax, log-scale, asinh, colormap, regions, region-files, reg-format, wcs, frame-lock, blink, tile, rgb-frame, contours, catalog-overlay, xpa, samp, pyds9, astropy-regions, image-inspection]
level: practitioner
status: docs-checked
description: "Use SAOImage DS9 to inspect FITS images properly: zscale and stretch choices, region files in sky coordinates, locked frames for blinking, and command-line control."
sources: [https://ds9.si.edu/doc/ref/command.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting images in DS9: scaling, regions and frames

**Goal:** look at astronomical images so you actually see the faint stuff and the
artefacts, mark things in a way other tools can read, and compare images pixel-for-pixel
on the sky.

## 1. Open the right thing
- `ds9 image.fits` opens the image. Check the FITS header first: units, exposure,
  filter, whether it is already sky-subtracted.

## 2. Scaling: the most important setting
- Default min/max scaling makes almost every image look black with a few white dots.
- **zscale** sets scale limits with the IRAF algorithm (`-zscale` on the command line;
  options `contrast` and `sample`) and is the right first look for nearly all data.
- Scale functions: linear, log, pow, sqrt, squared, asinh, sinh, histequ. For high dynamic
  range (galaxy cores + outskirts) use log or asinh with percentage limits, e.g.
  `-scale mode 99.5`.
- Linear with tight limits around the background is how you spot flat-field residuals
  and gradients.

## 3. Pixel and coordinate readout
Set the WCS display to match your catalogue. If no WCS readout appears, the header has no
valid WCS: fix that before trusting any position.

## 4. Regions
- **Save in sky coordinates** so the region file works on any image of that field, not
  just this pixel grid. `-region save foo.reg` saves the regions; `-region format`
  accepts ds9, xml, ciao, saotng, saoimage, pros and xy.

## 5. Comparing images
- Load each image in its own frame, then lock the frames on WCS (`-lock frame wcs`
  locks all other frames to the current frame) so pan and zoom follow on the sky.
- **Blink** (interval in seconds, `-blink interval 1`) or tile frames to spot movers,
  variables and subtraction residuals.

## 6. Command line
`ds9 img.fits -zscale -saveimage jpeg out.jpg -exit` opens an image, sets zscale, saves a
snapshot of the DS9 window and quits.

## Gotchas
- Regions saved in **image** coordinates silently misplace on a different image.
- Comparing two frames with independent auto-scaling and concluding one is "deeper".

## Verify
- [ ] Image viewed at zscale and at a linear tight stretch before drawing conclusions.
- [ ] WCS readout present.
- [ ] Region files saved in sky coordinates with an explicit frame.
- [ ] Frames locked on WCS (and scale where relevant) when comparing.

## Checked
2026-11-01. Confirmed against the DS9 command-line reference (command.html): -zscale (IRAF algorithm), -scale
functions, -scale mode 99.5, -region save and format list, -lock frame wcs, -blink interval in seconds, -saveimage,
-exit. Removed: menu paths, region file text example, catalogue overlays, XPA/SAMP/pyds9 scripting, astropy-regions,
cube and RGB notes (no page read).
Method: documentation only; no commands were run.
