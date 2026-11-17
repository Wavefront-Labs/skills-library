---
id: computing-software.web-development.biome.ci-biome-check-vs-ci-and-github-actions
name: ci-biome-check-vs-ci-and-github-actions
category: computing-software
field: web-development
product: biome
tags: [biome, ci, github-actions, setup-biome, biome-ci, reviewdog, continuous-integration, node-setup]
level: practitioner
status: docs-checked
description: "Use biome ci instead of check in CI, set up Biome with biomejs/setup-biome in GitHub Actions, and install Node when the config has dependencies."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/recipes/continuous-integration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`check` vs `ci`.** Both run all checks, but use `biome ci` in CI. Compared with `check`, `ci`:
- has no `--write`/`--fix` option;
- integrates with runners (on GitHub, diagnostics print as GitHub annotations);
- lets you control the number of threads;
- with VCS integration enabled, uses `--changed` rather than `--staged`, since a remote repository has no staged files.
The docs expect `ci` to gain more features over time.

**GitHub Actions.** Biome provides a first-party action, `biomejs/setup-biome@v2`:

```yaml
name: Code quality
on:
  push:
  pull_request:
jobs:
  quality:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v5
        with:
          persist-credentials: false
      - name: Setup Biome
        uses: biomejs/setup-biome@v2
        with:
          version: latest
      - name: Run Biome
        run: biome ci .
```

If the Biome configuration has external dependencies (for example `extends` from a package), set up Node.js and install dependencies first, e.g. `actions/setup-node@v4` with a cache, then `npm ci`, or `yarn install --frozen-lockfile` or `pnpm install --frozen-lockfile`.

**Third-party.** `reviewdog-action-biome` (community maintained) runs Biome with reviewdog and posts PR comments and commit suggestions; it needs `pull-requests: write` and `reporter: github-pr-review`.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the sentence that pinning `version` gives reproducible builds and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
