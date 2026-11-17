---
id: computing-software.database-administration.patroni.patronictl-configuration-and-global-options
name: patronictl-configuration-and-global-options
category: computing-software
field: database-administration
product: patroni
tags: [patroni, patronictl, configuration, dcs-url, insecure]
level: intro
status: docs-checked
description: "How patronictl finds its config file and DCS, and its global flags -c, -d and -k."
sources:
  - https://patroni.readthedocs.io/en/latest/patronictl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run patronictl from any host with the right settings.

patronictl is a client of the Patroni REST API and the DCS, so it can run on remote machines. It reads three configuration sections: `ctl` (REST API authentication and server validation), `restapi` (fallback: `restapi.authentication` and `restapi.cafile`) and the DCS section (for example etcd). They can come from environment variables or a file.

Default file name is `patronictl.yaml`, searched in:
- Unix: the user config directory under `patroni`, or the POSIX-style dot-directory `.patroni` in the home directory
- Mac OS X: the Application Support directory under `patroni`, or `.patroni` in home
- Windows: the roaming or local AppData `patroni` folder

Override with the environment variable `PATRONICTL_CONFIG_FILE` or `-c/--config-file`. On a Patroni host you can reuse the Patroni config if it has the needed sections.

Global options:
- `-c / --config-file PATH`
- `-d / --dcs-url / --dcs DCS://HOST:PORT/NAMESPACE`, for example `etcd3://localhost:2379/service`. Missing parts come from the configuration or defaults.
- `-k / --insecure`: skip REST API SSL certificate validation.

Synopsis: `patronictl [-c FILE] [-d URL] [-k] SUBCOMMAND`. If CLUSTER_NAME is omitted in most subcommands, it is taken from `scope` in the configuration.

## Checked

2026-11-03. Confirmed against the patronictl page: the three configuration sections, patronictl.yaml search paths, PATRONICTL_CONFIG_FILE, and `-c`, `-d`/`--dcs-url`/`--dcs`, `-k` options with the synopsis.

Method: documentation only; no commands were run.
