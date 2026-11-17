---
id: computing-software.web-development.bun.overrides-resolutions
name: overrides-resolutions
category: computing-software
field: web-development
product: bun
tags: [overrides, resolutions, transitive-dependency, version-pin]
level: advanced
status: docs-checked
description: "Pin or replace transitive dependencies with overrides or resolutions: scoped-to-parent forms, version selectors, catalog and npm alias values, and their limits."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/overrides.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Only the root `package.json` is read. If both `overrides` and `resolutions` exist, Bun uses `overrides`.

```json
"overrides": {
  "bar": "~4.4.0",
  "quux": "npm:@myorg/quux@^1.0.0",
  "foo": "catalog:",
  "bar": "$foo",
  "micromatch": { ".": "^4.0.5", "picomatch": "^2.3.2" },
  "micromatch>picomatch": "^2.3.2",
  "semver@<7.5.2": "7.5.2"
}
```
(Yarn path form: `"resolutions": { "micromatch/picomatch": "^2.3.2" }`.)

Rules:
- Any dependency specifier is a valid value; `$foo` reuses your declared range.
- Precedence: parent-with-version, then parent, then top-level. `"."` inside an object overrides the package itself.
- Version selectors match the range each dependent declares, not the resolved version: `semver@<7.5.2` matches `^7.3.0` but not `^7.5.2`.

Gotchas:
- Only one parent level works; `a>b>c` or `a/b/c` is ignored with a warning. pnpm `"pkg@"` and `"-"` forms are unsupported.
- `bun install` re-resolves lockfile entries that violate an override; `--frozen-lockfile` installs the lockfile version.
- Nested or version-scoped rules write `lockfileVersion` 3, unreadable by older Bun.

## Checked

2026-11-04. Confirmed against bun docs pm/overrides.mdx: root-only reading, overrides over resolutions, value forms (npm:, catalog:, $name), nested and version-scoped forms, precedence, declared-range matching, one-parent-level limit, unsupported pnpm forms, lockfile re-resolution and frozen behaviour, lockfileVersion 3 note.

Method: documentation only; no commands were run.
