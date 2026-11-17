---
id: computing-software.devops-ci-cd.turborepo.turbo-json-global-options-reference
name: turbo-json-global-options-reference
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, turbo-json-reference, global-options, globaldependencies, globalenv, globalpassthroughenv, concurrency, ui-setting, turbo-jsonc, no-update-notifier]
level: practitioner
status: docs-checked
description: "Root turbo.json global options: extends, globalDependencies, globalEnv, globalPassThroughEnv, ui, concurrency, noUpdateNotifier, envMode, and the deprecated daemon."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configure `turbo` with a `turbo.json` in the workspace root; use Package Configurations for granular control, and `turbo.jsonc` for comments with IDE support.

- **`extends`**: in a package `turbo.json`, `["//"]` inherits the root configuration; you may also extend other packages (`["//", "shared-config"]`). It must start with `"//"`. Ignored if used in the root `turbo.json`.
- **`globalDependencies`**: globs included in all task hashes; any matching change makes all tasks miss. Relative to `turbo.json`; they must be inside the repository's source control root. By default the root `package.json`, lockfile and source files of internal packages the root depends on are already in the global hash and cannot be ignored. `turbo prune` does not copy these files unless the `pruneIncludesGlobalFiles` future flag is on.
- **`globalEnv`**: variables whose changes affect all tasks (wildcard and negation syntax as in `env`).
- **`globalPassThroughEnv`**: variables made available to tasks; using it opts all tasks into Strict Mode. Turborepo has built-in passthrough variables such as `HOME`, `PATH`, `APPDATA`, `SHELL`, `PWD`. Passthrough values do **not** contribute to hashes; use `env` or `globalEnv` if changes should miss cache.
- **`ui`** (default `"stream"`): `"tui"` shows each log and allows interaction; `"stream"` outputs logs as they arrive, not interactive.
- **`noUpdateNotifier`** (default `false`): disables the new-version notification.
- **`concurrency`** (default `"10"`): integer of at least `1` or a percentage like `50%`. `1` forces serial runs; `100%` uses all logical processors. Ignored if the deprecated `--parallel` flag is passed.
- **`envMode`** (default `"strict"`): `"strict"` or `"loose"`.
- **`daemon`**: deprecated; no longer used by `turbo run` and removed in 3.0. The daemon is still used by `turbo watch` and the Turborepo LSP.

## Checked

2026-11-04. Read the introduction and Global options section of the configuration reference (`extends` through `daemon` and `envMode`); every default, rule and callout matches. Removed the invented Verify step.

Method: documentation only; no commands were run.
