---
id: computing-software.web-development.bun.lifecycle-scripts-trust
name: lifecycle-scripts-trust
category: computing-software
field: web-development
product: bun
tags: [trusted-dependencies, ignore-scripts, postinstall, lifecycle-scripts]
level: practitioner
status: docs-checked
description: "Control which dependency lifecycle scripts run: trustedDependencies semantics, bun pm untrusted and trust, disabling scripts, and Docker or frozen-install caveats."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/lifecycle.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/pm.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bun runs dependency scripts only for allow-listed packages.

```json
{ "trustedDependencies": ["node-sass"] }
```

| package.json | Scripts allowed |
|---|---|
| field omitted | Bun's built-in default list (npm sources only) |
| explicit array | only the listed packages |
| `[]` | none |

```bash
bun pm untrusted              # blocked scripts
bun pm trust --all --dry-run  # shows what would run
bun pm default-trusted
bun install --ignore-scripts  # or ignoreScripts = true under [install], or .npmrc ignore-scripts=true
```

Gotchas:
- An explicit `trustedDependencies` replaces the default list; re-list packages such as `sharp` or `esbuild`.
- `file:`, `link:`, `git:` and `github:` dependencies must be listed explicitly, even if the name matches a default.
- Use the real package name, not an npm alias.
- `--frozen-lockfile` and `bun ci` run scripts only for packages they install; in a checkout without the declaring workspace (a Docker layer) the default list is ignored and only lockfile-recorded packages run.
- `NPM_CONFIG_IGNORE_SCRIPTS` is a one-way switch (`false`/`0` do not override a config file) and is not read from `.env`.

## Checked

2026-11-04. Confirmed against bun docs pm/lifecycle.mdx and pm/cli/pm.mdx: trustedDependencies modes table, default-list replacement, non-npm sources needing explicit listing, alias names, frozen-install and Docker behaviour, --ignore-scripts, bunfig and .npmrc forms, NPM_CONFIG_IGNORE_SCRIPTS semantics, bun pm untrusted, trust --all --dry-run and default-trusted.

Method: documentation only; no commands were run.
