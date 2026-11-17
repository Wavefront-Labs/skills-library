---
id: natural-sciences.astronomy-astrophysics.astropy.fits-wcs-units-and-coordinates
name: fits-wcs-units-and-coordinates
category: natural-sciences
field: astronomy-astrophysics
product: astropy
tags: [astropy, python, fits, astropy-io-fits, fits-header, wcs, astropy-wcs, world-coordinates, pixel-coordinates, units, astropy-units, quantity, skycoord, coordinates, icrs, galactic, altaz, astropy-time, astropy-table, cutout2d, photutils, reproject, astroquery, memmap]
level: practitioner
status: verified
description: "Core Astropy craft: read/write FITS safely, convert pixels to sky with WCS, carry units with Quantity, transform SkyCoord frames, handle Time scales and Tables, and avoid the off-by-one traps."
sources: ["Astropy documentation (docs.astropy.org)", "Astropy Learn tutorials"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FITS, WCS, units and coordinates with Astropy

**Goal:** do the everyday astronomical-computing chores correctly — the bugs here are
silent (wrong pixel, wrong frame, wrong units), so the method is about making them loud.

## 1. FITS I/O
```python
from astropy.io import fits
with fits.open("image.fits") as hdul:      # context manager closes the file
    hdul.info()                             # which HDU holds the data?
    hdr = hdul[1].header                    # often SCI in extension 1, not 0
    data = hdul[1].data.astype("float64")  # copy out; with memmap the array is tied to the file
```
- **Axis order:** NumPy arrays are `data[y, x]` (row, column); FITS keywords `NAXIS1` is x.
- **Indexing:** FITS/WCS conventions are 1-based; NumPy and Astropy's pixel APIs are 0-based.
- Integer images with `BSCALE`/`BZERO` are scaled on read — keep floats on write unless you
  mean it (`do_not_scale_image_data` if you need raw).
- Writing: `fits.writeto("out.fits", data, header=hdr, overwrite=True)`; add a `HISTORY` card
  describing what you did.
- Validate odd files with `hdul.verify("fix")` and read the warnings.

## 2. WCS: pixels ↔ sky
```python
from astropy.wcs import WCS
w = WCS(hdr)                                  # use the header of the HDU with the data
sky = w.pixel_to_world(512, 512)              # 0-based pixel → SkyCoord
x, y = w.world_to_pixel(sky)
```
- `pixel_to_world`/`world_to_pixel` (high-level, 0-based) are preferred; the older
  `all_pix2world(..., origin)` requires you to pass the origin — getting it wrong is a
  one-pixel shift.
- `wcs_pix2world` ignores SIP distortion; `all_pix2world` includes it.
- Cutouts that keep a valid WCS: `astropy.nddata.Cutout2D(data, position, size, wcs=w)`.
- To align images on a common grid: the `reproject` package (`reproject_interp`, or
  `reproject_exact` for flux conservation).

## 3. Units
```python
import astropy.units as u
d = 10 * u.pc
(d / (3e5 * u.km/u.s)).to(u.yr)
flux = 1e-17 * u.erg/u.s/u.cm**2/u.AA
flux.to(u.mJy, equivalencies=u.spectral_density(5000*u.AA))
```
- Conversions between wavelength/frequency/flux-density need explicit **equivalencies**;
  Astropy refuses rather than guessing — that's the point.
- Magnitudes: `u.ABmag`; logs and dex need care (`u.dex`).
- Strip units only at the boundary with code that can't take them: `q.to_value(u.km)`.

## 4. Coordinates
```python
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
c = SkyCoord("05h35m17.3s -05d23m28s", frame="icrs")
c.galactic
site = EarthLocation(lat=19.82*u.deg, lon=-155.47*u.deg, height=4200*u.m)  # example site
c.transform_to(AltAz(obstime=Time("2026-11-01T10:00:00", scale="utc"), location=site)).alt
```
- `SkyCoord` arrays are much faster than looping over scalars.
- Name lookup `SkyCoord.from_name()` needs network; cache results in scripts.
- AltAz transforms download IERS Earth-rotation data; offline machines need
  `iers.conf.auto_download = False` and accept lower precision.

## 5. Time and Tables
- `Time` carries a **scale** (utc, tt, tdb): `t.tdb`, `t.jd`, `t.mjd`; barycentric
  correction via `t.light_travel_time(coord, location=site)`.
- `astropy.table.Table` / `QTable` (keeps Quantity columns): read/write FITS, ECSV
  (keeps units and metadata), VOTable; `join`, `vstack`, `group_by`.

## Gotchas
- Using the primary-HDU header for WCS when the data are in an extension.
- Plotting with `imshow` without `origin="lower"` flips the image relative to FITS.
- Saving a Table to CSV loses units — use ECSV.
- Ecosystem drift: check your Astropy version against the docs version you read. Every code block above was executed on Astropy 8.0.2 (Python 3.14): pixel_to_world(99, 99) on a header with CRPIX 100 returns CRVAL and world_to_pixel round-trips; all_pix2world(99, 99, 0) equals all_pix2world(100, 100, 1); Cutout2D with size (ny, nx) gives shape (40, 60) and shifts CRPIX; 10 pc / 3e5 km/s = 32.6 yr; the spectral_density conversion works and the same conversion without it raises UnitConversionError; QTable round-trips units through ECSV while CSV drops them.

## Verify
- [ ] `hdul.info()` checked and the right HDU's header used for WCS.
- [ ] A catalogue star placed via `world_to_pixel` lands on the star in the image.
- [ ] Every physical quantity carries units until final output.
- [ ] Coordinate frames and time scales are explicit in code.
