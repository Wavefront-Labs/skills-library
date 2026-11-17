---
id: computing-software.web-development.hugo.tailwind-css
name: tailwind-css
category: computing-software
field: web-development
product: hugo
tags: [tailwind, css-tailwindcss, hugo-stats, npm, templates-defer]
level: practitioner
status: docs-checked
description: "Process Tailwind CSS v4 with css.TailwindCSS: npm install, hugo_stats.json source, options, defer in baseof and CSS variable injection."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/css/TailwindCSS.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`css.TailwindCSS` runs the Tailwind CSS CLI on a resource and returns a `resource.Resource`. It needs Tailwind CSS v4.0 or later installed through npm; the standalone binary is no longer supported as of v0.161.0.

Setup:

1. Install `tailwindcss`, `@tailwindcss/cli` and `@tailwindcss/typography` as dev dependencies (the page's example installs all three).
2. In the project config: enable build stats, add cachebuster rules, mount `hugo_stats.json` into `assets`, and allow the `tailwindcss` and `node` commands under `security.exec`.
3. In `assets/css/main.css`:

```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
@source "hugo_stats.json";
```

Tailwind respects `.gitignore`, so `hugo_stats.json` must be sourced explicitly.

4. Create `layouts/_partials/css.html`: get the CSS, pass it to `css.TailwindCSS` with `minify` outside development, and fingerprint for production.
5. Call the partial from `baseof.html` inside `templates.Defer`, so it runs after all sites and output formats render.

Options:

- `disableInlineImports` (v0.147.4+, default `false`)
- `importContext` (v0.165.0+; no effect when inline imports are disabled)
- `minify` (default `false`)
- `optimize` (default `false`; optimizes without minifying)
- `skipInlineImportsNotFound` (default `false`)

To inject CSS variables, run `css.Build` first with `vars`, list `tailwindcss` under `externals`, then pass the result to `css.TailwindCSS` with `disableInlineImports` set to `true`.

## Checked

2026-11-04. Confirmed against the Hugo docs page css.TailwindCSS: Tailwind v4.0 or later via npm, the standalone binary dropped as of v0.161.0, the configuration (build stats, cachebusters, mounts, `security.exec`), the entry file and `.gitignore` note, the partial and `templates.Defer`, the five options with versions and defaults, and the `css.Build` variable injection pattern. Removed the word optionally for the typography package, which the page does not say.

Method: documentation only; no commands were run.
