---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.posing-3d-drawing-figures-for-reference
name: posing-3d-drawing-figures-for-reference
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-3d, csp-3d-drawing-figure, pose-reference, camera-angle, body-proportions, pose-materials]
level: practitioner
status: draft
description: "Use CSP 3D drawing figures as pose and camera reference: adjusting proportions, posing joints with the manipulator, pose materials, matching lens/angle, and drawing over without stiffness."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://tips.clip-studio.com/en-us
  - https://www.clipstudio.net/en/functions/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Posing 3D drawing figures for reference

**Goal:** fast, accurate reference for difficult angles and foreshortening, drawn over
with life rather than traced stiffly.

## Setup
1. Material palette > 3D > Body type: drag a drawing figure (male/female) onto the
   canvas; it creates a 3D layer.
2. Object tool > Tool property: adjust **body shape/proportions** (height, head-to-body
   ratio, build) to match your character model sheet. Save the adjusted figure as a
   material for reuse.

## Posing
- Click a body part, then drag the manipulator rings to rotate joints; drag hands/feet
  for IK-style posing.
- Apply **pose materials** (Material palette > Pose) and tweak.
- Hand poses: hand setup in Tool property (open/closed sliders, preset hands).
- Pose scanner (newer versions): estimate a pose from a photo; refine manually.

## Camera
- Rotate/pan/zoom the camera with the controller above the model; match the panel's
  camera height and angle (low/high).
- Set perspective (field of view) in Tool property: wider for dramatic close shots,
  narrower for flatter long shots.
- Lock the camera when done.

## Drawing over
- Lower 3D layer opacity, draw on a new layer above.
- Push gesture beyond the model (exaggerate line of action), fix the mannequin's
  stiffness, add weight and costume.
- Hide or delete the 3D layer before export.

## Gotchas
- Default proportions differ from stylised characters; adjust first.
- Joints can rotate into impossible positions; check silhouette and anatomy.

## Verify
- [ ] Figure proportions match the character.
- [ ] Camera matches panel composition.
- [ ] Final drawing has gesture beyond the model; 3D layer hidden on export.
