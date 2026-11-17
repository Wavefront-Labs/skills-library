---
id: computing-software.web-development.bun.bundler-loaders
name: bundler-loaders
category: computing-software
field: web-development
product: bun
tags: [bundler-loaders, import-attributes, file-loader, embed-sqlite]
level: practitioner
status: docs-checked
description: "Pick Bun loaders by extension, override them with import attributes, import toml, yaml, text, sqlite or html files, and avoid loader gotchas."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/bundler/loaders.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Defaults by extension: `js` (.cjs .mjs), `jsx` (.js .jsx), `ts` (.ts .mts .cts), `tsx`, `json`, `jsonc`, `toml`, `yaml` (.yaml .yml), `xml`, `text` (.txt .text), `napi` (.node), `html`, `css`, `sh`, and `file` for everything unrecognized (bundler copies it to `outdir` and resolves to the new path).

Override per import:

```ts
import cfg from "./config.data" with { type: "toml" };
const page = await import("./page.html", { with: { type: "text" } });  // string, not bundled HTML
import db from "./app.db" with { type: "sqlite", embed: "true" };
```

Behaviours:
- `json`, `toml`, `yaml` are inlined as objects; as an entrypoint they become a module with `export default`.
- `jsonc` also handles tsconfig.json, jsconfig.json, package.json and bun.lock.
- `xml` parses to `Bun.XML.parse` shape: attributes as `"@name"` keys, repeated children as arrays, all values strings.
- `file` imports honour `publicPath`; `naming.asset` sets where copies go.

Gotchas:
- A `sqlite` import works for the Bun target only and stays external unless `embed: "true"`; standalone executables always embed it. Otherwise the db is copied to `outdir` with a hashed name.
- `html` acts differently under `bun build`, `bun run` and `--target=bun` (where it resolves to a manifest for `Bun.serve`).

## Checked

2026-11-04. Confirmed against the Bun docs page bundler/loaders: default loader per extension, the type import attribute (static and dynamic), json/toml/yaml inlining and export default for entrypoints, jsonc for tsconfig.json/jsconfig.json/package.json/bun.lock, xml output shape (attribute keys, arrays, all strings), text loader and html imported as text, file loader with publicPath and naming.asset, sqlite loader limited to target bun with embed and the standalone-executable and hashed-copy behaviour, and the three html loader contexts. The list of default extensions in the skill is a subset of the page (json5, md, wasm are omitted but nothing is contradicted).
Method: documentation only; no commands were run.
