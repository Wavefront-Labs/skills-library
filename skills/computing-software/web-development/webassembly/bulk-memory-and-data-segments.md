---
id: computing-software.web-development.webassembly.bulk-memory-and-data-segments
name: bulk-memory-and-data-segments
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, memory-copy, memory-fill, passive-data-segments, wasm]
level: practitioner
status: docs-checked
description: "Fast copies"
sources: ["https://webassembly.github.io/spec/core/syntax/modules.html", "https://webassembly.github.io/spec/core/syntax/instructions.html", "https://webassembly.github.io/spec/core/exec/instructions.html", "https://webassembly.github.io/spec/core/binary/modules.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk memory operations and data segments

Goal: use bulk operations.
- `memory.copy`, `memory.fill`, `memory.init` with passive segments, `data.drop`.
- Replace manual loops.
- The range is checked first: out-of-range `memory.init`, `memory.copy` and `memory.fill` trap.
Verify: a copy with overlapping source and destination ranges gives the expected bytes.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: the instruction names, passive data and `memory.init`, trapping range checks, the data count section.
Removed or reworded as unconfirmed: the engine-support claim and the atomic-bounds wording.
Method: documentation only; no commands were run.
