---
id: creative-arts.animation.scripting.aerender-cli
name: aerender-cli
category: creative-arts
field: animation
product: scripting
tags: [aerender, ae-scripting, extendscript, after-effects, command-line-render, render-farm-ae, headless, output-module-template, batch-render]
level: advanced
status: draft
description: "Render After Effects comps headlessly with aerender: project/comp/output flags, templates, frame ranges for farm chunks, multiple instances, logs and failure handling."
sources:
  - https://helpx.adobe.com/after-effects/using/automated-rendering-network-rendering.html
  - https://ae-scripting.docsforadobe.dev/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# aerender command-line rendering

**Goal:** render AE comps without the GUI: from scripts, CI-style automation, or a render farm.
`aerender` ships with After Effects (in the AE install folder; `aerender.exe` on Windows).

## Basic forms

```bash
# render what is already in the project's Render Queue
aerender -project "<PROJECT_ROOT>/gfx/titles_v007.aep"

# render one comp with saved templates to a given file
aerender -project titles_v007.aep -comp "EP104_TitleCard" \
  -RStemplate "Best Settings" -OMtemplate "ProRes 4444 alpha" \
  -output "<PROJECT_ROOT>/renders/EP104_TitleCard_v007.mov"

# frame range for a farm chunk, image sequence output
aerender -project titles_v007.aep -comp "EP104_Open" -s 0 -e 99 \
  -OMtemplate "PNG sequence alpha" -output "<PROJECT_ROOT>/renders/EP104_Open/EP104_Open_[#####].png"
```

Key flags: `-s`/`-e` start/end frames, `-i` increment, `-RStemplate` / `-OMtemplate` (must exist in
that user's AE preferences on the render machine), `-mem_usage` (image cache %, max memory %),
`-reuse` (reuse a running AE instance), `-log` file, `-v ERRORS_AND_PROGRESS` verbosity,
`-close DO_NOT_SAVE_CHANGES`.

## Farm considerations

- Each node needs AE installed and licensed (render-only nodes may be allowed by Adobe licensing
  terms; check current terms), the same version and plugins, fonts, and the templates.
- Split by frame ranges only for image-sequence outputs; movie files cannot be chunked and merged
  safely, render those as single tasks or render sequences and encode after.
- Deadline/OpenCue have AE submitters that wrap aerender (`creative-arts.animation.scripting.batch-render-scripting-and-farm-submission`).

## Exit codes and logs

aerender returns non-zero on failure, but some errors (missing fonts, missing footage substituted with
placeholders) still render "successfully". Parse the log for "WARNING", "missing" and "error" and fail
the job on them.

## Gotchas

- Paths with spaces need quotes; on Windows use full paths, not mapped drive letters that differ per node.
- Comp names must be unique in the project for `-comp`.
- Output folder must exist for image sequences.

## Verify

Run on a farm node as the farm's user account: frame count of outputs matches the range, the log has no
missing-footage/font warnings, exit code 0.
