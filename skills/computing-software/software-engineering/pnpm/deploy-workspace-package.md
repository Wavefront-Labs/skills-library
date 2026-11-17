---
id: computing-software.software-engineering.pnpm.deploy-workspace-package
name: deploy-workspace-package
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-deploy, deploy-target, deploy-legacy, deploy-prod, source-date-epoch, deploy-all-files, portable-package]
level: advanced
status: docs-checked
description: "Create a portable deployable from a workspace package with pnpm deploy: single-project filter, --prod, error codes, files included, legacy mode and reproducible output."
sources:
  - https://pnpm.io/cli/deploy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm --filter=<project> --prod deploy <target-dir>
```

The package files are copied to the target and all dependencies (workspace ones included) are installed into an isolated `node_modules` there, giving a portable package.

- The filter must select exactly one project: `ERR_PNPM_NOTHING_TO_DEPLOY` (none), `ERR_PNPM_CANNOT_DEPLOY_MANY` (several). An unsafe target such as the workspace root gives `ERR_PNPM_INVALID_DEPLOY_TARGET`. A non-empty target needs `--force` (`ERR_PNPM_DEPLOY_DIR_NOT_EMPTY`).
- Since v12.2.0 `injectWorkspacePackages` is not required: linked workspace deps become `file:` in a dedicated deploy lockfile. Ambiguous peers fail with `ERR_PNPM_DEPLOY_AMBIGUOUS_PEER`; pin with `overrides` or enable `injectWorkspacePackages`.
- `--legacy` or `forceLegacyDeploy: true` selects the older implementation.
- `enableGlobalVirtualStore` is ignored; a local virtual store keeps the target portable.
- Not copied: `packageManager` and `devEngines.packageManager`. The `prepare` script is not run. Accepts `pnpm install` options (`--ignore-scripts`, `--dev`, `--no-optional`).
- Files copied are what `pnpm pack` would include (`files`, then `.npmignore`, then `.gitignore`); `deployAllFiles: true` copies everything.
- With `SOURCE_DATE_EPOCH` set (v12.15.0), timestamps in `node_modules/.modules.yaml` are bounded so output and Docker layers repeat.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/deploy: filter and error codes, v12.2.0 injectWorkspacePackages change and ERR_PNPM_DEPLOY_AMBIGUOUS_PEER, --legacy/forceLegacyDeploy, enableGlobalVirtualStore ignored, fields not copied, prepare not run, files selection and deployAllFiles, SOURCE_DATE_EPOCH (v12.15.0). Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
