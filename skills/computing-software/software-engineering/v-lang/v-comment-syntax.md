---
id: computing-software.software-engineering.v-lang.v-comment-syntax
name: v-comment-syntax
category: computing-software
field: software-engineering
product: v-lang
tags: [v-comment-syntax, comments, nested-comments, vfmt, vfmt-off, shebang, vsh, v-lang]
level: intro
status: docs-checked
description: "Write V line and nested block comments, switch v fmt off for a region, and recognise the .vsh shebang line."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line and block comments

Goal: comment code the way V tooling expects.

- `// line comment` runs to the end of the line. `/* block */` comments may be nested:
  `/* outer /* inner */ still outer */`, so a region that already holds a block comment can be commented out.
- `v fmt file.v` formats a file; `v fmt -w file.v` writes the result back. The docs recommend running
  `v fmt -w` on save and before pushing. `v fmt -verify` and `v fmt -c` check formatting without writing.
- To keep the formatter away from a block, wrap it in `// vfmt off` and `// vfmt on` comments.
- In a `.vsh` script, line 1 may be `#!/usr/bin/env -S v`; after `chmod +x deploy.vsh` it runs as `./deploy.vsh`
  on Unix-like systems.

Gotchas:
- A line starting with `#` in V source is not a comment: top-level `#flag` and `#include` are C-interop directives.

Verify: `v fmt -verify file.v` accepts a formatted file; a comment wrapped in `// vfmt off` keeps its spacing after `v fmt -w`.

## Checked

Read the Comments, v fmt (including disabling formatting locally) and V scripts sections of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). Removed claims the page does not state: that `v fmt` normalises trailing comment spacing in general, "do not use block comments in committed files", and the shebang for ordinary `.v` files (the docs show it for `.vsh` scripts only). Tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08
