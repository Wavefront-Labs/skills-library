---
id: computing-software.software-engineering.pnpm.patch-dependency
name: patch-dependency
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-patch, patch-commit, patched-dependencies, patch-remove, allow-unused-patches, patch-version-range]
level: practitioner
status: docs-checked
description: "Patch a dependency with pnpm patch and patch-commit: edit directory, patchedDependencies keys by exact version, range or name, priority order, patch-remove and allowUnusedPatches."
sources:
  - https://pnpm.io/cli/patch
  - https://pnpm.io/cli/patch-commit
  - https://pnpm.io/cli/patch-remove
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Workflow:

```sh
pnpm install                        # needed first, else ERR_PNPM_PATCH_NO_LOCKFILE
pnpm patch foo@1.0.0                # extracts to node_modules/.pnpm_patches/<pkg>
# edit files in that directory
pnpm patch-commit <path-printed>    # writes patch, registers it, runs install
pnpm patch-remove foo@1.0.0         # delete patch file and key
```

- With several installed versions, pnpm asks which to patch and whether to apply to all (key becomes the bare name).
- `--edit-dir`, `-d <dir>`: custom extraction dir; a non-empty one fails (`ERR_PNPM_PATCH_EDIT_DIR_EXISTS`, or `ERR_PNPM_EDIT_DIR_NOT_EMPTY` for the default). `--ignore-existing` ignores existing patches. `patch-commit --patches-dir <dir>` changes the output (default `patches`). Ambiguous target: `ERR_PNPM_AMBIGUOUS_PATCH_TARGET`.
- Do not patch a package's `package.json` to change dependencies; use `overrides` or a package hook.

```yaml
patchedDependencies:
  foo: patches/foo-1.patch
  foo@^2.0.0: patches/foo-2.patch
  foo@2.1.0: patches/foo-3.patch
```

Priority: exact version, then range, then name-only. Avoid overlapping ranges; exclude the sub-range from the broader one.

`allowUnusedPatches: true` stops installs failing on unapplied patches. A patch that fails to apply always fails the install; errors are reported together.

## Checked

2026-11-04. Confirmed the patch, patch-commit and patch-remove behaviour, error codes, options, patchedDependencies priority and allowUnusedPatches against pnpm.io/cli/patch, /cli/patch-commit and /cli/patch-remove. Changed the readPackage hook wording to the page's package hook. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
