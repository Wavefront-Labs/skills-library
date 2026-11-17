---
id: computing-software.systems-network-administration.netbird.cli-global-flags
name: cli-global-flags
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, cli, global-flags, nb-env-vars, config-precedence]
level: intro
status: docs-checked
description: "NetBird CLI global flags and precedence: management URL, setup key and key file, hostname, log level, anonymize, daemon address, and NB_ environment variables."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/get-started/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax: `netbird [command] [subcommand] [flags]`; use `--help` after a command for details.

Global flags:
- `-m, --management-url`: management service URL (default `https://api.netbird.io:443`).
- `-k, --setup-key`: register with a setup key.
- `--setup-key-file`: read the key from a file (ignored if `--setup-key` is set).
- `-n, --hostname`: custom device hostname.
- `-l, --log-level`: default `info`.
- `--log-file`: `console` for stdout, `syslog`, or a file path; repeat the flag or comma-separate for several (default is a client.log under /var/log/netbird).
- `-A, --anonymize`: anonymize IPs and non-netbird.io domains in logs and status output.
- `--daemon-addr`: daemon address for CLI requests (unix, tcp or npipe).
- `-s, --service`: system service name, default `netbird`.
- `--preshared-key`: WireGuard PreSharedKey; only peers with the same key can communicate.
- `-c, --config`: profile file override; deprecated on `up` and `login` (use `--service-env NB_CONFIG=<path>`).
- `--admin-url`: deprecated and ignored.

Precedence, highest first: environment variables, then command-line flags, then the profile file entries. The page says the environment-first order is kept for backwards compatibility.

Every flag can be an environment variable: `NB_` prefix, dashes become underscores (`--management-url` is `NB_MANAGEMENT_URL`, `--log-level` is `NB_LOG_LEVEL`).

Top-level commands: `up`, `login`, `down`, `status`, `ssh`, `expose`, `networks`, `profile`, `debug`, `service`, `version`. `up` logs in if needed and connects; `login` authenticates only; `down` disconnects and the daemon returns to Idle.

## Checked

2026-11-04: read the CLI page (get-started/cli) in full. Confirmed every flag, default, the precedence order, the NB_ naming rule and the command list. Added the missing preshared-key and log-file detail from the page; removed the earlier paraphrase of the precedence that omitted the compatibility note.

Method: documentation only; no commands were run.
