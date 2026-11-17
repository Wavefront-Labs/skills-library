---
id: creative-arts.animation.art-direction.on-model-checks-across-departments
name: on-model-checks-across-departments
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, visual-continuity, on-model-check, model-sheet, qc]
level: advanced
status: draft
description: "Check characters, props and sets stay on model as they pass through design, modeling, rigging, animation, lighting and outsourcing; checkpoints, overlays and red-flag lists."
sources:
  - https://animationguild.org/
  - https://books.google.com/books?vid=ISBN9780823023493
  - https://en.wikipedia.org/wiki/Model_sheet
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# On-model checks across departments

Goal: the character the audience sees in shot 900 is the one approved on the model sheet.

## 1. Checkpoints
| Stage | Check |
|---|---|
| Model | turnaround overlay at matched camera and lens; proportions and silhouette |
| Rig | extreme poses and face shapes against the expression sheet |
| Animation | key poses from camera; off-model drawings or broken silhouettes in extremes |
| Lighting/surfacing | colour model; texture scale; line weight for NPR |
| 2D cleanup / outsource | model sheet beside every scene; head-height ratios |

## 2. Tools
- **Overlay**: render the CG model with the design camera and lens; overlay at 50% on the drawing.
  Mismatched lens (e.g. 35 mm vs the drawing's flatter look) is the most common reason a correct
  model "looks wrong"; test 50-85 mm equivalents.
- **Pose library tests**: 10-20 standard poses and expressions rendered for every rig version.
- **Red-flag list**: per character, the 5 features that break the likeness (eye spacing, snout length,
  hair silhouette). Reviewers check these first.

## 3. Off-model vs acceptable distortion
- Animation may squash and stretch or smear for a few frames; on-model is judged on held poses and
  frames that hold longer than about 4 frames.
- Stylised cheats (a cheek pushed for a 3/4 view) are fine if the sheet lists them.

## 4. Feedback
- Note off-model issues with an overlay of the sheet and a draw-over, filed against the department
  responsible, not just the shot.

## Verify
- [ ] Overlay test passed with design camera and lens.
- [ ] Rig tested against the expression sheet.
- [ ] Red-flag features checked on held poses.

Related: `creative-arts.animation.pipeline.character-consistency`,
`creative-arts.animation.character-design.model-sheet-turnaround`,
`creative-arts.animation.storyboarding.on-model-enough-for-boards`.
