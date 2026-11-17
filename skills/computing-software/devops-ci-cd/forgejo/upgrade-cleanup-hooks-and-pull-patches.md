---
id: computing-software.devops-ci-cd.forgejo.upgrade-cleanup-hooks-and-pull-patches
name: upgrade-cleanup-hooks-and-pull-patches
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [repository-hooks-cleanup, repo-path, pulls-directory, v16-v17-cleanup]
level: advanced
status: docs-checked
description: "Reclaim disk space after v16 and v17 by deleting obsolete hook files and migrated pull request patches."
sources:
  - https://forgejo.org/docs/latest/admin/upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two optional cleanups appear in the version-specific upgrade notes. Both assume `REPO_PATH` points at the directory containing all repositories, for example `/path/to/forgejo/data/forgejo-repositories`.

From any version before 17.0 to 17.0 or later: Forgejo used to download a `.patch` file for each migrated pull request and keep it in the repository's pulls directory. They are unnecessary and unused, so they can be removed with `find "$REPO_PATH" -mindepth 3 -maxdepth 3 -name pulls -exec rm -rf {} \;`.

From any version before 16.0 to 16.0 or later: the Git hooks Forgejo needs are centralized since v16.0.0, so the old generated hooks and sample files in each existing repository are safe to delete. Custom user-defined server-side Git hooks are disabled by default and the project recommends against them for security reasons. If custom hooks were never added to any repository, delete with `find "$REPO_PATH" -mindepth 3 -maxdepth 3 -name hooks -exec rm -rf {} \;`. When unsure, the guide gives a check command: if it returns no paths there are no custom hooks and deletion is safe.

Forgejo webhooks are a separate feature and are not affected. The page recommends the hooks cleanup especially for instances with many repositories.

## Checked

Date: 2026-11-07
Confirmed against the "Upgrade guide" page (forgejo.org/docs/latest/admin/upgrade/), read in full including its code blocks: the `REPO_PATH` assumption and example, the pulls-directory `find` command for upgrades from before 17.0, the hooks `find` command, the centralization of hooks since v16.0.0, custom hooks disabled by default, webhooks unaffected, and the check command whose empty output means no custom hooks.
Corrected: reworded the closing sentence to the page's actual recommendation. The page also covers deleting `*.sample` files and `description` files; this skill does not repeat those commands.
Method: documentation only; no commands were run.
