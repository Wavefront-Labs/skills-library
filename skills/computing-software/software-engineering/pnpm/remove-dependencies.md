---
id: computing-software.software-engineering.pnpm.remove-dependencies
name: remove-dependencies
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-remove, uninstall-package, remove-recursive, remove-global, trust-lockfile-remove]
level: intro
status: docs-checked
description: "Remove packages with pnpm remove (rm, uninstall, un): field-specific removal, workspace-wide -r, global packages, --lockfile-only and the v12.3.0 trust-lockfile check."
sources:
  - https://pnpm.io/cli/remove
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm remove <pkg>...        # aliases: rm, uninstall, un, uni
pnpm remove -D typescript   # only from devDependencies
pnpm remove -r left-pad     # every workspace package
pnpm remove -g eslint       # global; unlinks bins
```

- With no `--save-*` option the package leaves every dependency field. `-D`, `-O`, `-P` restrict to `devDependencies`, `optionalDependencies`, `dependencies`.
- Outside a workspace, `-r` removes from every package in subdirectories.
- `--lockfile-only`: edit `package.json` and `pnpm-lock.yaml` without touching `node_modules`.
- `--lockfile-dir <dir>` (not with `--global`) picks the lockfile location.
- Since v12.3.0 removal rewrites the lockfile, so the whole lockfile is verified against active supply-chain policies like `pnpm install` does. `--trust-lockfile` skips it, `--no-trust-lockfile` forces it. `--trust-policy`, `--trust-policy-exclude`, `--trust-policy-ignore-after` are accepted.
- `--filter <selector>` limits projects.

## Checked

2026-11-04. Confirmed aliases, save-* scoping, -r and -g behaviour, --lockfile-only, --lockfile-dir and the v12.3.0 trust-lockfile verification against pnpm.io/cli/remove. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
