---
id: computing-software.web-development.biome.git-hooks-pre-commit-framework-and-shell-script
name: git-hooks-pre-commit-framework-and-shell-script
category: computing-software
field: web-development
product: biome
tags: [biome, pre-commit, pre-commit-config, biomejs-pre-commit, hook-ids, local-hook, shell-hook, git-update-index, staged]
level: practitioner
status: docs-checked
description: "Use the biomejs/pre-commit hooks (biome-ci, biome-check, biome-format, biome-lint), a local hook, or a plain shell hook with --staged."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/recipes/git-hooks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**pre-commit framework.** Biome provides four hooks via the `biomejs/pre-commit` repository:
- `biome-ci`: check formatting, check imports are organised, lint.
- `biome-check`: format, organise imports, lint, apply safe fixes to committed files.
- `biome-format`: format committed files.
- `biome-lint`: lint and apply safe fixes.

After installing pre-commit and running `pre-commit install`, add `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/biomejs/pre-commit
    rev: "v2.0.6"
    hooks:
    -   id: biome-check
        additional_dependencies: ["@biomejs/biome@2.1.1"]
```

This runs `biome check --write` on `git commit`. You must pin the Biome version through `additional_dependencies` because pre-commit installs tools separately. If Biome is already an npm dependency, avoid updating two places by using a **local hook**:

```yaml
repos:
  - repo: local
    hooks:
      - id: local-biome-check
        name: biome check
        entry: npx @biomejs/biome check --write --files-ignore-unknown=true --no-errors-on-unmatched
        language: system
        types: [text]
```

The `files` option is optional because `--files-ignore-unknown=true` already skips unknown files.

**Shell script** (`.git/hooks/pre-commit`; the docs warn of cross-platform incompatibilities and recommend a dedicated tool). Check only: `npx @biomejs/biome check --staged --files-ignore-unknown=true --no-errors-on-unmatched` under `set -eu`. To also fix, the script fails if any staged file has unstaged changes (`git status --short | grep --quiet '^MM'`), runs `biome check --write --staged ...` and then `git update-index --again` to re-stage.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step. The biomejs/pre-commit README does not mention `additional_dependencies`; that claim rests on the git-hooks recipe page.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
