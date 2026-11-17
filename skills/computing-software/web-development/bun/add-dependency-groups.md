---
id: computing-software.web-development.bun.add-dependency-groups
name: add-dependency-groups
category: computing-software
field: web-development
product: bun
tags: [bun-add, dev-dependency, peer-dependency, exact-version, save-prod]
level: intro
status: docs-checked
description: "Add packages with bun add into dependencies, devDependencies, optionalDependencies or peerDependencies, pin exact versions, and move packages between groups."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/add.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun add preact                  # dependencies
bun add zod@3.20.0              # also @^3.0.0, @latest
bun add --dev @types/react      # -d, -D, --development
bun add --optional lodash
bun add --peer @types/bun       # peers are installed by default
bun add --save-prod zod         # move from dev/optional to dependencies
bun add react --exact           # -E: write 18.2.0 instead of ^18.2.0
```

Rules:
- With no group flag, an existing entry is updated in place. If it is listed in two groups, both are updated unless the install skips a group (for example `--omit=dev`).
- A group flag moves the entry. A `peerDependencies` entry stays put, and `--peer` keeps an existing `devDependencies` entry.
- `bun add --help` lists every option.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/add.mdx: group flags and aliases, --save-prod, --exact, in-place update and move rules, peer default install. Removed an unsourced Verify line.

Method: documentation only; no commands were run.
