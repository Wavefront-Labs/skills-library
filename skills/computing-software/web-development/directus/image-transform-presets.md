---
id: computing-software.web-development.directus.image-transform-presets
name: image-transform-presets
category: computing-software
field: web-development
product: directus
tags: [transform-presets, sharp-transforms, transformation-keys, allowed-transformations]
level: advanced
status: docs-checked
description: "Use the Directus transforms parameter for Sharp operations and define transformation presets in project settings to limit generated asset variants."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/05.files/5.transform.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Advanced**: `transforms` is a two-dimensional array of Sharp operations, each `[name, ...args]`. In REST, booleans and other datatypes must be passed as strings.

```http
GET /assets/<file-id>?transforms=[["rotate", 90],["blur", 10],["tint", "rgb(255, 0, 255)"],["normalize", {"lower": 10, "upper": 50}]]
```

Sharp `.tint(255, 0, 255)` becomes `["tint", "rgb(255, 0, 255)"]`. Combine with basic params: `?transforms=[["flip"]]&fit=cover&width=300&height=100`.

**Presets**: to avoid generating a large number of files, restrict transformations with a storage asset preset created in the project's Settings section:
- Allowed Transformations (enable, disable or limit)
- Default Folder and Default Exports Folder (do not move existing files)
- Transformation Presets: key, fit, width, height, quality, upscaling, format, additional Sharp transformations

Request a preset by its `key` parameter. Default keys: `system-small-cover` (64x64), `system-small-contain` (64 wide), `system-medium-cover` (300x300), `system-medium-contain`, `system-large-cover` (800x800), `system-large-contain`.

## Checked

2026-11-04: the transforms parameter format, Sharp equivalents, REST string datatype note, preset options, and the six default transformation keys with sizes confirmed against the Directus Transform Files page. Reworded the Settings path and removed a Verify line the page does not state.

Method: documentation only; no commands were run.
