---
id: creative-arts.animation.color.look-development-for-color-pipelines
name: look-development-for-color-pipelines
category: creative-arts
field: animation
product: color
tags: [color, ocio, color-management, color-pipeline, working-space, view-transform, agx, filmic, aces, texture-color-space, monitor-calibration, cross-tool, blender, photoshop, nuke, ffmpeg, animation]
level: advanced
status: draft
description: "Setting up OCIO color management, working/view transforms and texture tagging so color is predictable and identical across every tool in a pipeline"
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Look development for color pipelines

**Goal:** make a specific color value mean the *same thing* in every tool and
every stage of production — a texture painted in Photoshop, rendered in
Blender, comped in Nuke/Blender-compositor, and reviewed on someone's laptop
all agree on what "that red" looks like. This is infrastructure, not mood:
it's the plumbing that `creative-arts.animation.color.color-grading` (the
per-shot/per-mood craft) and `creative-arts.animation.color.color-scripting-and-key-frames`
(the pre-production plan) both depend on being correct *before* either of
them can work. If the pipeline's color management is wrong, a grade that
looks right in the compositor will look wrong on the delivered master, and no
amount of per-shot grading skill fixes that.

## The core problem this solves

Every image has two things attached to it whether or not anyone tags them: a
**color space** (how its numeric values map to actual light/display) and a
**transfer function** (linear vs. gamma-encoded). Pipelines break when a tool
assumes the wrong one — e.g. a diffuse texture authored in sRGB gets read as
linear data, or vice versa, and every surface using it is subtly wrong in a
way that often reads as "just off" rather than obviously broken, which makes
it hard to catch.

## OCIO: the mechanism

OpenColorIO (OCIO) is the open config format that most modern pipelines
(Blender, Nuke, Houdini, Krita, Natron) read from a single `config.ocio` file
so every tool shares one definition of "scene-referred," "display," and every
named transform (AgX, Filmic, ACES, Standard/sRGB).

- **Pin one OCIO config for the whole show**, checked into the pipeline repo,
  never the per-tool default that ships with the app. Two artists on two
  machines with two different default configs will get two different-looking
  renders from the *same* file.
- **Set the working/scene-referred space once** (e.g. Blender's default
  scene-linear Rec.709/sRGB primaries under AgX) and never change it
  mid-production — switching a show's view transform partway through
  re-renders the perceived mood of every already-approved shot (this is the
  same law `color-grading` states from the grading side; here it's stated from
  the config side, because it's enforced before any shot exists).
- **The view transform is a display-time lens, not data.** AgX/Filmic/ACES
  transforms change how scene-referred light *looks* on screen; they must
  never be baked into a texture or an intermediate render meant to be
  processed further, or the next stage double-applies it.

## Tagging color at the source: textures and inputs

The single highest-leverage, most commonly botched step:

- **Albedo/diffuse/color textures** are almost always authored and saved as
  **display-referred sRGB** (that's what a paint app shows you) — tag them
  `sRGB` on import so the renderer linearizes them correctly before lighting.
- **Data textures** (normal maps, roughness, metalness, AO, displacement) are
  **not colors** — tag them `Non-Color`/`Raw`/`Linear` (naming varies by tool)
  so no gamma curve is applied to values that are really vectors or scalars.
  Importing a normal map as sRGB is a classic, very visible bug (lighting
  looks wrong/noisy on bump detail) with a one-click fix once you know to
  look for it.
- **Keep a per-asset color-space manifest** (even a simple spreadsheet or a
  naming convention like `_sRGB` / `_raw` suffixes) so a re-import or a new
  artist doesn't have to guess per file.

## Reference and calibration

- **A physical or digital reference chart** (a color checker card, or a
  rendered chart of known RGB/greyscale values run through the pipeline end
  to end) is how you *prove* the chain is linear and correctly round-trips —
  render it, grade it, deliver it, and check the known values still read
  correctly against a reference. This is the pipeline-level equivalent of the
  scopes check in `color-grading`, but done once per pipeline setup/change,
  not per shot.
- **Monitor calibration is a precondition, not a nice-to-have.** Any color
  decision made on an uncalibrated/ambient-lit display is unverifiable — flag
  review sessions on uncalibrated hardware as provisional.
- **Cross-tool parity check:** push the same test image/chart through every
  tool in the chain (paint app → renderer → compositor → delivery encode) and
  confirm the chart's known values survive each hop within a small tolerance.
  Do this whenever a tool version, OCIO config, or view transform changes —
  not just at pipeline kickoff.

## Gotchas

- **ffmpeg and most delivery encoders don't speak OCIO.** The handoff from a
  scene-referred/OCIO-managed tool to ffmpeg must happen *after* the view
  transform has already been baked to a display-referred intermediate (see
  `creative-arts.animation.color.color-grading`'s delivery-trim section) —
  feeding ffmpeg a linear EXR and expecting it to know about AgX is a common
  and silent failure.
- **Plugins and asset packs from outside the pipeline** (a purchased texture
  pack, a stock HDRI) often assume a different default color management setup
  than your show's config — always re-tag on import rather than trusting the
  pack's own assumptions.
- **A version bump of the render engine or OCIO itself can silently change the
  default config path or named transforms.** Re-run the cross-tool parity
  check after any such update before trusting new renders against old ones.
- Uncertain / unconfirmed here: specific ACES version interop quirks across
  tool versions are fast-moving and tool/version-specific; verify against the
  current OCIO config shipped with your actual toolset rather than treating
  any specific version number here as current.

## Verify

1. Import a known reference chart as a texture, tag it correctly, render it
   through the pipeline, and confirm the output values match the chart's
   known reference values within tolerance.
2. Check a normal map's color-space tag explicitly: it must read
   Non-Color/Raw, never sRGB — inspect a lit surface using it for tell-tale
   noisy/wrong-looking bump shading if unsure.
3. Open the show's OCIO config file path in two different artists' machines/
   render nodes and confirm it resolves to the identical file (not two
   divergent local copies).
4. Take one delivered master frame and one scene-referred source frame of the
   same shot; confirm the only difference between them is the expected view
   transform + grade, not an extra unintended gamma shift.
5. After any tool/engine/OCIO version update, redo the cross-tool parity
   check before approving new work against the prior baseline.
