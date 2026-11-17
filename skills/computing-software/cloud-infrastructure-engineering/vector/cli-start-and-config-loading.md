---
id: computing-software.cloud-infrastructure-engineering.vector.cli-start-and-config-loading
name: cli-start-and-config-loading
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [cli, configuration, config-dir, watch-config, formats, flags, vector]
level: practitioner
status: docs-checked
description: "Start Vector with the right config sources, formats, log flags and graceful shutdown options."
sources:
  - https://vector.dev/docs/reference/cli/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Running `vector` with no subcommand starts it. Key options:

- `--config` / `-c` (env `VECTOR_CONFIG`): one or more files, wildcards allowed. Default is `/etc/vector/vector.yaml`. Format comes from the extension (.yaml, .toml, .json) and falls back to YAML.
- `--config-dir`: read every file in a directory; names not ending in .toml, .json, .yaml or .yml are ignored.
- `--config-yaml`, `--config-toml`, `--config-json`: force the format.
- `--watch-config` / `-w`: reload when files change. `--watch-config-method` is `recommended` (event based) or `poll` for cases like NFS, with `--watch-config-poll-interval-seconds` (default 60).
- `--require-healthy` / `-r`: exit at startup if any sink fails its healthcheck.
- `--graceful-shutdown-limit-secs` (default 60) after SIGINT or SIGTERM, or `--no-graceful-shutdown-limit` to wait until SIGKILL.
- `--threads` / `-t`: defaults to the number of cores.
- `--log-format` `text` or `json`; `-v`/`-q` change verbosity.
- `--allow-empty-config` allows a stub config to be replaced later.

```bash
vector --config /etc/vector/vector.yaml --watch-config --require-healthy
```

Other subcommands: `validate`, `test`, `top`, `tap`, `graph`, `list`, `generate`, `vrl`.

Use `--require-healthy` in orchestrated environments so a broken credential fails the pod instead of silently running.

Verify with `vector --version` and by watching startup logs for loaded components.

## Checked

2026-11-03. Read reference/cli. Confirmed: the default config path, format detection and YAML fallback, `--config-dir` file-name rules, `--config-yaml/-toml/-json`, `--watch-config`/`-w`, `--watch-config-method` values, the 60-second poll interval default, `--require-healthy`/`-r`, `--graceful-shutdown-limit-secs` default 60, `--no-graceful-shutdown-limit`, `--threads`/`-t`, `--log-format`, `-v`/`-q`, `--allow-empty-config`, `--version`/`-V`, and the subcommand list. Nothing removed.

Method: documentation only; no commands were run.
