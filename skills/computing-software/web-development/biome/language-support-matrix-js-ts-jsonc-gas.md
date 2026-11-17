---
id: computing-software.web-development.biome.language-support-matrix-js-ts-jsonc-gas
name: language-support-matrix-js-ts-jsonc-gas
category: computing-software
field: web-development
product: biome
tags: [biome, language-support, javascript, typescript, jsx, jsonc, google-apps-script, json, css, scss, yaml, graphql, markdown]
level: practitioner
status: docs-checked
description: "Know which languages Biome parses, formats and lints, plus JS/TS versions, JSONC defaults, well-known files and Google Apps Script."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/introduction/language-support.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Support per language (parsing, formatting, linting, GritQL plugins, JavaScript plugins):

- **Supported for parse, format and lint:** JavaScript, TypeScript, JSX, TSX, Google Apps Script, JSON, JSONC, CSS, SCSS, YAML, GraphQL, Markdown. GritQL plugins work for JS/TS/JSX/TSX/GAS, JSON, JSONC and CSS. JavaScript plugins work for JS/TS/JSX/TSX/GAS.
- **Parse and lint supported, formatting experimental:** HTML and SVG. HTML requires explicit opt-in.
- **Experimental everything:** Vue, Svelte, Astro (see the HTML super languages skill).
- **GritQL files:** parse and format only.

`.html` and `.htm` files are recognised as HTML.

**JavaScript:** ES2024. Only official syntax; development of new syntax starts when a proposal reaches Stage 3. **TypeScript:** version 5.9.

**Embedded snippets (experimental):** CSS (tags `css`, `styled`) and GraphQL (tags `gql`, `graphql`) in template literals, enabled with `javascript.experimentalEmbeddedSnippetsEnabled: true`.

**Google Apps Script:** `.gs` files are parsed as scripts, not modules, so top-level `import`/`export` is a parse error. Core service globals such as `SpreadsheetApp`, `DriveApp` and `Logger` are known: `noUndeclaredVariables` will not flag them and `noGlobalAssign` flags reassignment. For advanced services or custom globals list them in `javascript.globals`, e.g. `["MyLibrary", "BigQuery"]`.

**JSONC:** there is no separate JSONC language config. Use `json.parser.allowComments`, `json.parser.allowTrailingCommas` and `json.formatter.trailingCommas`. For `.jsonc` (or files whose VS Code language id is `jsonc`) Biome defaults to comments true, trailing commas allowed, formatter trailing commas `none`. Well-known files such as `tsconfig.json` and `.babelrc` allow comments and trailing commas without the extension; others such as `.eslintrc.json` allow only comments. Biome recognises these automatically.

## Checked

2026-11-08. Read the language-support page in full and compared the matrix rows with the description. Unchanged: support levels per language, ES2024, TypeScript 5.9, embedded snippets, Google Apps Script and JSONC defaults. Removed: the invented Verify step.

Method: documentation only; no commands were run.
