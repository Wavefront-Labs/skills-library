---
id: computing-software.devops-ci-cd.packer.configure-env-vars
name: configure-env-vars
category: computing-software
field: devops-ci-cd
product: packer
tags: [environment-variables, packer-cache-dir, no-color, checkpoint, config-env, configure]
level: practitioner
status: docs-checked
description: "Packer environment variables for cache, timeouts, colour, update checks and the config directory."
sources:
  - "https://developer.hashicorp.com/packer/docs/configure/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Packer reads several environment variables.

- `PACKER_CONFIG_DIR` overrides the config directory, default `${HOME}/.config/packer/` (XDG) or `%APPDATA%\packer.d\` on Windows.
- `PACKER_CACHE_DIR` sets where downloaded files such as ISOs are cached; default `./packer_cache/`.
- `PACKER_GETTER_READ_TIMEOUT` overrides the timeout when a plugin fetches an ISO; default `30m`, needs a plugin built on SDK v0.6.0 or later.
- `PACKER_NO_COLOR` disables coloured output.
- `PACKER_PLUGIN_PATH` overrides plugin discovery.
- `PACKER_LOG` and `PACKER_LOG_PATH` control logging.
- `CHECKPOINT_DISABLE=1` stops Packer calling checkpoint.hashicorp.com to look for new versions.
- `TMPDIR` (Unix) or `TMP`, `TEMP`, `USERPROFILE` (Windows) set the temporary directory; change it where the default is non-writable or non-executable.

A deprecated JSON config file can be set through `PACKER_CONFIG` or `${HOME}/.packerconfig`. It supports `plugin_min_port` (10000) and `plugin_max_port` (25000) to bound the ports used by plugin processes.

```bash
export PACKER_CACHE_DIR=/path/to/cache
export CHECKPOINT_DISABLE=1
```

## Checked
2026-11-03. Confirmed against the Configure Packer page: config directory defaults, cache directory, getter timeout, no-color, plugin path, logging, checkpoint, temp directory, the deprecated JSON file and its 10000/25000 port defaults. Removed unsourced CI advice.
Method: documentation only; no commands were run.
