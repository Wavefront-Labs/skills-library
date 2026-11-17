---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.limb-scanning
name: limb-scanning
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [limb-scanning, cad-cam-prosthetics, 3d-printed-socket, 3d-scanning, structured-light, residual-limb-scan, photogrammetry, stl]
level: practitioner
status: draft
description: "Capture residual limb shape digitally: scanner types, patient positioning and landmark marking, scan quality checks, file formats and common errors versus casting."
sources: ["Scanner manufacturer operating guides", "Smith, Michael and Bowker (eds.), Atlas of Amputations and Limb Deficiencies (AAOS)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Residual limb scanning

**Goal:** a clean, scaled 3D scan of the residual limb in a defined posture, ready for digital socket design.

## Equipment
- Structured-light handheld scanners and tablet-mounted depth sensors are common; photogrammetry and laser scanners also exist. Check the manufacturer's stated accuracy, and measure it with a calibration object (a known cylinder or cast of known size).

## Procedure
1. **Prepare the limb:** apply any liner or stockinette as the socket will use; mark bony landmarks with a pen or markers that show in the scan.
2. **Position:** standardise posture (e.g., standing or seated with the limb hanging for transtibial; transfemoral pelvis neutral); hold steady; reduce muscle tone changes. For casting-equivalent shape capture, apply the same hand pressures the prosthetist would use, or follow the software's guidance (some systems have a capture jig).
3. **Scan:** move the scanner smoothly in overlapping passes, keep distance in range, avoid highlights and fast motion; cover the whole surface including the distal end.
4. **Quality check:** no holes at distal end, no double surfaces; check with a measuring tape that circumferences agree within a few millimetres of the scan.
5. **Export** to STL, OBJ or PLY in millimetres; keep unit and orientation notes and the landmark file.
6. **Repeat** when limb volume or posture changes, since the limb is dynamic.

## Errors
- Movement during the scan, shiny or dark liners, missing landmarks, scale errors, mesh smoothing that removes bony prominences.

## Verify
- [ ] Known object scanned within the claimed accuracy.
- [ ] Landmark positions identifiable.
- [ ] File opens in the design software with correct scale.
