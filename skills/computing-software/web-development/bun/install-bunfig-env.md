---
id: computing-software.web-development.bun.install-bunfig-env
name: install-bunfig-env
category: computing-software
field: web-development
product: bun
tags: [bunfig-install, bun-config-registry, install-env-vars, http-retry]
level: practitioner
status: docs-checked
description: "Configure bun install through bunfig.toml [install] keys and BUN_CONFIG environment variables: registry, token, retries, linker, lockfile and cache."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
bunfig.toml `[install]` keys (the page lists `optional`, `dev`, `peer`, `production`, `saveTextLockfile`, `frozenLockfile`, `dryRun` and `concurrentScripts` at the values shown; `prefer`, `offline` and `disableManifest` below are non-default examples):

```toml
[install]
optional = true      # also dev, peer (all true)
production = false
dryRun = false
frozenLockfile = false
saveTextLockfile = true
concurrentScripts = 16   # (cpu count or GOMAXPROCS) x2
linker = "hoisted"   # or "isolated"; the default depends on lockfile configVersion and workspaces
prefer = "offline"
offline = true

[install.cache]
disableManifest = true
```

Project `bunfig.toml` overrides the global file.

Environment variables (these override `bunfig.toml`):
- `BUN_CONFIG_REGISTRY` registry URL; `BUN_CONFIG_TOKEN` auth token.
- `BUN_CONFIG_YARN_LOCKFILE` also writes a Yarn v1 lockfile.
- `BUN_CONFIG_SKIP_SAVE_LOCKFILE`, `BUN_CONFIG_SKIP_LOAD_LOCKFILE`, `BUN_CONFIG_SKIP_INSTALL_PACKAGES`.
- `BUN_CONFIG_HTTP_RETRY_COUNT` (default 5) and `BUN_CONFIG_HTTP_RETRY_BACKOFF` (default 50 ms; `0` retries immediately).
- `BUN_FEATURE_FLAG_DISABLE_NATIVE_DEPENDENCY_LINKER=1` and `BUN_FEATURE_FLAG_DISABLE_IGNORE_SCRIPTS=1` disable postinstall optimizations.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/install.mdx: [install] keys and documented defaults, project-over-global override, BUN_CONFIG_* variables (priority over bunfig.toml), retry defaults, the two BUN_FEATURE_FLAG variables. Fixed the misleading defaults label (prefer, offline and disableManifest are not defaults) and removed an unsourced Verify line.

Method: documentation only; no commands were run.
