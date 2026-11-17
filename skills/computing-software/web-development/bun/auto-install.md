---
id: computing-software.web-development.bun.auto-install
name: auto-install
category: computing-software
field: web-development
product: bun
tags: [auto-install, prefer-offline, import-version-specifier, no-node-modules]
level: advanced
status: docs-checked
description: "Run scripts without node_modules using Bun auto-install: version resolution order, inline version specifiers, cache behaviour and blocking, timeouts and limits."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/auto-install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When no `node_modules` exists, Bun installs imported packages on first use into the global cache.

Version resolution:
1. Search up the tree for a `package.json` listing the package (any dependency group) and use that range.
2. Otherwise use `latest`.
3. If `bun.lock` in the project root satisfies the range, use it.

An inline specifier bypasses this:

```ts
import { z } from "zod@3.0.0";   // exact
import { z } from "zod@next";    // tag
import { z } from "zod@^3.20.0"; // range
```

Cache: packages go to `<cache>/<pkg>@<version>`; `latest` reuses a copy cached within 24 hours. `bun --prefer-offline` (or `install.prefer = "offline"`) resolves from cached metadata of any age. A read-only cache still serves cached packages.

Gotchas:
- The first import of an uncached package blocks the thread, so timers do not run during `require()` or `import()`.
- An import fails if the registry is silent for about 30 s (`BUN_CONFIG_HTTP_IDLE_TIMEOUT`); a 404 is not re-requested for 5 minutes.
- The first auto-installed import sets the project for the whole process.
- Unsupported: git dependencies, patch-package, IDE IntelliSense for auto-installed types.
- `-i`/`--install` does not re-enable it if a security scanner is configured or `bunfig.toml`/`package.json` cannot be read.

## Checked

2026-11-04. Confirmed against bun docs runtime/auto-install.mdx: no-node_modules trigger, version resolution order, inline version specifiers, cache layout and 24-hour latest reuse, --prefer-offline and install.prefer, thread blocking, 30 second idle timeout and BUN_CONFIG_HTTP_IDLE_TIMEOUT, 404 five-minute rule, read-only cache, one project per process, limitations, scanner and unreadable-config disabling with -i ignored.

Method: documentation only; no commands were run.
