---
id: computing-software.software-engineering.deno.test-doc-tests
name: test-doc-tests
category: computing-software
field: software-engineering
product: deno
tags: [test, doc-tests, jsdoc, markdown, ignore-attribute, hashbang]
level: advanced
status: docs-checked
description: "Run JSDoc and markdown code examples with deno test --doc: language identifiers, auto-imported exports, hashbang permissions and skipping blocks."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/doc_tests.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`deno test --doc example.ts` extracts code blocks from JSDoc (and markdown) and runs each as a pseudo test in a module beside the documented one.

Block language identifiers: `js`, `javascript`, `mjs`, `cjs`, `jsx`, `ts`, `typescript`, `mts`, `cts`, `tsx`. With none, the language is inferred from the source document's media type.

Items exported from the documented module are automatically imported by name, including the default export, so examples can call `add(ONE, getTwo())` without import lines.

A hashbang in an example is validated against supported Deno flags and permission flags forward to the generated `Deno.test`:

```ts
/**
 * ```ts
 * #!/usr/bin/env -S deno run --allow-env=MY_ENV_VAR
 * console.log(Deno.env.get("MY_ENV_VAR"));
 * ```
 */
```

| Flag | Generated permissions |
| --- | --- |
| `--allow-all` | Inherits all from `deno test` |
| `--allow-*` | Inherits that permission |
| `--allow-*=...` | Restricts to provided values |
| `--deny-*` | Explicitly revokes |
| `--deny-*=...` | Unsupported (test failure) |
| `--permission-set`, `--ignore-*` | Unsupported (ignored) |
| none | None |

An example never runs with broader permissions than `deno test` was granted.

Skip a block with the `ignore` attribute: ```` ```ts ignore ````.

To only type-check snippets, use `deno check --doc` (JSDoc) or `deno check --doc-only` (markdown).

## Checked

2026-11-04. Confirmed against docs runtime/test/doc_tests.md: deno test --doc, language identifiers, auto-imported exports, hashbang permission table, ignore attribute, deno check --doc/--doc-only.

Method: documentation only; no commands were run.
