---
id: computing-software.web-development.bun.watch-and-hot
name: watch-and-hot
category: computing-software
field: web-development
product: bun
tags: [bun-watch, bun-hot, hot-reload, watch-mode]
level: intro
status: docs-checked
description: "Choose between bun --watch (hard restart) and --hot (soft reload keeping state), with check, kill-signal and no-clear-screen options and their limits."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/watch-mode.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun --watch index.tsx                      # hard restart on imported-file changes
bun run --watch watchy.tsx
bun --watch test
bun --watch --check index.tsx              # type-check before each restart
bun --watch --watch-kill-signal SIGINT index.ts
bun build --watch --no-clear-screen
bun --hot server.ts                        # soft reload, process stays alive
```

`--watch` restarts with the same arguments and environment. `--hot` keeps global state such as `globalThis`:

```ts
globalThis.count ??= 0;
console.log(`Reloaded ${globalThis.count++} times`);
setInterval(function () {}, 1000000); // keeps `bun run` alive
```

Gotchas:
- With `--check`, a type error stops the run; Bun waits for your next change.
- Kill-signal handlers you register run before each `--watch` restart (default SIGTERM).
- `--hot` is server-side only, not browser HMR; it skips `node_modules` and re-transpiles all code each reload.
- HTTP servers can pick up handler changes under `--hot` without dropping the server.
- `import.meta.hot` is planned, not available.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/watch-mode: --watch hard restart versus --hot soft reload, bun --watch test, --check, --watch-kill-signal (default SIGTERM), --no-clear-screen, globalThis persistence, node_modules exclusion, re-transpile on reload, HTTP server handler reload, import.meta.hot planned. Nothing removed.
Method: documentation only; no commands were run.
