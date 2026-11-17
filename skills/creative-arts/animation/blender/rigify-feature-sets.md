---
id: creative-arts.animation.blender.rigify-feature-sets
name: rigify-feature-sets
category: creative-arts
field: animation
product: blender
tags: [blender, rigify, rigify-feature-sets, custom-rig-types, rigify-python, bpy]
level: advanced
status: docs-checked
description: "Extend Rigify with feature sets: installing zip feature sets from Rigify settings, writing custom rig types, and where the developer documentation lives."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/feature_sets.html
  - https://developer.blender.org/docs/features/animation/rigify/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigify-feature-sets

Goal: reusable custom rig types (props, vehicles, special limbs) generated like built-ins.

## What a feature set is
Third-party developers can provide sub-add-ons called *Feature Sets* that add new metarigs and rig types. Like regular add-ons they are installed from zip files through the Rigify settings in Preferences (Add-ons, with Rigify enabled). The manual lists two examples: Cessen's Rigify Extensions (the original Rigify rigs, repackaged to work without Rigify's legacy mode; names changed, so legacy-mode metarigs are not directly compatible) and Alexander Gavrilov's experimental rigs (extra-IK limbs, spline tentacle and more). For a GitHub repository, use Code, then Download ZIP, and install that file.

## Writing one
The manual defers to the developer documentation (Rigify section) for the feature set structure, the rig class API, generation stages, parameters UI and sample creation. Read it for the Blender version you target, and treat the class and stage names there as the source of truth rather than copying them from older tutorials.

## Debugging
Run Blender from a terminal so Python tracebacks are visible. Regenerate after every change to the feature set.

## Gotchas
- Rigify's rig types change between Blender versions, so test a production feature set on each Blender release you support.
- Metarigs from legacy-mode sets are not directly compatible with renamed ports.

## Verify
Install the zip, check its rig types appear in the Rigify Type dropdown (the dropdown can be filtered by feature set), add a sample, generate, then regenerate and confirm the rig still overwrites in place.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Rigify, Feature Sets and Creating Meta-rigs), branch blender-v5.2-release. Confirmed: feature sets provide metarigs and rig types, install from zip through Rigify settings, the two listed example sets, the Rigify Type dropdown filter by feature set, and the developer documentation link. Removed the file layout, stage list, method names and `MetarigError` claims, which the manual does not cover and which were not checked against the developer documentation.
Method: documentation only; no commands were run.
