---
id: computing-software.messaging-and-integration.nats.server-command-line-flags
name: server-command-line-flags
category: computing-software
field: messaging-and-integration
product: nats
tags: [nats-server, flags, cli, store-dir, jetstream-flag, monitoring-port]
level: practitioner
status: docs-checked
description: "Start nats-server from flags: bind addr/port, name, config, -js and -sd, auth, logging, TLS and cluster flags, config test with -t."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/running/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure a server from the command line without a config file, and know which flag is which.

Server options: `-a/--addr/--net` (default `0.0.0.0`), `-p/--port` (default 4222), `-n/--name/--server_name`, `-P/--pid`, `-m/--http_port` or `-ms/--https_port` for the monitoring dashboard (mutually exclusive), `-c/--config` path, `-t` test the config and exit, `-sl/--signal` signal a running server, `--client_advertise`, `--ports_file_dir`.

JetStream: `-js/--jetstream` enables it and `-sd/--store_dir` sets the storage directory.

Auth: `--user` plus `--pass`, or `--auth` token (the token is exclusive of user/pass).

Logging: `-l/--log` file, `-T=false` removes timestamps, `-s/--syslog`, `-r/--remote_syslog` (for example `udp://localhost:514`), `-D/--debug`, `-V/--trace`, `-VV`, `-DV`, `-DVV` (the double V also traces the system account), `--max_traced_msg_len`.

TLS: `--tls` (does not verify clients), `--tlscert`, `--tlskey`, `--tlsverify` (verify client certificates), `--tlscacert`.

Cluster: `--routes`, `--cluster`, `--cluster_listen`, `--cluster_advertise`, `--no_advertise`, `--connect_retries`.

Common: `-h`, `-v`, `--help_tls`.

Gotchas: flags such as `--user`/`--pass` put credentials on the process command line; prefer a config file for real deployments. Monitoring exposes data on its port, so restrict it.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
