---
id: computing-software.software-engineering.deno.packages-version-ranges
name: packages-version-ranges
category: computing-software
field: software-engineering
product: deno
tags: [packages, semver, version-ranges, caret, tilde, specifiers]
level: intro
status: docs-checked
description: "Specify package versions with @ and semver ranges (exact, caret, tilde, comparators, x-ranges) for jsr: and npm: dependencies."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Append `@` and a semver range to a package specifier:

```bash
@scopename/mypackage           # highest version
@scopename/mypackage@16.1.0    # exact version
@scopename/mypackage@16        # highest 16.x version >= 16.0.0
@scopename/mypackage@^16.1.0   # highest 16.x version >= 16.1.0
@scopename/mypackage@~16.1.0   # highest 16.1.x version >= 16.1.0
```

| Symbol | Meaning |
| --- | --- |
| `1.2.3` | Exact version only |
| `^1.2.3` | Allows changes not touching the leftmost non-zero digit (`1.2.4`, `1.3.0` yes; `2.0.0` no) |
| `~1.2.3` | Patch updates only (`1.2.4` yes; `1.3.0` no) |
| `>=1.2.3`, `<=1.2.3`, `>1.2.3`, `<1.2.3` | Comparators |
| `1.2.x` | Any patch within minor 1.2 |
| `1.x` | Any minor and patch within major 1 |
| `*` | Any version |

To share one range across multiple workspace members, use `catalog:` (see the workspaces page).

## Checked

2026-11-04. Confirmed against the Deno Dependency management page: the five specifier examples and the symbol table, and the `catalog:` pointer. Nothing removed.

Method: documentation only; no commands were run.
