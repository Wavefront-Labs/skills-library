---
id: computing-software.web-development.docusaurus.cli-build-and-serve
name: cli-build-and-serve
category: computing-software
field: web-development
product: docusaurus
tags: [docusaurus-build, docusaurus-serve, out-dir, no-minify, lightning-css]
level: practitioner
status: docs-checked
description: "Use docusaurus build and docusaurus serve: output directory, locale builds, dev-mode builds, skipping minification, and serving a production build locally."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`docusaurus build [siteDir]` compiles the site for production.

| Option | Default | Use |
| --- | --- | --- |
| `--dev` | | build in dev mode with full React error messages |
| `--out-dir` | `build` | output directory, relative to the current workspace |
| `--config` | | path to the config file |
| `--locale` | all known locales | build only the given locale(s) |
| `--no-minify` | `false` | skip minifying JS/CSS |

CSS bundles are minified with Lightning CSS, using your Browserslist config as targets. Skip HTML minification with the environment variable `SKIP_HTML_MINIFICATION=true`.

`docusaurus serve [siteDir]` serves the built website locally.

| Option | Default | Use |
| --- | --- | --- |
| `--port` | `3000` | port |
| `--dir` | `build` | output directory to serve |
| `--build` | `false` | build before serving |
| `--host` | `localhost` | e.g. `0.0.0.0` for external access |
| `--no-open` | `false` locally, `true` in CI | do not open a browser |

```sh
npm run build && npm run serve
```

## Checked

2026-11-04: read the Docusaurus CLI page in full. Confirmed the build and serve option tables with defaults, Lightning CSS with Browserslist, and SKIP_HTML_MINIFICATION. Nothing removed.

Method: documentation only; no commands were run.
