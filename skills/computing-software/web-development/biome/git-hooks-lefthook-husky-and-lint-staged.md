---
id: computing-software.web-development.biome.git-hooks-lefthook-husky-and-lint-staged
name: git-hooks-lefthook-husky-and-lint-staged
category: computing-software
field: web-development
product: biome
tags: [biome, git-hooks, lefthook, husky, lint-staged, git-format-staged, staged-files, no-errors-on-unmatched, files-ignore-unknown, stage-fixed]
level: practitioner
status: docs-checked
description: "Wire Biome into Lefthook, Husky with lint-staged or git-format-staged, using staged files, --no-errors-on-unmatched and --files-ignore-unknown."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/recipes/git-hooks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Lefthook** (`lefthook.yml` at the repo root):

```yaml
pre-commit:
  commands:
    check:
      glob: "*.{js,ts,cjs,mjs,d.cts,d.mts,jsx,tsx,json,jsonc,css}"
      run: npx @biomejs/biome check --write --no-errors-on-unmatched --files-ignore-unknown=true {staged_files}
      stage_fixed: true
```

Drop `--write` and `stage_fixed` for a check-only hook; use `pre-push` with `{push_files}` for pushes. You do not need both `glob` and `--files-ignore-unknown=true`; the flag alone handles files Biome supports now and later, while `glob` gives more control. `--no-errors-on-unmatched` silences errors when no files are processed. Run `lefthook install` afterwards. Lefthook older than v2.1.6 may print raw ANSI sequences: upgrade, set `NO_COLOR`, or pass `--colors=off`.

**Husky** does not hide unstaged changes or list staged files, so pair it with lint-staged or git-format-staged. Set `"prepare": "husky"` in `package.json` scripts, and put `lint-staged` in `.husky/pre-commit`. lint-staged config in `package.json` maps globs to commands, such as `biome check --files-ignore-unknown=true` (check), `biome check --write --no-errors-on-unmatched` (format, organize imports, lint, safe fixes), `... --unsafe ...`, `biome format --write ...`, `biome lint --write ...`. A `"*"` key with `--files-ignore-unknown=true` passes every file.

**git-format-staged** does not use `git stash`, avoiding manual intervention when unstaged and staged changes conflict:

```shell
git-format-staged --formatter 'biome check --write --files-ignore-unknown=true --no-errors-on-unmatched --stdin-file-path="{}"' '*'
```

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
