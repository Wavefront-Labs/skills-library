---
id: engineering-technology.civil-engineering.civil-3d.surface-from-survey-data
name: surface-from-survey-data
category: engineering-technology
field: civil-engineering
product: civil-3d
tags: [civil-3d, surface, tin-surface, survey-data, breaklines, point-groups, boundaries, surface-from-survey, lidar, contours, surface-quality]
level: practitioner
status: draft
description: "Build a Civil 3D TIN surface from survey points, breaklines and boundaries: point groups, breakline types, outer boundary, build options, edits, and checks against data."
sources: ["Autodesk Civil 3D Help (Surfaces)", "Autodesk Civil 3D User's Guide", "Surveying standards of the local jurisdiction"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Surface from survey data in Civil 3D

Goal: a clean TIN that represents the existing ground, built from field data and verified against it.

## Steps
1. Import survey points (point file or survey database), assign point groups (ground shots, break shots, features) and use descriptions keys so field codes map to layers and point groups.
2. Create the surface (TIN) in Prospector > Surfaces. Add point groups and breaklines in the surface definition.
3. Breaklines: standard (3D lines with elevations at vertices), proximity (elevations from nearby points), wall (with vertical offset), non-destructive (preserve vertices, no triangle crossing). Add breaklines along road edges, top and toe of bank, kerbs, ridges and gullies: TINs interpolate straight lines between points.
4. Boundary: outer boundary to exclude triangles outside the surveyed area (otherwise long, thin triangles span the exterior). Hide boundary to remove void regions inside.
5. Build options: set the maximum triangle length (for example, shorter than your point spacing) and the "exclude elevations" ranges; enable "Use maximum triangle length" for non-rectangular data. Check "allow crossing breaklines" is off.
6. Edit: remove bad points or flat triangles ("swap edge"), add/delete lines, smooth contours if needed. Do not smooth the surface used for earthwork quantities unless intended.
7. Check surface statistics (point counts, min/max elevations), display contours and slope analysis, and compare spot elevations against independent control.

## Gotchas
- Mixed datums or vertical units can be hidden outliers.
- Large LiDAR sets: simplify or thin before building (or use terrain/raster workflows).
- Surfaces used for design must be named and locked to avoid accidental edits.

## Verify
Pick 5 control points; surface elevation within survey tolerance; no missing breaklines at kerb lines.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
