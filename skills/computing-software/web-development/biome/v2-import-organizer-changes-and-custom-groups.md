---
id: computing-software.web-development.biome.v2-import-organizer-changes-and-custom-groups
name: v2-import-organizer-changes-and-custom-groups
category: computing-software
field: web-development
product: biome
tags: [biome, organize-imports, import-sorting, upgrade-v2, assist, groups, node-protocol, import-groups, biome-jsonc]
level: advanced
status: docs-checked
description: "Handle the v2 import organizer: config moved to assist, node: sorting change, merging exports, and a groups list to approximate v1 order."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/upgrade-to-biome-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The v2 organizer is new: sorting is customizable, `export` statements are organized, blank lines between imports are ignored, `import`/`export` are merged, and default sorting is more consistent. Results can differ from v1.

**Config moved** from the `organizeImports` field to an assist action. `biome migrate` rewrites

```json
{ "organizeImports": { "enabled": true } }
```

into

```json
{ "assist": { "actions": { "source": { "organizeImports": "on" } } } }
```

**Notable order change.** In 1.x Node modules without the `node:` protocol sorted before other imports. In 2.0 `import fs from "node:fs"; import pkg from "@a/package"; import path from "path";` is the order.

**Approximate the old order** with `options.groups` in biome.jsonc, listed in this order: `:BUN:`, `:NODE:`, `["npm:*", "npm:*/**"]`, `:PACKAGE_WITH_PROTOCOL:`, `:URL:`, `:PACKAGE:`, `["/**"]`, `["#*", "#*/**"]`, `:PATH:`:

```json
{
  "assist": { "actions": { "source": { "organizeImports": {
    "level": "on",
    "options": { "groups": [":BUN:", ":NODE:", ["npm:*", "npm:*/**"], ":PACKAGE_WITH_PROTOCOL:", ":URL:", ":PACKAGE:", ["/**"], ["#*", "#*/**"], ":PATH:"] }
  } } } }
}
```

It is not possible to reproduce v1 exactly; the docs recommend the new default as more consistent and simpler. See the organize-imports action documentation for full group syntax.

## Checked

2026-11-08. Read the upgrade-to-biome-v2 page in full. Unchanged: new organizer features, organizeImports moved to the assist action, the node: sorting change, the groups list and the note that v1 cannot be reproduced exactly. Removed: an inference about bare path being treated as a package and the invented Verify step.

Method: documentation only; no commands were run.
