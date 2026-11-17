---
id: computing-software.web-development.webassembly.imported-globals-and-constants
name: imported-globals-and-constants
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, extended-const, imported-global-offset, dynamic-link-base, wasm]
level: practitioner
status: docs-checked
description: "Relocatable layout"
sources: ["https://webassembly.github.io/spec/core/valid/modules.html", "https://webassembly.github.io/spec/core/syntax/modules.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Imported globals and constant expressions

Goal: relocate modules.
- Constant expressions (segment offsets, global initialisers) can read imported globals, so a loader can supply base addresses at instantiation.
Verify: two instances with different bases do not collide.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: constant expressions have access to imported or previously defined globals.
Removed or reworded as unconfirmed: `__memory_base`/`__table_base` names, extended-const and the dynamic-linking sentence (not on a page read).
Method: documentation only; no commands were run.
