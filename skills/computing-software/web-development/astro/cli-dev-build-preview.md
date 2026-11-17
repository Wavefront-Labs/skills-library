---
id: computing-software.web-development.astro.cli-dev-build-preview
name: cli-dev-build-preview
category: computing-software
field: web-development
product: astro
tags: [astro-cli, astro-dev, astro-build, astro-preview, package-scripts]
level: intro
status: docs-checked
description: "Run astro dev, build and preview: package.json scripts, passing flags through npm with --, dev hotkeys, devOutput, and common flags like port and host."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/reference/cli-reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Typical scripts (added by the `create astro` wizard):

```json title="package.json"
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview"
  }
}
```

Pass flags through npm with an extra `--`:

```shell
npm run dev -- --port 8080
npm run build -- --verbose
```

`astro dev` starts the HMR dev server, which does not bundle assets. Hotkeys: `s + enter` sync the content layer, `o + enter` open in browser, `q + enter` quit.

`astro build` writes static files to `dist/` (plus server files if any route renders on demand). `--devOutput` produces a development-based build to test build-only issues.

`astro preview` serves the built output locally to catch errors before deploying; it is not designed for production.

Common flags: `--root <path>`, `--config <path>` (default `astro.config.mjs`), `--force` (clear the content layer cache), `--mode <string>`, `--outDir`, `--site`, `--base`, `--port <number>` (default `4321`), `--host` (all addresses) or `--host <custom-address>`, `--allowed-hosts`, `--verbose`, `--silent`, `--open`.

Do not use `--host` to expose the dev or preview server in production.

## Checked

2026-11-04. Confirmed against the Astro CLI reference: scripts, npm -- passthrough, dev hotkeys, --devOutput, common flags and the default port 4321. Nothing removed.

Method: documentation only; no commands were run.
