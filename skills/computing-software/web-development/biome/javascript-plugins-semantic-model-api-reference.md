---
id: computing-software.web-development.biome.javascript-plugins-semantic-model-api-reference
name: javascript-plugins-semantic-model-api-reference
category: computing-software
field: web-development
product: biome
tags: [biome, semantic-model, binding, scope, reference, global-reference, unresolved-reference, declaration-kind, export-ranges, javascript-plugin-api]
level: sme
status: docs-checked
description: "Reference for the plugin SemanticModel, Binding, Reference, Scope and global/unresolved reference methods, including edge-case semantics."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available through `ctx.model` in `semantic` queries.

**SemanticModel**
- `binding(reference)`: binding an identifier use refers to, respecting shadowing; `undefined` for configured globals and unresolved references. `asBinding(node)` looks up the binding introduced by a declaration identifier.
- `allBindings()`: every tracked binding including nested scopes (same-name declarations can be separate bindings). `allExportedBindings()`: each exported binding once, order unspecified, re-exports without a local binding excluded. `hasExports()` is true only if an exported binding is tracked (empty exports or exported literals can leave it false).
- `scopes()`, `globalScope()` (outermost, no parent, exists for empty files), `scope(node)` (most specific scope for the trimmed range, `undefined` for an empty node), `scopeHoistedTo(node)`.
- `allGlobalReferences()`, `allUnresolvedReferences()`, `isGlobalReference(ref)`, `isUnresolvedReference(ref)` (a reference to a later declaration can still resolve), `isImported(node)`, `isExported(node)`.

**Binding:** `syntax()` (identifier node), `declarationKind()` (one of class, enum, function, generic, hoistedValue, import, importType, interface, module, namespace, type, unknown, using, value), `exports()` (a specifier yields the local identifier, not the alias), `exportRanges()` (UTF-8 byte offsets, start inclusive, end exclusive), `scope()`, `allReferences()`, `allReads()`, `allWrites()`, `isImported()`, `isExported()`.

**Reference:** `syntax()`, `binding()`, `scope()`, `isRead()`, `isWrite()`.

**Scope:** `syntax()`, `isGlobalScope()`, `parent()`, `children()` (immediate only), `ancestors()` (self then outward to global), `bindings()` (declared or hoisted here only), `getBinding(name)` (this scope only; Unicode escapes decoded; when a TS name has both type and value bindings the value is preferred).

**GlobalReference** and **UnresolvedReference** expose `syntax()`; the global one also has `isRead()` and `isWrite()`.

## Checked

Method: 2026-11-08 compared against the Biome website source mdx for linter plugins (Run APIs, SemanticModel, Binding, Reference, Scope sections). Every method and edge-case note matches the page; no changes to the technical content. Dropped an invented "Verify" step. Note that `hasExports` and `allExportedBindings` notes are the page's own wording and describe the model, not export syntax.
