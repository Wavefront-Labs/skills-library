---
id: computing-software.web-development.bun.html-dev-server
name: html-dev-server
category: computing-software
field: web-development
product: bun
tags: [html-dev-server, html-bundling, serve-static-plugins, tailwind-plugin]
level: practitioner
status: docs-checked
description: "Serve and build HTML entrypoints with Bun: dev server modes, console streaming, production build, serve.static plugins, Tailwind and env inlining."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/bundler/html-static.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun ./index.html                     # SPA: one file is the fallback for all paths
bun ./index.html ./about.html        # MPA: serves / and /about
bun './**/*.html'                    # globs work
bun ./index.html --console           # browser console output in terminal
bun build ./index.html --minify --outdir=dist --env='PUBLIC_*'
bun build --compile --target=browser ./index.html --outdir=dist   # single-file output
```
Shortcuts in the running server: `o+Enter` opens browser, `c+Enter` clears console, `q+Enter` or Ctrl+C quits. Route base is the longest common prefix of the files; `./about/index.html` maps to `/about`.

```toml
[serve.static]
plugins = ["bun-plugin-tailwind"]
env = "PUBLIC_*"        # or "inline" / "disable" (default)
```

Processed tags: `<script src>`, `<link rel="stylesheet">`, `<img>`, `<picture>`, `<video>`, `<audio>`, `<source>`, local `<link href>` (hashed and rewritten).

Tailwind: `bun install --dev bun-plugin-tailwind`, add to `bunfig.toml`, then use exactly one of `<link rel="stylesheet" href="tailwindcss" />`, `@import "tailwindcss";` or `import "tailwindcss";`.

Gotchas:
- Env inlining only replaces literal `process.env.FOO`, not `import.meta.env` or `const env = process.env`; an unset variable may throw `process is not defined` in the browser.
- Plugins work through `Bun.build` or bunfig, not the `bun build` CLI.
- Plugin API is a work in progress; headers and CORS are not configurable yet.

## Checked

2026-11-04. Confirmed against the Bun docs page bundler/html-static: SPA fallback for a single HTML file, MPA routes from multiple files, glob entries, longest-common-prefix path normalization, --console streaming over the HMR WebSocket, keyboard shortcuts o/c/q plus Ctrl+C, bun build with --minify/--outdir/--env, --compile --target=browser standalone output, serve.static plugins and env values (PUBLIC_*, inline, disable default), the Tailwind plugin install and the three alternative references, the list of processed tags, the literal process.env.FOO limitation, plugins not available in the bun build CLI, and the work-in-progress note about headers and CORS. Nothing removed.
Method: documentation only; no commands were run.
