---
id: computing-software.software-engineering.javascript.js-cross-origin-isolation
name: js-cross-origin-isolation
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, cross-origin-isolation, js-atomics]
level: advanced
status: docs-checked
description: "Opt into cross-origin isolation with COOP and COEP headers, prepare subresources with CORP or CORS, test with Report-Only and check crossOriginIsolated."
sources: ["https://web.dev/articles/coop-coep"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-origin isolation for SharedArrayBuffer

- Cross-origin isolation is an opt-in state that unlocks features with side-channel risk: `SharedArrayBuffer` (needed for WebAssembly threads), `performance.measureUserAgentSpecificMemory()` and higher-resolution `performance.now()` / `performance.timeOrigin` (the page says resolution can reach 5 microseconds or better, against 100 microseconds otherwise). It also makes `document.domain` immutable. The page notes Chrome desktop requires isolation for `SharedArrayBuffer` from Chrome 92.
- Send on the main document: `Cross-Origin-Embedder-Policy: require-corp` and `Cross-Origin-Opener-Policy: same-origin`. Windows opened from the document then live in a separate browsing context group and cannot interact directly with it.
- Subresources need an opt-in: set `Cross-Origin-Resource-Policy` (`same-origin`, `same-site`, or `cross-origin` for resources you control that are loaded cross-origin) or serve them with CORS and use the `crossorigin` attribute. Worker scripts must be same-origin, so they need neither. With `COEP: require-corp`, cross-origin subresources loaded without CORS (`script`, `link`, `video`, `iframe`, and so on) must send `Cross-Origin-Resource-Policy: cross-origin`.
- Dry run first: send `Cross-Origin-Embedder-Policy-Report-Only` on all documents (including iframes and worker scripts) to receive reports without blocking, then switch to `Cross-Origin-Embedder-Policy` with the same value once everything loads.
- COEP `credentialless` mode loads resources without a CORP header by stripping their credentials. The page says it is available from Chrome 96 and in Edge and not yet supported by other browsers (as of its 2022 update); check current support before relying on it.
- Embedded documents can be isolated with `allow="cross-origin-isolated"` on the iframe, but the whole chain of parent and child frames must be isolated too.
- Check `self.crossOriginIsolated === true`; it is true only when the page and all resources and windows are isolated in the same browsing context group.
- Debug in Chrome DevTools: blocked requests show `(blocked:NotSameOriginAfterDefaultedToSameOriginByCoep)` in the Network panel Status column; the Application panel Frames section shows iframe and dialog status. The Reporting API can send COEP and COOP reports.

Self-check: `self.crossOriginIsolated` is `true` in the page's console.

## Checked

Confirmed on the web.dev COOP/COEP article (last updated June 2022): feature list, headers, CORP/CORS rules, Report-Only workflow, credentialless note, iframe permission, `crossOriginIsolated` and debugging. Removed: `Cross-Origin-Opener-Policy`-induced OAuth popup breakage as a stated fact, "Node and Deno have no such restriction" and the local dev server note, none of which the page states. Browser-support statements are the page's own and may be out of date.

Method: docs-only read of cited pages, 2026-11-08
