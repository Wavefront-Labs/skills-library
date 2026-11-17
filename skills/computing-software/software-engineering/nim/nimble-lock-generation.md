---
id: computing-software.software-engineering.nim.nimble-lock-generation
name: nimble-lock-generation
category: computing-software
field: software-engineering
product: nim
tags: [nimble-lock-generation, nimble-lock-files, nimble-lock, nimble.lock, lockfile, reproducible-build, checksum, vcs-revision, nim]
level: practitioner
status: docs-checked
description: "Generate and use nimble.lock: nimble lock, lock --refresh, per-package relock, checksum verification, and the deprecated nimble upgrade alias."
sources:
  - https://github.com/nim-lang/nimble
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/workflow.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/nimble-reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nimble.lock

Goal: pin exact dependency revisions.

- `nimble lock` generates or updates `nimble.lock`, a JSON file (version 2) listing each package with `version`, `vcsRevision`, `url`, `downloadMethod` (`git` or `hg`), `dependencies` and `checksums.sha1`. Commit it.
- Build, install and develop read the lock and abort on a checksum mismatch.
- `nimble lock <pkg>` relocks one package. `nimble lock --refresh` resolves against the package repositories again (newest published versions).
- `nimble upgrade` is a deprecated alias of `nimble lock --refresh`.
- Locking is optional ("you don't have to use nimble lock"). Uses: consistency across a team, faster dependency resolution in CI, reproducible application builds.
- `nimble check` validates develop-mode dependencies against the lock; `nimble sync` aligns a working copy with it.

Gotchas:
- Regenerating the lock after dependency changes is manual.

Verify: `git diff nimble.lock` shows only the intended revisions.

## Checked

2026-11-03. Confirmed in the Nimble README, workflow guide and reference. Real error corrected: earlier text treated `nimble upgrade` as distinct; it is a deprecated alias of `lock --refresh`. Removed: `nimble lock --global`, `lock --help`, taskRequires-in-lock claim, and "libraries usually do not lock".
Method: documentation only; no commands were run.
