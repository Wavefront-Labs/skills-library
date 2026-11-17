---
id: computing-software.systems-network-administration.icinga-2.cli-commands-daemon-feature-object-variable
name: cli-commands-daemon-feature-object-variable
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, cli, icinga2-daemon, feature-enable, object-list, variable, console]
level: practitioner
status: docs-checked
description: Use the icinga2 CLI - daemon -C validation, reload, feature enable and disable, object list, variable get and list, ca, pki and node commands, api setup, and the console.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/11-cli-commands/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# icinga2 CLI commands
Run any command with `--help`; bash completion ships in `/etc/bash_completion.d/icinga2` (needs the `bash-completion` package).

**Commands:** `api setup`, `ca list|sign|remove|restore`, `console`, `daemon`, `feature enable|disable|list`, `node setup|wizard`, `object list`, `pki new-ca|new-cert|request|save-cert|sign-csr|ticket|verify`, `variable get|list`.

**Global options:** `-D` defines a constant, `-I` adds an include search directory (used by `include <file.conf>`), `-x` sets the console log level (debug, notice, information, warning, critical), `-X` enables the script debugger.

**Validate before reload:** `icinga2 daemon -C` reports file, line and message of errors. Then `systemctl reload icinga2`: `SIGHUP` makes the daemon validate in a separate process without stopping checks or notifications.

**Features:** `icinga2 feature list`, `feature enable graphite`, `feature disable ido-mysql`. These do not restart Icinga 2; restart afterwards.

**Inspect objects:** after validation passes, `icinga2 object list` shows attributes, inheritance and apply-rule-created objects.

**Console:** `icinga2 console` evaluates config expressions locally; `--eval`, `--file`, `--syntax-only`, `--sandbox` and `--connect` (needs API `console` permission) are available.

## Checked

2026-11-04. Confirmed against the Icinga 2 CLI commands chapter: command list, global options -D -I -x -X, bash completion file, ca subcommands and daemon -C.

Method: documentation only; no commands were run.
