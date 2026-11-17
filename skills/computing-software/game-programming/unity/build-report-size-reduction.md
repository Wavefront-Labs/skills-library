---
id: computing-software.game-programming.unity.build-report-size-reduction
name: build-report-size-reduction
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-build, build-report, build-size, asset-size, game-programming]
level: practitioner
status: docs-checked
description: "Shrink Unity player builds using the build report and Editor.log size breakdown: find largest assets, texture/audio compression, stripping and duplicated content."
sources: ["https://docs.unity3d.com/Manual/ReducingFilesize.html", "https://docs.unity3d.com/ScriptReference/Build.Reporting.BuildReport.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build size reduction with the build report

**Goal:** know exactly what makes the build big and cut it, especially for store size limits.

## Read the report
- Editor log: Console window > More menu (three dots) > Open Editor Log, after a build. It gives a
  summary of assets by type, then lists individual assets in order of size contribution. Textures,
  sounds and animations usually dominate; scripts, scenes and shaders are usually small.
- Build Report Inspector package: shows build steps and assets from the build report file at
  `Library/LastBuild.buildreport`.
- `BuildReport` API: returned by `BuildPipeline.BuildPlayer`; `BuildReport.GetLatestReport` for the most
  recent build; properties include `packedAssets`, `strippingInfo`, `steps` and `summary`
  (`summary.totalSize`).

## Usual wins (the Unity manual lists these)
- Compressed texture formats, compressed meshes, compressed animation clips.
- Strip unreferenced code (managed code stripping).
- .NET Standard as API Compatibility Level restricts you to a smaller .NET API subset.
- Disable the built-in physics modules (`com.unity.modules.physics`, `com.unity.modules.physics2d`) in
  Package Manager if unused. Keep `com.unity.modules.physics` if you use local volumes.
- **Resources folder**: everything in it ships whether used or not; keep only assets you use.

## Gotchas
- Source file type does not matter: Unity re-codes imported assets to internal formats, so a layered
  `.psd` and a `.png` of the same texture build to the same size.
- Unity strips unreferenced assets itself, except those in `Resources`; no need to hand-delete them.
- File headers in the log are normally small but can be large with many big assets in `Resources`.

## Verify
- [ ] Largest assets in the Editor log recorded before and after a change.
- [ ] No asset near the top of the list is unexpected (debug content, uncompressed textures).

## Checked
2026-11-01. Confirmed against the Reducing the file size of a build manual page and the BuildReport
script reference: Editor log steps and contents, Build Report Inspector and file path, API members,
module and stripping advice, Resources folder behaviour, source-format irrelevance. Removed
unconfirmed claims: the packedSize code sample, ASTC block sizes, audio quality and sample-rate
figures, mesh channel options, Android bundle limits, the uncompressed-size note and the EditorOnly
tag advice.
Method: documentation only; no commands were run.
