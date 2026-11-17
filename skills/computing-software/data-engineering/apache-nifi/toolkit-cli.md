---
id: computing-software.data-engineering.apache-nifi.toolkit-cli
name: toolkit-cli
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, toolkit, cli, cli-sh, registry, session]
level: practitioner
status: docs-checked
description: "NiFi Toolkit CLI (bin/cli.sh): one-shot vs interactive mode, command groups, properties files with -p, session defaults, argument precedence and output types."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/toolkit-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toolkit CLI

- Script is `./bin/cli.sh` (not nifi.sh). `cli.sh <command> <args>` runs one command; `cli.sh` alone opens the interactive shell; `-h` and `<command> -h` show help.
- Groups: `nifi ...`, `registry ...`, `session ...`, plus `demo quick-import`, `exit`, `help`.
- Examples from the guide: `registry list-buckets -u http://localhost:18080`, `registry export-all-flows --outputDirectory <dir>`, `registry import-all-flows --input <dir> --skipExisting`.
- `-p <file>` loads connection settings such as `baseUrl`, keystore, truststore and `proxiedEntity`.
- Session defaults: `session set nifi.props <file>` and `session set nifi.reg.props <file>` write to `~/.nifi-cli.config`; also `keys`, `show`, `get`, `remove`, `clear`.
- Precedence: direct argument, then `-p` file, then session.
- `-ot` / `--outputType`: `simple` or `json`; default is json standalone, simple interactive.

Verify: `registry list-buckets` against your registry returns the expected buckets.

## Checked

Checked against the NiFi Toolkit Guide, NiFi CLI section: script name, one-shot and interactive modes, command groups, the session subcommands, `.nifi-cli.config` in the home directory, argument precedence, the properties file keys, and the `-ot` output defaults match.

Method: docs-only read of cited pages, 2026-11-08
