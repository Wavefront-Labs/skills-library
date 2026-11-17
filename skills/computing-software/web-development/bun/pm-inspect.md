---
id: computing-software.web-development.bun.pm-inspect
name: pm-inspect
category: computing-software
field: web-development
product: bun
tags: [bun-pm-ls, bun-pm-licenses, bun-pm-diff, pm-diff-versions]
level: practitioner
status: docs-checked
description: "Inspect installed dependencies with bun pm ls, licenses and diff: list versions, group by license, and compare package versions for risky changes."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/pm.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List:

```bash
bun pm ls               # direct deps (default); --all for nested
bun pm ls --trusted     # packages allowed to run lifecycle scripts
bun pm ls --omit=dev    # or --production
bun pm ls react         # every installed version; exit 1 if none
bun pm ls -g
```

`--depth=0` is the only depth accepted.

Licenses (needs both `bun.lock` and `node_modules`; packages missing from `node_modules` are skipped with a warning):

```bash
bun pm licenses --long --prod
bun pm licenses --json --filter 'pkg-*'
```
Packages without a license field appear under `Unknown`; dev-only ones are marked `(dev)`.

Diff two versions (registry spec, folder or `.tgz`):

```bash
bun pm diff react                       # lockfile version vs latest
bun pm diff react@18.2.0 19.0.0
bun pm diff --stat --name-only
```
Flags: `--raw`, `--minify`, `--unminify`, `-w`, `-U <n>`, `--diff <spec>`, `--json`. Piped output or `NO_COLOR` gives a plain patch usable with `git apply`. The summary flags new install scripts, dependency changes and new `child_process`/`fs`/`net` imports.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/pm.mdx: bun pm ls forms and exit code, --depth=0 only, licenses requirements and flags, Unknown and (dev) markers, bun pm diff forms, flags, plain-patch output and summary callouts.

Method: documentation only; no commands were run.
