---
id: computing-software.devops-ci-cd.turborepo.upgrading-to-turborepo-2-behavior-changes
name: upgrading-to-turborepo-2-behavior-changes
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, upgrade-2-0, strict-env-mode, envmode, root-implicit-dependency, filter-changes, ignore-flag-removed, scope-flag-removed, only-flag]
level: advanced
status: docs-checked
description: "The 2.0 behaviour changes to check: Strict env mode default, root as implicit dependency, removed --ignore and --scope, engines hashing, stricter --filter, and --only."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/upgrading.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo 2.0 includes behaviour and correctness changes to `turbo run`. They may or may not affect your codebase:

- **Strict Mode for environment variables is the default** (was Loose Mode). If scripts seem to miss variables, opt back out per command with `--env-mode` to migrate incrementally, and update the `env` key so you can drop the flag soon. To set Loose Mode as the repository default use the `envMode` configuration.
- **Workspace root directory is an implicit dependency of all packages.** Keep as little code in the root as possible; root changes, and changes to Internal Packages used by the root, cause cache misses for all tasks. Consider moving code into a package.
- **`--ignore` removed** in favour of `--filter` and graph correctness changes.
- **`--scope` flag removed** (deprecated since 1.2).
- **`engines` field in the root `package.json` is now used in hashing.**
- **`--filter` no longer infers namespaces** for package names.
- **`--filter` now errors** when no package names or directories are matched.
- **`--only` restricts task dependencies** instead of package dependencies.

Each change links to a pull request in the vercel/turborepo repository in the docs.

## Checked

2026-11-04. Read the "Upgrading to 2.0" step on `turbo run` changes in full; all eight changes match. Removed the invented Verify step.

Method: documentation only; no commands were run.
