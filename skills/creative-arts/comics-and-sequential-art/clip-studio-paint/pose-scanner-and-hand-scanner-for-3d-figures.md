---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.pose-scanner-and-hand-scanner-for-3d-figures
name: pose-scanner-and-hand-scanner-for-3d-figures
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-3d, csp-pose-scanner, hand-scanner, 3d-drawing-figure, pose-from-photo, pose-reference]
level: practitioner
status: draft
description: "Pose CSP 3D drawing figures from photos and a webcam: Pose scanner from an image, Hand scanner for hands, fixing scanned results and saving poses as materials."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pose scanner and hand scanner

Both are AI-assisted "technology preview" features in recent Clip Studio Paint versions; results are a
starting pose that you refine.

## Pose scanner (pose from a photo)
1. Place a 3D drawing figure (Material > 3D > Body type) in the panel.
2. Select it with the **Object** tool. In Tool property (or the object launcher), use **Pose scanner** and
   pick a photo of a person in the pose.
3. CSP estimates joint positions and applies them to the figure.
4. Refine: drag joints with the manipulator, fix hands and feet, check balance (weight over the support
   foot), then adjust camera to match the panel angle.

## Hand scanner
- With the figure selected, use **Hand scanner** in Tool property: it reads your hand through a webcam and
  copies the pose to the figure's hand in real time; capture when it looks right. Choose left or right hand.
- Alternative: hand pose presets in Tool property > Hand setup (grip slider between open and closed).

## Save
- Pose materials: drag the posed figure's pose into Material palette > Pose (or Register to material) to
  reuse on other characters and panels.

## Tips
- Photos with full body visible, little occlusion and neutral clothing scan best.
- Use your own reference photos or licensed ones; scanned poses from copyrighted photos are still
  derived from them.

## Gotchas
- Scanned poses often misread depth (arm toward camera vs away); rotate the camera to check from the side.
- Joint limits may be off; disable "restrict joint" only when needed.

## Verify
- [ ] Pose reads correctly from the panel's camera angle and from a side view.
