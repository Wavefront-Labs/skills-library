---
id: computing-software.web-development.bun.outdated-report
name: outdated-report
category: computing-software
field: web-development
product: bun
tags: [bun-outdated, outdated-table, outdated-patterns]
level: intro
status: docs-checked
description: "Read the bun outdated table (Current, Update, Latest), filter by glob patterns and workspaces, and include catalog dependencies with -r."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/outdated.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Columns: Current (installed), Update (latest version satisfying your range), Latest (the registry `latest` tag).

```bash
bun outdated
bun outdated eslint-plugin-security
bun outdated 'eslint*'
bun outdated '@types/*'
bun outdated '!@types/*'
bun outdated typescript 'eslint*' '!eslint-plugin-sonarjs'
bun outdated --filter='@monorepo/{types,cli}'
bun outdated -r        # include catalog dependencies, adds a Workspace column
```

Gotchas:
- Multiple positive patterns combine as OR; `!` patterns subtract.
- If Update equals Current but Latest is higher, the newer release is outside your `package.json` range.
- A prerelease ahead of `latest` can appear when `bun update` would change it.
- An aliased dependency such as `"lodash3": "npm:lodash@^3.0.0"` shows as `lodash3@npm:lodash` and matches by either name.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/outdated.mdx: column meanings, pattern and ! negation examples, OR semantics, --filter globs, -r catalog table with Workspace column, aliased dependency display, prerelease note. Removed an unsourced quoting gotcha and the --latest hint.

Method: documentation only; no commands were run.
