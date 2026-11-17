---
id: computing-software.web-development.biome.javascript-plugins-definerule-and-queries
name: javascript-plugins-definerule-and-queries
category: computing-software
field: web-development
product: biome
tags: [biome, javascript-plugin, definerule, ast-query, semantic-query, registerdiagnostic, biome-runtime, biome-inspect-file, cst-node-names]
level: advanced
status: docs-checked
description: "Author a JavaScript or TypeScript plugin with defineRule, ast and semantic queries, node kind names, registerDiagnostic and the RuleContext."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JavaScript plugins (Developer Preview) are `.js` or `.ts` files. For TypeScript, install `@biomejs/runtime` for types. A plugin exports an object built with `defineRule`, which needs:
- `query`: which CST nodes to inspect.
- `run(node, ctx)`: the logic; on a violation call `registerDiagnostic(node, severity, message)`.

```ts
import { defineRule, ast, registerDiagnostic } from "@biomejs/runtime/plugin"

export const noAssign = defineRule({
    query: ast("JS_CALL_EXPRESSION"),
    run(node, ctx) {
      registerDiagnostic(node, "error", "Can't assign anything.")
    }
})
```

**Finding node names.** Nodes use grammar names in all caps, such as `JS_DEBUGGER_STATEMENT`. Discover them with `biome inspect file` or the playground. You can also import the interface (`JsDebuggerStatement`) and use `ast(JsDebuggerStatement.kind)`.

**Queries.** `ast(...)` takes one name or a list. `semantic(...)` takes names too and additionally exposes the file's semantic model on `ctx.model`.

**`ctx` (RuleContext).**
- `ctx.filePath`: absolute path of the linted file.
- `ctx.sourceType`: how it was parsed (JS or TS, module or script, embedded in Astro, Vue or Svelte).
- `ctx.model`: the `SemanticModel` of bindings and references.

Breaking changes may land in patch releases while JavaScript plugins are in Developer Preview.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the unsupported claim that JavaScript plugin files are registered like Grit plugins and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
