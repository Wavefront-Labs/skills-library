---
id: transportation-logistics.unmanned-aircraft-operations.inspection-survey-missions.gsd-overlap-and-capture-qa-for-mapping-and-inspection
name: gsd-overlap-and-capture-qa-for-mapping-and-inspection
category: transportation-logistics
field: unmanned-aircraft-operations
product: inspection-survey-missions
tags: [drone-mapping, photogrammetry, aerial-survey, inspection, gsd, ground-sample-distance, front-overlap, side-overlap, grid-mission, double-grid, orbit, facade-mission, oblique-imagery, gcp, ground-control-points, rtk, ppk, motion-blur, shutter-speed, terrain-follow, dji-pilot-2, dronedeploy, pix4d, metashape, field-qa]
level: practitioner
status: gated
description: "Planning mapping and inspection flights: computing GSD, choosing overlaps and patterns (grid, orbit, facade), setting exposure against blur, and checking capture before leaving site."
sources: ["https://www.pix4d.com/", "https://www.agisoft.com/pdf/metashape-pro_2_1_en.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GSD, overlap and capture QA for mapping and inspection

**Goal:** come home with images that reconstruct cleanly and resolve the defects you
were sent to find — the first time, without a re-fly.

## 1. Compute GSD from the requirement
**GSD (cm/px) = sensor width (mm) × height above target (m) × 100 /
(focal length (mm) × image width (px))**
Example, 4/3" sensor 17.3 mm wide, 12.3 mm lens, 5,280 px wide, at 100 m:
17.3 × 100 × 100 / (12.3 × 5,280) ≈ **2.7 cm/px**.
- Work backwards from the need: to see a 5 mm crack you want ~1–2 mm/px → fly very
  close or use zoom.
- Height is above the **target**, not take-off: on sloping terrain use terrain
  following (DSM-based) or GSD varies across the job.

## 2. Pick the pattern
| Job | Pattern | Typical settings |
|---|---|---|
| Orthomosaic of flat-ish land | Single grid, nadir | 75–80 % front, 65–70 % side |
| Forest, crops, uniform texture | Grid with higher overlap | 85 % front, 70–75 % side; fly higher |
| Buildings / 3D models | Double grid with oblique camera (~45–70°) + orbits | 80/70; orbits every 5–15° of arc |
| Towers, chimneys | Orbits at several heights, camera toward structure | ~10–15° steps, overlapping rings |
| Facades, bridges, dams | Vertical facade/linear mission at fixed standoff | 70–80 % overlap, constant distance |

Overlap percentages in this table (gated: unconfirmed, source is paywalled or blocked). The vendor page redirected without loading.

Fly grid lines **parallel to the wind** or to the long side of the area to reduce
turns; consistent speed matters more than direction for most cameras.

## 3. Camera settings
- **Motion blur:** ground speed × exposure time should be < ~0.5 × GSD.
  At 10 m/s and 2.7 cm GSD: exposure < 1/740 s → set 1/1000 s or faster.
- Shutter priority or manual; ISO as low as light allows; focus at infinity for mapping
  (or locked AF), or AF for close inspection.
- Mechanical shutter on (if available) to avoid rolling-shutter distortion.
- Lock white balance across the flight so the mosaic is consistent.
- Overcast light is ideal (no harsh shadows); avoid low sun for mapping.

## 4. Accuracy: GCPs, RTK and PPK
- **RTK/PPK** gives cm-level camera positions; still place **3–5 checkpoints** (gated: unconfirmed, source is paywalled or blocked) to prove
  accuracy.
- Without RTK, use **GCPs** (gated: unconfirmed, source is paywalled or blocked): at least 5, spread around edges and centre, more on
  long corridors (every few hundred metres); survey them with GNSS RTK; visible
  targets ≥ ~10 GSD across.
- Record coordinate system and vertical datum (ellipsoid vs. geoid) — a mismatch
  gives a constant height error of tens of metres.

## 5. Field QA before you pack up
1. Check image count vs. planned; no gaps from skipped triggers.
2. Spot-check sharpness (zoom 100 % on several images across the flight).
3. Run a quick low-res processing or the app's coverage map on site if possible.
4. Confirm geotags present and RTK fix status (fixed, not float) for the flight.
5. For inspections: confirm each required component has images at the required
   resolution from the required angles (use a checklist per asset).

## Gotchas
- Water, snow and sand don't reconstruct — higher overlap helps only partly.
- Reflective glass facades confuse matching; add obliques and accept gaps.
- Wind makes crabbing; side overlap shrinks in crosswind — add margin.
- *Overlap values are common vendor recommendations; projects may need more.*

## Verify
- [ ] GSD calculated from the requirement, with terrain following where relief varies.
- [ ] Pattern and overlap suit the subject.
- [ ] Shutter speed passes the blur rule.
- [ ] GCPs/checkpoints or RTK fix recorded with datum.
- [ ] Field QA done before leaving site.

## Checked

Jurisdiction: not applicable (photogrammetry arithmetic). Checked 2026-10-25 by recomputation: GSD = 17.3 x 100 x 100 / (12.3 x 5,280) = 2.66 cm/px (skill says about 2.7); motion-blur limit 0.5 x 2.7 cm at 10 m/s = 1/741 s (skill says 1/740). Overlap tables and GCP counts follow vendor guidance (Pix4D, Agisoft) that could not be fetched and are marked gated.

Method: documentation only; no commands were run.
