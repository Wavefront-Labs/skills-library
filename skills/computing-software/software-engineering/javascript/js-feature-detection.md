---
id: computing-software.software-engineering.javascript.js-feature-detection
name: js-feature-detection
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, feature-detection, js-compat]
level: practitioner
status: docs-checked
description: "Detect features rather than browsers: in checks, CSS.supports, @supports, element probes and matchMedia, with graceful fallbacks."
sources: ["https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Feature_detection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature detection and progressive enhancement

- Feature detection runs a test for support and then conditionally runs code, so the browser gets a working experience instead of failing. Do not confuse it with browser sniffing (UA sniffing), which MDN calls a terrible practice to discourage at all costs.
- JavaScript patterns from MDN: check a member of an object (`"geolocation" in navigator`); create an element in memory with `document.createElement()` and check a property (`!!document.createElement("canvas").getContext`, where `!!` forces a real boolean); check a specific return value of a method on an element; set a property on an element and check whether the value is retained.
- CSS from JavaScript: `CSS.supports("grid-template-columns", "subgrid")`, or test the existence of `element.style.property` (for example `paragraph.style.rotate`).
- CSS-native: the `@supports` at-rule, with `and`, `or` and `not`. A condition with a value needs a complete declaration in parentheses and no trailing semicolon, for example `@supports (grid-template-columns: subgrid) { ... }` and `@supports not (grid-template-columns: subgrid) { ... }`. MDN calls it the preferred method for CSS features: no JavaScript and one stylesheet.
- `window.matchMedia("(width <= 480px)").matches` runs media-query tests in JavaScript.
- Some features are known to be undetectable; use a different approach such as a polyfill.
- Always write the fallback branch (for example a static map when geolocation is missing).

Self-check: disable the feature in DevTools or stub it out and confirm the fallback branch runs.

## Checked

2026-11-08. Confirmed on the MDN Implementing feature detection article: the concept, UA sniffing warning, the four JavaScript patterns, `CSS.supports()`, `@supports` syntax rules and preference, `matchMedia`, and undetectable features. Removed `IntersectionObserver`, `structuredClone` and `HTMLScriptElement.supports("importmap")` as example probes, the `navigator.userAgentData` advice, the `nomodule` bundling advice, conditional polyfill loading via dynamic import, and the Baseline tracking note, none of which the article covers.

Method: docs-only read of cited pages, 2026-11-08
