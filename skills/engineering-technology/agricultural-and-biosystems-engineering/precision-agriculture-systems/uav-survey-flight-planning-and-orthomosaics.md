---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.uav-survey-flight-planning-and-orthomosaics
name: uav-survey-flight-planning-and-orthomosaics
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, uav-mapping, remote-sensing-agriculture, crop-sensing, drone-survey, ground-sample-distance, orthomosaic, photogrammetry]
level: practitioner
status: draft
description: "Plan a drone crop survey: ground sample distance, overlap, altitude and regulations, ground control and radiometric calibration, and processing to an orthomosaic."
sources:
  - "14 CFR 107.51 operating limitations (https://www.law.cornell.edu/cfr/text/14/107.51)"
  - "EASA, drones open category (https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/open-category-low-risk-civil-drones)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# UAV survey flight planning and orthomosaics

**Goal:** georeferenced, radiometrically consistent imagery of a field.

## Regulations
Check and follow the national drone regulations (for example registration, pilot certification, maximum altitude: 400 ft above ground level in the US (14 CFR 107.51(b)) and 120 m in the EU open category, visual line of sight, airspace authorisation, privacy). This is the operator's responsibility.

## Planning
1. **Ground sample distance (GSD)**: `GSD = (flight height x sensor width) / (focal length x image width in pixels)`; for crop scouting 2-5 cm per pixel is common; weed mapping needs about 1 cm or finer.
2. **Overlap**: about 75-80 percent forward and 65-70 percent side for photogrammetry of crops (higher for uniform canopy, where tie points are fewer).
3. **Flight height and speed** from GSD and camera shutter speed (avoid motion blur); mission planner software creates grids.
4. **Time and light**: fly within about two hours of solar noon, under stable light (clear or uniformly overcast), avoid shifting clouds; avoid strong wind.
5. **Ground control**: place ground control points (GCPs) measured with RTK or use an RTK/PPK-enabled drone for good absolute accuracy.
6. **Radiometric calibration**: photograph a calibrated reflectance panel before and after the flight, and use the sunshine sensor if multispectral, so that reflectance and indices are comparable across dates.

## Processing
Photogrammetry software builds the point cloud and orthomosaic; generate index layers such as NDVI from the red and near-infrared bands; export a GeoTIFF with correct projection.

## Verify
- [ ] Check GCP residuals and the orthomosaic registration against field boundaries and previous flights.
