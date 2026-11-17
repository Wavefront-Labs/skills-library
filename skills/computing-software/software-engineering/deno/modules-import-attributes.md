---
id: computing-software.software-engineering.deno.modules-import-attributes
name: modules-import-attributes
category: computing-software
field: software-engineering
product: deno
tags: [modules, import-attributes, json-import, text-import, bytes-import, css-import, raw-imports]
level: practitioner
status: docs-checked
description: "Importing json, text, bytes and css modules with 'with { type }' attributes, which are stable versus experimental, and the CSSStyleSheet limits."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JSON:

```ts
import data from "./data.json" with { type: "json" };
```

`text` and `bytes` modules arrived in Deno 2.4. `text` is stable in Deno 2.8 and needs no flag:

```ts
import text from "./log.txt" with { type: "text" };
import bytes from "./image.png" with { type: "bytes" };
// text is a string; bytes instanceof Uint8Array
```

`bytes` is still experimental: enable with `--unstable-raw-imports` or the `unstable.raw-import` option in deno.json.

`css` is also experimental (same flag). It evaluates to a `CSSStyleSheet`, mainly for running unmodified browser module graphs (SSR, testing web components):

```ts
import sheet from "./styles.css" with { type: "css" };
sheet.replaceSync("body { color: red; }");
```

Dynamic form:

```ts
const { default: sheet } = await import("./styles.css", {
  with: { type: "css" },
});
```

Deno implements only a slice of `CSSStyleSheet`: `cssRules` is a frozen array recreated on each access, `CSSRule.cssText`, `replace`/`replaceSync` (top-level `@import` dropped). `insertRule` and `deleteRule` are not implemented, and the constructor's `options` argument is unsupported.

Static and statically analyzable dynamic imports need no permission; an unanalyzable specifier needs `--allow-read`.

## Checked

2026-11-04: confirmed against the Deno docs Modules page (Import attributes): json, text (stable 2.8) and bytes (2.4, experimental) imports, unstable.raw-import option, css imports and CSSStyleSheet limits, permission rules.

Method: documentation only; no commands were run.
