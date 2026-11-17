---
id: creative-arts.conservation-and-restoration.condition-reporting.photogrammetry-for-3d-documentation
name: photogrammetry-for-3d-documentation
category: creative-arts
field: conservation-and-restoration
product: condition-reporting
tags: [condition-reporting, documentation-photography, photogrammetry, 3d-documentation, structure-from-motion, agisoft-metashape, meshroom, colmap, turntable, scale-bars, london-charter]
level: advanced
status: draft
description: "Document objects in 3D by photographing overlapping views under diffuse light, building a scaled model, and recording processing steps and accuracy."
sources:
  - "Cultural Heritage Imaging - https://culturalheritageimaging.org"
  - "FADGI Technical Guidelines - https://www.digitizationguidelines.gov"
  - "Getty Conservation Institute - https://www.getty.edu/conservation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Photogrammetry for 3D documentation

**Goal:** a scaled 3D model usable for documentation, monitoring and visualisation.

## Capture
1. Fixed focal length lens; manual focus and exposure; diffuse light; matte, non-reflective background.
2. Overlap images by roughly 60 to 80 percent; capture rings around the object at several heights and also top and underside when possible.
3. Use a turntable with a non-featured background or move the camera around the object; avoid moving the object relative to scene features.
4. Include scale bars and, if wanted, coded targets for accuracy.
5. Capture a colour target.

## Processing
1. Align images in software (examples include Agisoft Metashape, RealityCapture, and open-source tools like Meshroom and COLMAP).
2. Build a dense point cloud and mesh; apply scale from the scale bars.
3. Generate texture; check for holes and distortions.
4. Export formats like OBJ or PLY with textures; record software and settings.

## Standards
Follow the principles of the London Charter for the computer-based visualisation of cultural heritage: document methods and sources, and make the processing transparent.

## Verify
- [ ] Scale checked against a known length.
- [ ] Mesh free of large holes and artefacts.
- [ ] Settings and raw images archived.

## Professional note
General guidance only, not a treatment recommendation for a specific object. Work on heritage objects needs the judgement of a qualified conservator, working to the AIC Code of Ethics and Guidelines for Practice (or the ECCO / Icon equivalent) and the owner's consent; test, document and prefer the minimum intervention. Check current safety data sheets and local regulations for every material named.
