---
id: computing-software.data-engineering.kestra.install-standalone-jar
name: install-standalone-jar
category: computing-software
field: data-engineering
product: kestra
tags: [standalone, jar, systemd, jvm, plugins, install]
level: practitioner
status: docs-checked
description: "Run Kestra from the standalone JAR without Docker: server local vs standalone, config file lookup, installing plugins, and a systemd unit."
sources:
  - https://kestra.io/docs/installation/standalone-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requires JVM 21+. Download the JAR from https://api.kestra.io/v1/versions/download.

```shell
./kestra-VERSION server local
./kestra-VERSION server standalone
```

- `server local`: embedded H2 file database.
- `server standalone`: needs a configured external database.

Config: pass `--config` / `-c` with a YAML file, or put the full YAML in `KESTRA_CONFIGURATION` (create a `confs/` directory first, quote multi-line values). Default lookup is `${HOME}/.kestra/config.yaml`.

The JAR ships without plugins:

- Auto-install (`server local` only): `KESTRA_PLUGINS_AUTO_INSTALL_ENABLED=true` or `kestra.plugins.auto-install.enabled: true`.
- Manual: `kestra plugins install directory_with_plugins/`.
- Point to a directory with `KESTRA_PLUGINS_PATH`.

systemd unit essentials (`[Service]`):

```systemd
ExecStart=/bin/sh <PATH_TO_YOUR_KESTRA_JAR>/kestra-<VERSION> server standalone
Restart=always
KillMode=mixed
TimeoutStopSec=150
SuccessExitStatus=143
```

On Windows without `--config`, Kestra reads `%USERPROFILE%\.kestra\config.yaml`.

## Checked

2026-11-04. Confirmed against the Kestra standalone server page: JVM 21+, server local with H2 versus server standalone with a configured database, --config and -c, KESTRA_CONFIGURATION with a confs directory, default config lookup under the home directory and %USERPROFILE% on Windows, JAR without plugins, auto-install variable and setting, kestra plugins install, KESTRA_PLUGINS_PATH, the systemd unit settings. Nothing removed.

Method: documentation only; no commands were run.
