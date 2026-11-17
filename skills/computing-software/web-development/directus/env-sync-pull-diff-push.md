---
id: computing-software.web-development.directus.env-sync-pull-diff-push
name: env-sync-pull-diff-push
category: computing-software
field: web-development
product: directus
tags: [env-sync-pull, env-sync-diff, env-sync-push, sync-files-git]
level: advanced
status: docs-checked
description: "Move Directus schema and configuration between instances with d6s sync pull, diff and push, reviewing deterministic sync files in git first."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/10.environment-sync/1.quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run in a git repository with profiles `source` and `target` already added.

```bash
d6s sync pull --from source     # writes ./directus/default/schema and /data
git add directus/ directus.config.json && git commit -m "Baseline"
d6s sync diff --to target       # plan only, applies nothing
d6s sync push --to target       # shows plan, asks to confirm, applies
```

Layout: `directus/default/schema/` has one JSON file per collection (names carry a content-hash suffix) plus `metadata.json`; `data/` has one file per configuration resource.

Properties:
- Output is deterministic (no timestamps, no reshuffling), so a repeat pull on an unchanged source leaves a clean tree and `git diff` shows only real changes.
- Default mode is `merge`: creates and updates, never deletes.
- Push verifies the target schema hash against the plan and stops if the target changed meanwhile.
- Re-running a completed push says nothing to push; safe for automation.
- Pushing configuration records may write `directus/default/id_map.json`; commit it when it changes.

## Checked

2026-11-04: pull, diff and push commands, directory layout, deterministic output, merge default that never deletes, schema hash check, repeat-push behaviour and id_map.json confirmed against the Directus Environment Sync quickstart. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
