---
id: computing-software.web-development.vite.cli-dev-server
name: cli-dev-server
category: computing-software
field: web-development
product: vite
tags: [vite-dev-command, dev-server-flags, strict-port, config-loader]
level: practitioner
status: docs-checked
description: "Use the vite dev server CLI flags: host, port, open, cors, strictPort, force, config, base, logLevel, configLoader, profile, debug, and mode."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`vite [root]` starts the dev server; `vite dev` and `vite serve` are aliases.

Options:
- `--host [host]`, `--port <port>`, `--open [path]`, `--cors`
- `--strictPort`: exit if the port is already in use
- `--force`: ignore the optimizer cache and re-bundle
- `--experimentalBundle`: experimental full bundle mode (highly experimental)
- `-c, --config <file>`, `--base <path>` (default `/`)
- `-l, --logLevel <level>`: info | warn | error | silent
- `--clearScreen`: allow or disable clearing the screen when logging
- `--configLoader <loader>`: `bundle` (default, bundles the config with Rolldown), `runner` (experimental, processes on the fly) or `native` (experimental, native runtime)
- `--profile [name]`: start the Node.js inspector and write `<name>.cpuprofile`
- `-d, --debug [feat]` and `-f, --filter <filter>`: debug logs and a filter
- `-m, --mode <mode>`: set the env mode
- `-h, --help`, `-v, --version`

```bash
vite --port 3000 --strictPort --open
vite --force
```

Run `npx vite --help` for the list for your installed version.

## Checked

2026-11-04. Confirmed against the Vite CLI guide (docs/guide/cli.md, dev server section): flags, the aliases vite dev and vite serve, logLevel values, configLoader values and default, profile cpuprofile output. Nothing removed.

Method: documentation only; no commands were run.
