---
id: computing-software.web-development.hugo.js-build
name: js-build
category: computing-software
field: web-development
product: hugo
tags: [js-build, esbuild, typescript, jsx, bundling, artifacts]
level: practitioner
status: docs-checked
description: "Bundle, transpile and minify JavaScript and TypeScript with js.Build (esbuild): format, targetPath, imports, params, node_modules and artifacts."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/js/Build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`js.Build` uses esbuild to bundle, transpile (TypeScript and JSX), tree shake, minify and create source maps for a JavaScript resource. It returns a resource.

Options:

- `format`: `iife` (default), `cjs` or `esm`.
- `importContext`: a resource getter Hugo checks first when resolving imports (v0.165.0).
- `targetPath`: output path; the extension may change for TypeScript sources.
- `params`: template data passed to JS, imported via `@params`.
- `externals`, `defines`, `minify` and `sourceMap` also appear in the examples.

Imports:

- Resolve against Hugo's unified assets file system: `my/module` resolves to the top-most `index.{js,ts,tsx,jsx}` in `assets/my/module`.
- A leading `.` resolves relative to the current file.
- Non-JS files such as JSON or CSS need the full path with extension.
- Hugo generates `assets/jsconfig.json` to map imports for editors; this can be disabled.

Node.js dependencies: unresolved imports, or imports from files outside `assets`, are resolved by esbuild from `node_modules` within allowed paths. Run `npm install` before building. Theme or component authors should use `hugo mod npm pack`.

Artifacts (v0.165.0): extra files from esbuild's file loader (fonts, images) and source maps (`sourceMap` of `external` or `linked`) appear in `.Data.Artifacts`, each with `MediaType`, `Permalink` and `RelPermalink`.

Common pattern: toggle `minify` and `sourceMap` with `hugo.IsDevelopment`, and add fingerprinting plus an `integrity` attribute in production.

## Checked

2026-11-04. Confirmed against the Hugo docs page js.Build: the esbuild-backed feature list, `format` values and default, `importContext` and artifacts (v0.165.0), `targetPath`, import resolution rules, `@params`, the generated `assets/jsconfig.json`, `node_modules` resolution, `hugo mod npm pack` and the `.Data.Artifacts` members. Nothing removed.

Method: documentation only; no commands were run.
