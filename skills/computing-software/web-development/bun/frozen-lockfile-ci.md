---
id: computing-software.web-development.bun.frozen-lockfile-ci
name: frozen-lockfile-ci
category: computing-software
field: web-development
product: bun
tags: [frozen-lockfile, bun-ci, reproducible-install, ci-install]
level: practitioner
status: docs-checked
description: "Make Bun installs reproducible in CI with bun ci or --frozen-lockfile, and know what happens without a lockfile or with a mismatching package.json."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/install.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/lockfile.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bun does not enable `--frozen-lockfile` in CI automatically. Pass it yourself or use `bun ci`.

```bash
bun ci                              # CI install, equivalent to --frozen-lockfile
bun install --frozen-lockfile       # exact lockfile versions; fails if package.json adds, removes or changes a package version
bun install --frozen-lockfile --dry-run
```

Rules and gotchas:
- Commit `bun.lock` to git; the frozen install needs it.
- Without a lockfile, `--frozen-lockfile` installs from `package.json` and writes none.
- `--frozen-lockfile`, `--production`, `--dry-run` and `--no-save` write no lockfile.
- A frozen install migrating another manager's lockfile (yarn, pnpm, npm) does so in memory only and asks you to run `bun install` and commit the result.
- If `package.json` was edited, run `bun install` locally first and commit the updated `bun.lock`, or the CI step fails.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/install.mdx and pm/lockfile.mdx: bun ci, --frozen-lockfile, no automatic CI freezing, missing-lockfile behaviour, flags that save no lockfile, in-memory migration with a note, commit bun.lock. Removed an unsourced lifecycle-script claim and a Verify line; narrowed the mismatch wording (edits that keep locked versions do not fail).

Method: documentation only; no commands were run.
