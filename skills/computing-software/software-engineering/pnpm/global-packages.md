---
id: computing-software.software-engineering.pnpm.global-packages
name: global-packages
category: computing-software
field: software-engineering
product: pnpm
tags: [global-install, pnpm-add-global, isolated-install-groups, global-bin-dir, pnpm-home, global-list, approve-builds-global, link-local-global]
level: practitioner
status: docs-checked
description: "Manage globally installed pnpm tools: isolated install groups, comma versus space grouping, list depth limits, PNPM_HOME bin directory, what cannot be global, and build approval."
sources:
  - https://pnpm.io/global-packages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm add -g typescript prettier        # two isolated installs
pnpm add -g eslint,prettier            # one shared install group
pnpm list -g
pnpm remove -g eslint
```

- Never use `sudo`; modifying commands fail with `ERR_PNPM_SUDO_NOT_SUPPORTED`.
- Each space-separated package gets its own directory at `{pnpmHomeDir}/global/v11/{hash}/` with its own `package.json`, `node_modules` and lockfile. A comma list bundles packages into one group that shares peers and is removed together. `pnpm add -g <pkg>` replaces every group containing `<pkg>`; re-add the whole group or use `pnpm update -g`.
- Contents live in the global virtual store (`{storeDir}/links`) by default. Orphaned targets older than five minutes are cleaned on the next `add -g`, `update -g` or `self-update`.
- `pnpm list -g` shows all top-level packages. `--depth>0` works only with one group or a positional argument that narrows to one group, else `ERR_PNPM_GLOBAL_LS_DEPTH_NOT_SUPPORTED`.
- `pnpm install -g` with no arguments is unsupported. Cannot install globally: pnpm itself (`ERR_PNPM_GLOBAL_PNPM_INSTALL`, use `pnpm self-update`), a package whose bin a `pnpm shim` already provides (`ERR_PNPM_GLOBAL_BIN_CONFLICT`), `crate:` and Python dependencies. `pnpm add -g rust` installs the Rust toolchain.
- Bins go in `$PNPM_HOME/bin`; run `pnpm setup` to put it on PATH; `pnpm bin -g` prints it.
- `pnpm add -g .` registers the local package's bins.
- Builds need approval: `pnpm add -g --allow-build=esbuild esbuild`, or `pnpm approve-builds -g`, which writes one `allowBuilds` policy to the global packages directory's `pnpm-workspace.yaml` and rebuilds only affected groups.

## Checked

2026-11-04. Confirmed against pnpm.io/global-packages: isolated install groups and comma bundling, replacement rule, directory layout and five-minute orphan cleanup, list depth rules and error code, uninstallable cases and error codes, bin location and pnpm setup, pnpm add -g ., build approval. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
