---
id: computing-software.cloud-infrastructure-engineering.garage.garage-cli-config-file-lookup
name: garage-cli-config-file-lookup
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-config-file, garage-config-env, config-flag, docker-alias]
level: intro
status: docs-checked
description: "Point the garage CLI at the right config with GARAGE_CONFIG_FILE or -c, including a Docker alias."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `garage` binary is both the server and the administration CLI. The CLI reads the configuration file to learn how to contact the local node, and needs read access to the metadata directory as well.

The default config path is `/etc/garage.toml`. Override it either by:

- setting `GARAGE_CONFIG_FILE`, for example `export GARAGE_CONFIG_FILE=$(pwd)/garage.toml`, or
- passing `-c` per command, for example `garage -c ./garage.toml status`.

For a container, define a local alias so every command runs the binary inside it:

`alias garage="docker exec -ti <container name> /garage"`

The Quick Start also shows `docker exec garage-container /garage status`.

Test the setup with `garage status`. If it fails, check path and permissions first; the troubleshooting list says the config file, `metadata_dir` and `data_dir` must be readable by the user running the CLI or server.

Help is built in: `garage help` lists commands and flags such as `garage bucket allow --help` explain each one.

## Checked

2026-11-04. Read the Quick Start page in full. Confirmed the default path, the environment variable, the -c flag, the alias, the status test, the troubleshooting permissions and the help commands. Removed the claim that the second docker form is for use without a TTY, which the page does not say.
Method: documentation only; no commands were run.
