---
id: computing-software.data-engineering.trino.trino-launcher-and-logs
name: trino-launcher-and-logs
category: computing-software
field: data-engineering
product: trino
tags: [launcher, bin-launcher, server-log, http-request-log, daemon]
level: practitioner
status: docs-checked
description: "Start, stop and inspect Trino with bin/launcher, the default pid and log locations, and what launcher.log, server.log and http-request.log contain."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/installation/deployment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino launcher and logs

The installation ships `bin/launcher`, usable manually or as a daemon startup script.

Commands:
- `run`: start in the foreground; stop with Ctrl+C or `stop` from another terminal.
- `start`: start as a daemon and print the process ID.
- `stop`: SIGTERM a server started with `start` or `run`.
- `restart`: stop then start (or start a stopped server) with a new PID.
- `kill`: SIGKILL a possibly hung server.
- `status`: prints `Stopped pid` or `Running as pid`.

`-v` or `--verbose` prepends current settings: `bin/launcher -v status` shows the PID and configuration. Run with `--help` for options to move configuration files, directories and Java options. With a supervisor such as daemontools, use `bin/launcher run` and capture both stdout and stderr.

Defaults: configuration directory `etc`, data directory equal to the installation directory, pid file `var/run/launcher.pid`, logs in `var/log`. All can be changed; the Trino RPM, for instance, adjusts them to follow the Linux Filesystem Hierarchy Standard.

Log files:
- `launcher.log`: connected to the server's stdout and stderr; early messages before logging initialises plus JVM errors and diagnostics.
- `server.log`: the main log, usually where initialisation failures appear; rotated and compressed automatically.
- `http-request.log`: every HTTP request the server received; rotated and compressed.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
