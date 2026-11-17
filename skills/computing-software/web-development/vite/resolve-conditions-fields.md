---
id: computing-software.web-development.vite.resolve-conditions-fields
name: resolve-conditions-fields
category: computing-software
field: web-development
product: vite
tags: [resolve-conditions, resolve-main-fields, resolve-extensions, resolve-tsconfig-paths]
level: advanced
status: docs-checked
description: "Tune package entry resolution: resolve.conditions with the development|production token, mainFields defaults, extensions, preserveSymlinks and tsconfigPaths limits."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `resolve.conditions`: default `['module', 'browser', 'development|production']`. Extra allowed conditions for package `exports`; list from most to least specific. `development|production` becomes `production` when `process.env.NODE_ENV === 'production'`, otherwise `development`. `import`, `require` and `default` always apply when their requirements are met; `style` applies to style imports, plus `sass` and `less` for those pre-processors.
- `resolve.mainFields`: default `['browser', 'module', 'jsnext:main', 'jsnext']`. Lower precedence than `exports`: if `exports` resolves an entry, main fields are ignored.
- `resolve.extensions`: default `['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json']`. Omitting extensions for custom types like `.vue` is not recommended.
- `resolve.preserveSymlinks`: default `false`; `true` identifies files by the original path rather than the real one.
- `resolve.tsconfigPaths`: default `false`. `paths` applies only to files matched by a tsconfig's `files` or `include`; non-JS files (CSS) must be listed explicitly, for example `"src/**/*.css"`. It does not apply inside `.less` files; use a relative path or `resolve.alias`.

## Checked

2026-11-07. Re-read the Shared Options page (docs/config/shared-options.md) in full. Confirmed the defaults and wording for resolve.conditions (including the development|production value, import/require/default, style, sass and less), resolve.mainFields, resolve.extensions, resolve.preserveSymlinks and resolve.tsconfigPaths (files/include matching, explicit CSS globs, no Less support). Removed the two '(not inherited)' notes, which rest on a badge the page does not explain.

Method: documentation only; no commands were run.
