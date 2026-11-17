---
id: computing-software.software-engineering.nim.nimble-sync-and-deps-dir
name: nimble-sync-and-deps-dir
category: computing-software
field: software-engineering
product: nim
tags: [nimble-sync-and-deps-dir, nimble-lock-files, nimble-sync, nimble-setup, nimbledeps, local-deps, nimble-paths, isolated-environment, deps-dir, nim]
level: advanced
status: docs-checked
description: "Use nimble sync, setup, develop, check, nimbledeps and --localdeps to keep develop-mode dependencies aligned with nimble.lock."
sources:
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/workflow.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/folder-structure.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/nimble-reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimble sync, setup and local dependency directories

Goal: reproducible dependencies for a working copy.

- `nimble sync` synchronises develop-mode dependencies with the content of the lock file: it fetches the locked revision for each and downloads missing non-develop dependencies listed in the lock. `-l, --listOnly` only lists what it would do. After `git pull` brings in a new `nimble.lock`, run it.
- `nimble check` validates develop-mode dependencies against the lock file.
- `nimble setup` creates `nimble.paths` (compiler paths of the dependencies) and includes it in `config.nims`, creating that file if needed; it also adds `nimble.develop` and `nimble.paths` to `.gitignore`. These files are user specific; do not commit them.
- `nimble develop` options: `-p` (path), `-c` (create), `-a, --add`, `-r`, `-n`, `-i`, `-e`, `--withDependencies`, `--developFile`. A develop dependency is recorded as a `.nimble-link`.
- Project-local dependencies: a `nimbledeps` directory next to the .nimble file is used as `$nimbleDir`; `-l, --localdeps` selects local mode; `--nimbleDir` or `NIMBLE_DIR` sets any other directory.

Gotchas:
- The compiler cannot read .nimble files, which is why `nimble setup` writes `nimble.paths`.

Verify: `nimble check` reports no mismatch after `nimble sync`.

## Checked

2026-11-03. Confirmed in the Nimble guide (workflow, folder structure, reference) and README. Removed: `--inplace`, a hand-written `include "nimble.paths"` recipe, Docker/CI recipes, the claim that nimbledeps is git-ignored, and the version-range note.
Method: documentation only; no commands were run.
