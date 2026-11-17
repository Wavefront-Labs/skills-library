---
id: computing-software.web-development.biome.javascript-parser-globals-jsx-runtime-and-pnpm-catalogs
name: javascript-parser-globals-jsx-runtime-and-pnpm-catalogs
category: computing-software
field: web-development
product: biome
tags: [biome, javascript-globals, jsxruntime, react-classic, jsxeverywhere, parameter-decorators, pnpm-catalog, embedded-snippets, tsconfig]
level: advanced
status: docs-checked
description: "Tune the JavaScript parser and analyzer: jsxEverywhere, parameter decorators, globals, jsxRuntime transparent or reactClassic, pnpm catalogs."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `javascript.parser.jsxEverywhere` (default true): allow JSX in `.js`, `.mjs` and `.cjs`. When false, JSX there raises a diagnostic.
- `javascript.parser.unsafeParameterDecoratorsEnabled` (default false): parse decorators on class parameters such as `method(@Decorator() value)`. This is an old experimental proposal and may change; enable only if existing code requires it.
- `javascript.globals` (string[]): extra names the linter treats as predefined globals, for runtime, framework or external-script variables: `{ "javascript": { "globals": ["$", "_", "externalVariable"] } }`.
- `javascript.jsxRuntime`: `transparent` (default) or `reactClassic`. It only tells the analyzer how JSX imports count; it does not transform JSX or choose a build runtime. `transparent` suits the automatic React JSX transform, native JSX environments and setups with no factory import. `reactClassic` is for the classic React transform: Biome treats the React import, or custom JSX factory imports configured in `tsconfig.json`, as used by JSX (TypeScript `"jsx": "react"`).
- `javascript.resolver.experimentalPnpmCatalogs` (default false): resolve `catalog:` and `catalog:<name>` versions in `dependencies`, `devDependencies` and `peerDependencies` using `catalog` and `catalogs` in `pnpm-workspace.yaml`. If that file is missing, unreadable or invalid, Biome behaves as if the option were off.
- `javascript.experimentalEmbeddedSnippetsEnabled` (default false): parse, format, lint and fix CSS in `css` and `styled` templates and GraphQL in `gql` and `graphql` templates or calls. Templates with interpolations are not supported yet.
- `javascript.linter.enabled`, `javascript.assist.enabled`, `javascript.formatter.enabled` all default to true.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
