---
id: computing-software.software-engineering.javascript.js-dynamic-import
name: js-dynamic-import
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, dynamic-import, js-modules]
level: practitioner
status: docs-checked
description: "Load modules on demand with import(): promise result, namespace object, error behaviour, caching, import attributes and context limits."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/import"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic import

- `import(moduleName)` or `import(moduleName, options)` loads an ES module asynchronously, also from non-module scripts. `import` is a keyword, not a function: `const myImport = import` is a `SyntaxError`. It never throws synchronously.
- It returns a promise that fulfils with the module namespace object (all exports; the default export is the key `default`, so destructuring must rename it: `const { default: myDefault, foo } = await import("/modules/my-module.js")`). It rejects if coercing the specifier throws, if loading fails (browsers use `TypeError`, Node a generic `Error`), or if evaluating the module throws.
- Reasons to use it: the cost of static import is high and the code is rarely needed, the module does not exist at load time, the specifier is built dynamically, side effects should only run conditionally, or you are in a non-module environment. MDN says to use it only when necessary: static imports are better for initial dependencies because of static analysis and tree shaking.
- The namespace object is sealed with a null prototype; each normalised specifier maps to one namespace object, so modules are evaluated only once and later imports cause no extra HTTP request or disk access. Only evaluation failures are cached; load or link failures may be retried. A unique query string forces re-evaluation but can leak memory because namespace objects cannot be garbage-collected.
- Do not export a function named `then()` from a module: it would be called during promise resolution and make dynamic import behave differently from static import.
- Import attributes go in the second argument: `await import("./data.json", { with: { type: "json" } })`. Trailing commas in the call are allowed only where the runtime supports the options argument; check browser compatibility.
- `import()` works in the main thread, shared workers and dedicated workers, but throws in a service worker or a worklet.
- Static `import` in an HTML script needs `type="module"`; `import()` is always available.

Self-check: a conditional `await import("./x.js")` does not run the module until that branch executes.

## Checked

Confirmed on the MDN import() page: syntax, return and rejection rules, use cases, caching and `then()` warning, import attributes, context restrictions. Removed: bundler chunk naming (`webpackChunkName`), top-level `await` blocking importers, `import.meta.url`, circular-import `ReferenceError` and the network-panel self-check, none of which the page states. Whether a given runtime supports import attributes is left to the page's compatibility table, which was not readable as text.

Method: docs-only read of cited pages, 2026-11-08
