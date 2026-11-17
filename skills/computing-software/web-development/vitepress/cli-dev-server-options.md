---
id: computing-software.web-development.vitepress.cli-dev-server-options
name: cli-dev-server-options
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, vitepress-dev, cli, dev-server, strictport, cors, base]
level: practitioner
status: docs-checked
description: "Use vitepress dev flags: --open, --port, --base, --cors, --strictPort and --force, and omit the dev subcommand in the current directory."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vitepress dev [root]` starts the dev server using the given directory as root (default: current directory). The `dev` word can be omitted when running in the current directory, so plain `vitepress` works.

```sh
vitepress                   # current directory, dev implied
vitepress dev docs          # sub directory as root
vitepress dev docs --port 3000 --strictPort --open /guide/
```

| Option | Effect |
|---|---|
| `--open [path]` | open the browser on startup (`boolean \| string`) |
| `--port <port>` | specify the port (`number`) |
| `--base <path>` | public base path, default `/` |
| `--cors` | enable CORS |
| `--strictPort` | exit if the specified port is already in use |
| `--force` | force the optimizer to ignore the cache and re-bundle |

The same page documents `vitepress build`, `vitepress preview` (options `--base`, `--assetsBase`, `--port`) and `vitepress init` (starts the setup wizard in the current directory).

## Checked

2026-11-04. Confirmed against the VitePress CLI reference (vitepress dev usage and options table). Removed: the default port 5173 (the page gives no default), the whole 'When to use what' advice section, the claim about 'dev server docs' on base, and the Verify step. Thin skill: about 100 words of confirmed content survive; the id is kept.

Method: documentation only; no commands were run.
