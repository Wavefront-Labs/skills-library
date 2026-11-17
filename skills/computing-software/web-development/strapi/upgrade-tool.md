---
id: computing-software.web-development.strapi.upgrade-tool
name: upgrade-tool
category: computing-software
field: web-development
product: strapi
tags: [strapi, upgrade, codemods, dry-run, versions, npx]
level: practitioner
status: docs-checked
description: "Upgrade a Strapi project with npx @strapi/upgrade (major, minor, patch, latest), dry runs, and what it does not do."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/upgrade-tool.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrade tool

```bash
npx @strapi/upgrade minor
```

Targets: `major` (next major), `minor` (latest minor and patch of the current major), `patch` (latest patch of the current minor), `latest`, and `to <version>` for a specific version (`--codemods-target` selects the codemod set for pre-releases). Options: `-n, --dry` (simulate; no files change, dependencies are not reinstalled), `-y, --yes` (answer yes to every prompt), `-p, --project-path`, `-d, --debug`, `-s, --silent`. A `latest` that crosses a major asks for confirmation.

## What it does
- Updates and installs the `@strapi/*` dependencies, then runs codemods that edit the code for the breaking changes up to the target version.
- Only updates `@strapi/*` dependencies declared with an exact version (for example `5.12.0`). If any use a range (`^5.12.0`) it lists them and asks whether to pin them all (yes writes exact versions; no stops; `--yes` answers yes).
- `npx @strapi/upgrade codemods ls` lists codemods and `codemods run` runs selected ones without updating dependencies.

## What it does not do
- It does not add, remove or move files and folders, and does not migrate data (database migrations do that).
- Back up the codebase and database first, and review the changes it made before re-running the app.
- For a major upgrade, first reach the latest minor and patch of your current major (the `to` command skips this check).

## Workflow
1. Commit or back up.
2. `npx @strapi/upgrade minor --dry`, read the output.
3. Run without `--dry` (the tool updates and installs dependencies itself), then review the modifications before re-running the app (`computing-software.web-development.strapi.dev-start-build-commands`).

## Checked

2026-11-04: checked against the Strapi docs page Upgrade tool (upgrade-tool). Confirmed: `npx @strapi/upgrade` targets and their semantics, `--dry`/`--yes` and other options, scope (dependencies, codemods, no file tree changes, no data migration), backup warning, latest-minor-first rule for major upgrades. Corrected: dependencies are installed by the tool, only exact-version `@strapi/*` entries are updated (ranges prompt for pinning), and the page recommends reviewing changes rather than a reinstall step. Added: the `to` command and the codemods subcommands.

Method: documentation only; no commands were run.
