---
id: computing-software.web-development.web-performance.async-defer-and-module-scripts
name: async-defer-and-module-scripts
category: computing-software
field: web-development
product: web-performance
tags: [critical-rendering-path, resource-hints, async-defer-scripts, render-blocking-scripts, defer, async, script-type-module, script-loading-order]
level: practitioner
status: verified
description: "Loading scripts without blocking the parser: classic vs defer vs async vs module, execution order, third-party tags, and where to place each script."
sources:
  - https://html.spec.whatwg.org/multipage/scripting.html#attr-script-async
  - https://web.dev/learn/performance/optimize-resource-loading
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# async, defer and module script loading

**Goal:** scripts never block HTML parsing or first paint unless they genuinely must run first.

## 1. The four behaviours
| Markup | Download | Executes | Order kept? |
|---|---|---|---|
| `<script src>` (in head) | Blocks parser | Immediately | Yes |
| `<script defer src>` | In parallel | After parsing, before `DOMContentLoaded` | Yes, document order |
| `<script async src>` | In parallel | As soon as downloaded (pauses parser) | No |
| `<script type="module" src>` | In parallel (+ its imports) | Deferred by default | Yes |
| `<script type="module" async src>` | In parallel | As soon as graph ready | No |

## 2. Choosing
- **App bundles**: `defer` (or `type="module"`), in `<head>` so download starts early.
- **Independent third parties** (analytics, ads): `async` - order doesn't matter and they shouldn't wait for parsing. Even better: load after `load` or on interaction for non-essential tags.
- **Inline scripts** that must run before paint (theme class to avoid dark-mode flash, feature flags): small, inline, in head, synchronous.
- **Polyfills** needed by deferred code: also `defer`, placed before them.
`defer`/`async` are ignored on inline scripts (except module inline scripts, which are deferred).

## 3. Common mistakes
- Bundles at end of `<body>` without `defer` - download starts late (parser discovers them late).
- `async` on scripts that depend on each other (jQuery + plugin) - random breakage.
- `document.write` in any async/deferred script - ignored/blocked.
- Injected scripts (`document.createElement('script')`) are async by default and invisible to the preload scanner - add `<link rel="preload" as="script">` if they're critical.

## 4. Priorities
Run in Chromium (CDP `initialPriority`): `async` and `defer` scripts in `<head>` both start at Low, a parser-blocking script and a module script start at High. `fetchpriority="high"` raised an async and a defer script to High. `fetchpriority="low"` on a plain blocking script did not lower it (still High), so do not rely on it there.

Run in Chromium (execution order, slow `a.js` listed before fast `b.js`): sync `a, b, inline, DCL`; defer `inline, a, b, DCL`; async `inline, DCL, b, a`; module scripts `inline, m, n, inline-module, DCL`; `type=module async` behaves like async (`b, a`); `defer` on an inline script is ignored (it ran in document order); a script created with `createElement('script')` reports `async === true` and ran in download order.

## Verify
- [ ] Lighthouse: no render-blocking scripts (except intended tiny inline ones).
- [ ] Network waterfall: bundles start downloading in the first round-trip.
- [ ] Functionality works with scripts loading in any timing (throttle and reload many times).
