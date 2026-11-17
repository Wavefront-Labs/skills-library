---
id: computing-software.web-development.bun.bunx-run-binaries
name: bunx-run-binaries
category: computing-software
field: web-development
product: bun
tags: [bunx, package-executable, bun-flag-placement, npx-alternative]
level: intro
status: docs-checked
description: "Run package binaries with bunx: version pinning, --bun versus shebang, --package for differently named binaries, and update-check and failure behaviour."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/bunx.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bunx cowsay "Hello world!"
bunx my-cli@2                      # version specifier skips the local package
bunx --bun my-cli                  # run under Bun's runtime, not the shebang's node
bunx my-cli --foo bar              # args go to the executable
bunx -p renovate renovate-config-validator
bunx --package @angular/cli ng
bunx -p typescript sh -c "tsc --version"
```

Resolution: a locally installed package is used first, then bunx auto-installs from npm into Bun's global cache.

Gotchas:
- Flag placement: `bunx --bun my-cli` works; `bunx my-cli --bun` passes `--bun` to the executable.
- Bun respects shebangs: a `#!/usr/bin/env node` script runs under node. Use `#!/usr/bin/env bun` or `--bun` to force Bun.
- On macOS/Linux, a missing or non-executable local binary is an error naming the file; bunx does not re-download.
- `bunx my-cli` checks the registry for newer versions once a day; `@latest` checks every run. If the registry is unreachable or returns 5xx, 429 or 408, it warns and runs the version it has.

## Checked

2026-11-04. Confirmed against bun docs pm/bunx.mdx: bunx alias, local-first resolution and version specifier skipping the local package, global cache, missing or non-executable binary error on macOS and Linux, daily update check with 5xx/429/408 fallback and @latest every run, argument placement, shebang handling and --bun placement, -p/--package examples.

Method: documentation only; no commands were run.
