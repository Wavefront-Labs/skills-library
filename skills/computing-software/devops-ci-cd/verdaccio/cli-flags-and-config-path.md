---
id: computing-software.devops-ci-cd.verdaccio.cli-flags-and-config-path
name: cli-flags-and-config-path
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [cli, config-path, listen-flag, cli-flags, config-location, xdg]
level: practitioner
status: docs-checked
description: "Verdaccio CLI flags (--listen, --config, --port, --info, --mask) and how the default config.yaml and storage locations are chosen from XDG and APPDATA paths."
sources:
  - https://verdaccio.org/docs/cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flags: `--listen/-l` (default `localhost:4873`), `--config/-c`, `--info/-i`, `--version/-v`; on 7.x also `--port/-p` (alias of `--listen`) and `--mask` (hides file paths in the `--info` report). On 6.x use `--listen` and `--info`.

```
verdaccio --listen 4000 --config ./config.yaml
```
`--listen` accepts a port, `host:port`, `proto://host:port`, a bracketed IPv6 address or `unix:/path/to.sock`, and overrides the `listen` key in the file.

Config lookup without `--config`: the first existing file among
1. `$XDG_CONFIG_HOME/verdaccio/config.yaml` (falls back to `$HOME/.config`; only if that base directory exists)
2. `%APPDATA%\verdaccio\config.yaml` on Windows
3. `./verdaccio/config.yaml`
4. `./config.yaml`

If none exists, a default is written to the first candidate and the path is logged.

Format: YAML only, `.yaml` or `.yml`. 6.x still loads JSON or JS configs (deprecation warning VERDEP004); 7.x fails with `config file must be a YAML file`.

Default storage: `$XDG_DATA_HOME` (falls back to `$HOME/.local/share`) plus `verdaccio/storage`. `VERDACCIO_STORAGE_PATH` overrides it.

To see which file a running process picked up: `verdaccio --info`, or the `conf` field of the `/-/_debug` endpoint.

## Checked

2026-11-04. Confirmed against the Command Line Tool page (flags, 7.x-only --port and --mask, candidate config paths, default config creation, VERDEP004, YAML-only error, default storage location). Nothing removed.
Method: documentation only; no commands were run.
