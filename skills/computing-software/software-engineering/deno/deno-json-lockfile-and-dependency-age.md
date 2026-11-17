---
id: computing-software.software-engineering.deno.deno-json-lockfile-and-dependency-age
name: deno-json-lockfile-and-dependency-age
category: computing-software
field: software-engineering
product: deno
tags: [deno-json, lockfile, frozen, minimum-dependency-age, supply-chain, merge-conflicts]
level: advanced
status: docs-checked
description: "The deno.json lock field (path, frozen, disable), automatic deno.lock merge-conflict repair, and minimumDependencyAge to delay freshly published packages."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/deno_json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno uses a lockfile by default. Configure it with `lock`:

```json title="deno.json"
{
  "lock": {
    "path": "./deno.lock",
    "frozen": true
  }
}
```

`./deno.lock` is the default path. `frozen: true` errors if any dependency changes. Disable with `"lock": false`.

If `deno.lock` is left with git conflict markers after a merge, the next command that reads it merges the conflicting entries and rewrites a clean file; no manual edit is needed.

`minimumDependencyAge` stops installing npm or JSR versions published more recently than the age, since freshly published malicious versions are usually yanked within days:

```jsonc title="deno.json"
{
  // Don't install versions published less than 3 days ago
  "minimumDependencyAge": "P3D"
}
```

Accepts an ISO-8601 duration (`P3D`, `PT72H`), minutes (`120`), an absolute date (`2025-09-16`) or RFC3339 timestamp, or `0` to disable. Since Deno 2.9 a 24-hour minimum applies even when unset.

Exempt packages with the object form:

```jsonc
{
  "minimumDependencyAge": {
    "age": "P3D",
    "exclude": ["npm:@mycompany/cli", "jsr:@mycompany/lib"]
  }
}
```

Also available as the `--minimum-dependency-age` flag and `min-release-age` in `.npmrc`.

## Checked

2026-11-04. Confirmed against the Deno configuration file (deno.json) reference: `lock` path and frozen, `"lock": false`, merge-conflict repair, `minimumDependencyAge` forms, the 24-hour default since Deno 2.9, object form with exclude, flag and `.npmrc` equivalents. Nothing removed.

Method: documentation only; no commands were run.
