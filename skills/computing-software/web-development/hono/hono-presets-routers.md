---
id: computing-software.web-development.hono.hono-presets-routers
name: hono-presets-routers
category: computing-software
field: web-development
product: hono
tags: [hono, concepts, routers, performance, presets]
level: advanced
status: docs-checked
description: "Choose the right Hono preset and router: hono, hono/quick, hono/tiny, RegExpRouter, TrieRouter, SmartRouter, LinearRouter and PatternRouter."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/presets.md
  - https://github.com/honojs/website/blob/main/docs/concepts/routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Presets and routers

The `Hono` class from every preset is the same; only the router differs, so they are interchangeable.

| Import | Router | Use for |
| --- | --- | --- |
| `hono` | `SmartRouter({ routers: [new RegExpRouter(), new TrieRouter()] })` | Recommended default. Long-lived servers (Deno, Bun, Node.js), Fastly Compute, and isolate platforms like Cloudflare Workers and Deno Deploy |
| `hono/quick` | `SmartRouter({ routers: [new LinearRouter(), new TrieRouter()] })` | Apps initialized on every request |
| `hono/tiny` | `PatternRouter` | Resource-limited environments, smallest bundle |

```ts
import { Hono } from 'hono/quick'
```

## The five routers
- **RegExpRouter**: compiles all routes into one large regular expression and matches once; fastest, but does not support all patterns, so it is paired with another router.
- **TrieRouter**: Trie-tree; supports all patterns; slower than RegExpRouter but much faster than Express.
- **SmartRouter**: picks the best of the registered routers at startup and keeps using it.
- **LinearRouter**: very fast route registration (no string compilation); for one-shot environments.
- **PatternRouter**: smallest. An app with only PatternRouter is under 15KB (docs show Total Upload 14.68 KiB / gzip 5.38 KiB).

You can also specify the router you want in the constructor of `Hono`.

## Gotcha
RegExpRouter registration is slightly slow, so it is wrong for per-request initialization; use `hono/quick` there. Default `hono` is highly recommended for most cases.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page api/presets.md and concepts/routers.md. Removed: the invented Verify step (getRouterName from hono/dev) and the RegExpRouter import path, neither on the cited pages.
Method: documentation only; no commands were run.
