---
id: natural-sciences.astronomy-astrophysics.planetary-science.crater-counting-for-surface-ages
name: crater-counting-for-surface-ages
category: natural-sciences
field: astronomy-astrophysics
product: planetary-science
tags: [planetary-science, crater-counting, crater-size-frequency-distribution, csfd, model-ages, surface-dating, chronology-function, production-function, neukum, hartmann, craterstats, cratertools, arcgis, qgis, lroc, ctx, hirise, secondary-craters, crater-saturation, resurfacing, moon, mars, mercury, planetary-geology]
level: advanced
status: gated
description: "Derive model ages for planetary surfaces from crater counts: count-area definition, mapping craters in GIS, avoiding secondaries and saturation, fitting CSFDs in Craterstats."
sources: ["Michael & Neukum 2010, planetary surface dating from crater SFD (EPSL)", "Hartmann 2005, Martian cratering 8 (Icarus)", "Craterstats2 documentation (FU Berlin)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crater counting for surface ages

**Goal:** a crater size-frequency distribution (CSFD) for a geologically uniform unit and
a model age with an honest uncertainty — including the part of the uncertainty that comes
from the chronology model rather than your count.

## 1. Define the count area
- Map a **single geological unit** — uniform morphology, no obvious later resurfacing
  (lava flows, ejecta blankets, dust mantles). Mixing units mixes ages.
- Exclude areas where craters can't be seen or have been erased: steep slopes, ejecta of
  large young craters, secondary-crater chains, image artefacts, shadowed regions.
- Area matters: small areas (<~1000 km² on Mars at CTX scale, *rule of thumb* (gated: unconfirmed, source is paywalled or blocked) give few
  large craters and big statistical errors, especially for older ages.

## 2. Choose the images
- Consistent resolution and **illumination**: low-to-moderate sun (incidence ~55–80° (gated: unconfirmed, source is paywalled or blocked)
  shows topography; high sun hides small craters.
- Typical datasets: LROC NAC/WAC (Moon), CTX/HiRISE/THEMIS (Mars), MESSENGER MDIS (Mercury).
- Only count craters ≥ ~5–10 pixels in diameter (gated: unconfirmed, source is paywalled or blocked); below that, completeness drops.
- Work in an **equal-area** or locally appropriate projection so areas and diameters are
  right; tools like CraterTools (ArcGIS) and the QGIS equivalents measure on the sphere.

## 3. Mapping craters
- Mark rim-to-rim diameter with three points on the rim.
- Count every primary crater whose centre lies inside the area.
- **Secondaries:** clusters, chains, herringbone ejecta, elongated shapes, and
  over-abundance at small diameters point to secondaries — exclude them or exclude the
  size range they dominate.
- Note degraded/ghost craters separately; they may belong to an older surface.

## 4. Plot and fit
- Export (Craterstats reads `.scc`, `.diam` and `.stat`; checked in craterstats 3.6.11 source) and plot **cumulative** and
  **differential** or R-plots. Cumulative plots hide resurfacing kinks; check R-plots.
- Select the diameter range where the CSFD follows the **production function** (isochron
  shape). Departures signal:
  - roll-off at small D → resolution limit or resurfacing (erasure);
  - kink to a younger isochron at small D → partial resurfacing event (can be dated with
    resurfacing correction);
  - flattening at high density → **saturation/equilibrium**; ages are minimums.
- Fit with a named **production function + chronology function** pair (craterstats 3.6.11 `-lcs` lists "Moon, Neukum et al. (2001)", "Mars, Neukum-Ivanov (2001)" and "Mars, Ivanov (2001)"; the Mars PF/CF pairing differs between them, so name the one you use). Use Poisson-based fitting
  (Michael et al. 2016) for small counts.

## 5. Report
Area (km²), number of craters in fit range, diameter range, PF and CF names, model age
with statistical error, and note that model ages on Mars carry systematic uncertainty
of up to ~a factor of 2 for young surfaces from the chronology itself (*value depends on
age; check current literature*). Provide the crater file.

## Gotchas
- Counting across a unit boundary or onto a younger ejecta blanket.
- Deriving an age from craters only a few pixels across.
- Treating model ages from different chronology systems as directly comparable.
- Very young surfaces (few Myr) are dominated by small craters where secondaries and
  target properties (e.g. Martian lava flows vs regolith) matter most.

## Verify
- [ ] Count area is one mapped unit, with exclusions drawn and their area removed.
- [ ] Minimum counted diameter ≥ ~5–10 pixels; imaging conditions noted.
- [ ] Secondaries handled explicitly.
- [ ] Fit diameter range follows an isochron in an R-plot or differential plot.
- [ ] PF/CF named; statistical and systematic uncertainty stated separately.
