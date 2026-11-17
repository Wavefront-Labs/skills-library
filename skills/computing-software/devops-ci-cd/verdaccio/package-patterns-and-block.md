---
id: computing-software.devops-ci-cd.verdaccio.package-patterns-and-block
name: package-patterns-and-block
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [packages, glob-patterns, pattern-order, minimatch, package-order, block-packages, double-wildcard]
level: practitioner
status: docs-checked
description: "Write the packages section: glob patterns are matched top to bottom, how to block names by leaving access empty, and why to keep a ** entry last."
sources:
  - https://verdaccio.org/docs/packages/
  - https://verdaccio.org/docs/protect-your-dependencies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Patterns use minimatch globs and are matched top to bottom; the first match wins.

```yaml
packages:
  'old-*':                # no access or publish: blocked
  '@scope/*':
    access: $all
    publish: $authenticated
    proxy: server2
  '**':
    access: $all
    publish: $authenticated
    proxy: npmjs
```
Properties: `access`, `publish`, `unpublish`, `stage` (7.x), `proxy`, `storage` (subfolder inside storage per matching package). `allow_access`, `allow_publish` and `proxy_access` are deprecated; use `access`, `publish`, `proxy`.

Rules:
- An empty or missing list matches nobody. `unpublish` and `stage` fall back to `publish`.
- Always include the double wildcard `'**'`; if you omit it Verdaccio adds one and resolution may change.
- Several groups per field are space separated.
- If the whole `packages` section is missing, nobody can access anything.

A name matching a pattern with no `access` and `publish` is blocked.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Package Access and Protecting packages. Confirmed: minimatch-style patterns matched top to bottom with the first match winning, blocking by leaving access empty, the property list, the deprecated allow_access, allow_publish and proxy_access, the fallbacks, the double wildcard and the missing packages section. Removed or corrected: the verify line about reading HTTP status in the log.

Method: documentation only; no commands were run.
