---
id: creative-arts.animation.art-direction.lookdev-turntables
name: lookdev-turntables
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, look-development, lookdev-turntable, turntable, approval]
level: practitioner
status: draft
description: "Set up and review lookdev turntables: standard light rigs and HDRIs, grey and chrome balls, colour checker, camera and frame range, and what to approve before an asset goes final."
sources:
  - https://www.khanacademy.org/computing/pixar
  - https://help.autodesk.com/view/SGSUB/ENU/
  - https://en.wikipedia.org/wiki/Turntable
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lookdev turntables and approval

Goal: every asset is judged under the same conditions, so approval means the same thing for every asset.

## 1. Standard turntable scene
- **Lighting**: 2-3 locked setups - neutral studio HDRI, the show's key day state, and a night or
  interior state. Same exposure every time.
- **References in frame**: 18% grey ball, chrome ball, and a colour checker chart (render matches the
  chart = calibrated pipeline).
- **Camera**: fixed lens (e.g. 50 mm equivalent), asset framed to a standard height; asset rotates 360
  degrees over a set number of frames (e.g. 100-120), plus a light-rotation pass where the HDRI turns.
- Render with the production renderer and settings, at review resolution, with a slate (asset, version,
  artist, date).

## 2. Review checklist
- Silhouette and proportions against the design.
- Material read: metal vs plastic vs cloth distinguishable.
- Texture scale against a human-scale reference (a 1.8 m figure in frame).
- Holds up in every lighting state; no swimming or flicker.
- NPR assets: line and shadow behaviour through the rotation.

## 3. Approve then lock
- Approval is given on the turntable version; lookdev changes after approval require re-approval.

## Verify
- [ ] Turntable template used unchanged.
- [ ] Grey ball, chrome ball and checker in frame.
- [ ] Reviewed in all lighting states before approval.

Related: `creative-arts.animation.art-direction.texture-style-targets`,
`creative-arts.animation.art-direction.cross-department-approval-tracking`,
`creative-arts.animation.color.look-development-for-color-pipelines`.
