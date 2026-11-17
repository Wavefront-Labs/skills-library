---
id: creative-arts.animation.blender.clean-channels
name: clean-channels
category: creative-arts
field: animation
product: blender
tags: [blender, animation-cleanup, clean-channels, clean-keyframes, euler-filter, discontinuity-filter, delete-redundant-keys]
level: practitioner
status: docs-checked
description: "Remove redundant keys and dead channels in Blender: Clean Keyframes and its Channels option, Threshold, the Euler discontinuity filter, and deleting unused channels."
sources:
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/channels/editing.html
  - https://docs.blender.org/manual/en/latest/editors/timeline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# clean-channels

Goal: lean actions — no flat curves on every channel, no duplicate keys, no euler flips — before polish or export.

## Clean Keyframes and its Channels option (Graph Editor: Key > Density > Clean Keyframes, X)

- **Clean Keyframes**: finds redundant keyframes among the selected ones and deletes them. A key is redundant if it has the same value as its neighbours, even when the curve segments around it are not flat. **Threshold** (default 0.001) widens that to values that are almost the same.
- **Channels** option: cleans all keyframes, even unselected ones, in the selected F-curves; a curve left with only one keyframe is deleted entirely (for example the untouched scale channels of every bone after Whole Character keying). Big reduction for baked or whole-character actions.
- The manual warns this operator is likely to change curve shapes, so run it after bulk keyframe insertion and before tweaking curves by hand.
- Run on selected curves only if some flat channels are intentional (pinned holds for layering).

## Discontinuity (Euler) Filter

Channel > **Discontinuity (Euler) Filter**: cleans up Euler rotation channels that suffer from gimbal lock; the channels of all three Euler rotation axes must be selected for it to work. Run it before smoothing/decimating (see `fcurve-decimate-smooth`); that ordering is practice.

## Before export

- Cleaning with the Channels option removes flat per-bone scale curves, which shrinks the exported file; check how your engine treats missing scale tracks.
- Delete channels for non-deforming helper bones if the export doesn't include them (Channel > Delete Channels, X or Delete).
- The Only Show Errors filter lists curves and drivers that are disabled or have errors, which helps find orphan F-curves (for example after a bone rename).

## Gotchas

- Cleaning a layered (NLA Combine/Add) action can remove intentional zero-offset keys — check layer actions separately (practice).
- Threshold is a plain value difference in the channel's own units; for custom properties with large ranges raise it.
- Cleaning Constant-interpolated blocking removes held duplicate keys you might want for timing — clean after splining.

## Verify

Channel count and key count drop; playback looks the same; no ±360 spikes in rotation curves.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release), plus the graph.clean operator definition in graph_edit.cc. Confirmed: Key > Density > Clean Keyframes with Threshold (default 0.001) and a Channels option (default off) that deletes curves left with one key (editors/graph_editor/fcurves/editing.rst); Channel > Discontinuity (Euler) Filter needs all three Euler axes selected, and Channel > Delete Channels (channels/editing.rst); Only Show Errors filter (editors/timeline.rst). Wrong in the old text: there is no separate Clean Channels command, it is the Channels option of Clean Keyframes, and flat-at-default is not the stated rule. Removed the radians-versus-metres threshold claim.

Method: documentation only; no commands were run.
