---
id: computing-software.web-development.bun.audit-vulnerabilities
name: audit-vulnerabilities
category: computing-software
field: web-development
product: bun
tags: [bun-audit, audit-fix, audit-level, ghsa-ignore]
level: practitioner
status: docs-checked
description: "Scan bun.lock for known vulnerabilities with bun audit, filter by level or dependency type, ignore advisories, and apply fixes with bun audit fix."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/audit.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`bun audit` reads `bun.lock` (no `node_modules` needed), queries the registry advisory endpoint, and never modifies project files.

```bash
bun audit --audit-level=high
bun audit --prod                  # -p: dependencies, optional, peer only
bun audit --omit=optional --omit=peer
bun audit --ignore GHSA-c2qf-rxjj-qqgw --ignore 1112918
bun audit --json
bun audit fix                     # also --latest, --dry-run, --json, --ignore-scripts
```

Gotchas:
- Exit code is 0 only when nothing remains after filtering; a registry error or non-advisory response exits 1.
- `--json` is unfiltered; `--audit-level` and `--ignore` affect only the exit code.
- CVE IDs do not match `--ignore`; use GHSA or numeric IDs.
- Filtering flags are CLI-only: put them in a `package.json` script to apply every run.
- `bun audit fix` changes only `bun.lock` and `node_modules` (exact pins are rewritten to `^version`). It rejects `--prod`, `--frozen-lockfile`, `--no-save`.
- Fixes blocked by a third party's range need `overrides`. Patched dependencies get upgraded, so redo `bun patch`.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/audit.mdx: bun.lock source, filter flags, --ignore ID types, --json being unfiltered, audit fix behaviour, rejected flags, exit codes.

Method: documentation only; no commands were run.
