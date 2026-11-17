---
id: computing-software.web-development.vitepress.cli-build-options
name: cli-build-options
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, vitepress-build, cli, outdir, assetsbase, assetsinlinelimit, target, mpa]
level: practitioner
status: docs-checked
description: "Run vitepress build with --base, --assetsBase, --outDir, --target, --assetsInlineLimit and --mpa for production output control."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vitepress build [root]` builds the production site (static HTML plus hashed assets).

| Option | Meaning |
|---|---|
| `--mpa` (experimental) | build in MPA mode, no client-side hydration |
| `--base <path>` | public base path (default `/`) |
| `--assetsBase <url>` | URL prefix generated assets are served from, such as a CDN |
| `--target <target>` | transpile target (default `"modules"`) |
| `--outDir <dir>` | output directory relative to the current working directory (default `<root>/.vitepress/dist`) |
| `--assetsInlineLimit <number>` | base64-inline threshold for static assets in bytes (default 4096) |

Notes that bite:

- `--outDir` is relative to the **cwd**, not to the root, unlike the config option `outDir` which is relative to the project root.
- `--base` and `--assetsBase` override config for that build only, which suits CI where the value is environment-specific:

```sh
vitepress build docs --base /my-repo/ --assetsBase "$CDN_URL"
```

- Lower `--assetsInlineLimit` if small images inflating HTML is a concern; the default inlines assets under 4 kB.
- `--mpa` ships zero JS by default (see the MPA mode skill).

After building, run `vitepress preview` to check the result locally.

Verify: the output directory contains `index.html` and an `assets/` folder with hashed filenames.

## Checked

2026-11-04. Confirmed against the VitePress CLI reference (vitepress build options and defaults) and the site-config page (assetsBase, MPA mode ships 0kb JavaScript by default). Removed: the claim that the dev server does not apply production behaviours.

Method: documentation only; no commands were run.
