---
id: creative-arts.animation.pipeline.ayon-project-anatomy
name: ayon-project-anatomy
category: creative-arts
field: animation
product: pipeline
tags: [project-anatomy, ayon, openpype, path-templates, roots, folder-structure, publish-templates, naming-convention-templates]
level: advanced
status: draft
description: "Configure Ayon project anatomy: roots per OS, work and publish path templates with tokens, folder/task types, and changing anatomy safely mid-project."
sources:
  - https://ayon.ynput.io/docs/admin_settings_project_anatomy/
  - https://ayon.ynput.io/docs/admin_server_project_management/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ayon project anatomy

**Goal:** every work file and publish lands at a predictable path generated from templates, the same on
Windows, Linux and macOS, so tools never hard-code paths.

## Parts of anatomy

| Section | Purpose |
|---|---|
| Roots | named storage roots per platform, e.g. `work`: `<DRIVE>:/projects`, `/mnt/projects`, `/Volumes/projects` |
| Templates - work | where artists' scene files live |
| Templates - publish | versioned outputs |
| Templates - others | hero/master versions, delivery, staging |
| Folder types / task types | Episode, Sequence, Shot, Asset...; Modeling, Rigging, Animation, Lighting... |
| Attributes | fps, resolution, frame start/end, handles, pixel aspect (inherited down the folder tree) |

## Template tokens (examples)

```
work:    {root[work]}/{project[name]}/{hierarchy}/{folder[name]}/work/{task[name]}
file:    {project[code]}_{folder[name]}_{task[name]}_v{@version}<_{comment}>.{ext}
publish: {root[work]}/{project[name]}/{hierarchy}/{folder[name]}/publish/{product[type]}/{product[name]}/v{@version}
```
`{@version}` applies the padding defined in anatomy (e.g. 3 digits); `<...>` marks optional parts.

## Design choices

- Keep `hierarchy` shallow and meaningful (`ep104/sq020/sh010`).
- Separate work and publish areas (publish read-only to artists).
- Product types (formerly families): `model`, `rig`, `animation`, `pointcache`, `render`, `review`: names
  appear in paths, so decide them early.

## Changing anatomy mid-project

Templates apply to new files; existing publishes keep their stored paths. Moving roots (new server) is done
by changing root values, not templates. Test changes on a copy project and check the loader still resolves
old publishes.

## Gotchas

- Windows path length (260 chars) with deep hierarchies and long product names; keep names short or enable
  long paths.
- Attributes set on the project but overridden on a shot win for that shot; check fps/frame ranges at shot
  level before rendering.

## Verify

Create a test shot and task, open a DCC from the launcher, save a work file and publish: both paths match the
templates on two operating systems.
