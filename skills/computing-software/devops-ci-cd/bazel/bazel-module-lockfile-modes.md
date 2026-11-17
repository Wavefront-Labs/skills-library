---
id: computing-software.devops-ci-cd.bazel.bazel-module-lockfile-modes
name: bazel-module-lockfile-modes
category: computing-software
field: devops-ci-cd
product: bazel
tags: [module-bazel-lock, lockfile-mode, bzlmod, reproducible-builds, module-extensions, bazel-mod-deps]
level: advanced
status: docs-checked
description: "Use MODULE.bazel.lock and the four --lockfile_mode values (update, refresh, error, off) for reproducible dependency resolution."
sources: ["https://bazel.build/external/lockfile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MODULE.bazel.lock and --lockfile_mode

Bazel writes `MODULE.bazel.lock` at the workspace root after module resolution and extension evaluation. It only records what the current invocation used, so run the builds you care about before committing it. It holds:
- `registryFileHashes`: hashes of every registry file read, including `"not found"` entries for registries that lacked a module (this mutable information refreshes with `bazel mod deps --lockfile_mode=refresh`);
- `selectedYankedVersions`: non-empty only when yanked versions were explicitly allowed;
- `moduleExtensions`: per extension, `bzlTransitiveDigest`, `usagesDigest` and `generatedRepoSpecs`, with one `general` entry or per-OS/arch entries such as `os:linux`.

`--lockfile_mode`:
- `update` (default): reuse lock data to skip registry downloads and re-evaluation; add missing data.
- `refresh`: like update but always refreshes mutable data when switching to it, then roughly hourly.
- `error`: fail if anything consulted is missing or stale; never changes the file or hits the network during resolution. Superfluous entries are ignored, so a lockfile that passes may still be pruned by `update`.
- `off`: neither checked nor updated.

There is also a hidden lockfile at `$(bazel info output_base)/MODULE.bazel.lock`; its format is unspecified and only a performance cache. Needing to `bazel clean --expunge` to fix it indicates a bug in Bazel or an extension.

## Checked

2026-11-04. Read against the Bazel docs page(s): Bazel Lockfile (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the advice to use error mode in CI and the closing Verify line (neither is on the page).
Method: documentation only; no commands were run.
