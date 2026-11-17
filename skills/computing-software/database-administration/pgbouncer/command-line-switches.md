---
id: computing-software.database-administration.pgbouncer.command-line-switches
name: command-line-switches
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, cli, daemon, verbose, windows-service]
level: intro
status: docs-checked
description: "The pgbouncer command line: -d, -u, -v, -q, -V, -h and the Windows service switches."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start the pgbouncer binary with the right switches.

Synopsis: `pgbouncer [-d][-v][-u user] <pgbouncer.ini>`; also `pgbouncer -V|-h`.

Switches:

- `-d`, `--daemon`: run in the background. Without it the process stays in the foreground. In daemon mode pidfile and either logfile or syslog are required, and nothing is written to stderr after backgrounding. Does not work on Windows.
- `-u USERNAME`, `--user=USERNAME`: switch to the given Unix user on startup. Same as the `user` setting; it works only if PgBouncer starts as root or already runs as that user.
- `-v`, `--verbose`: increase verbosity; repeat it (`-v -v`) for more. Mirrors `verbose=2`; 3 is the highest supported.
- `-q`, `--quiet`: do not log to stderr. It does not change verbosity, only the destination. Intended for init.d scripts. Note that setting logfile alone does not turn off stderr logging; use -q or -d for that.
- `-V`, `--version`: show version.
- `-h`, `--help`: show short help.

Windows only: `pgbouncer.exe [-v][-u user] <pgbouncer.ini>`, plus `--regservice <pgbouncer.ini>` to register a Windows service (named by service_name, default pgbouncer) and `--unregservice <pgbouncer.ini>` to remove it.

The libevent kernel notification method can be disabled with the environment variables EVENT_NOEPOLL, EVENT_NOKQUEUE, EVENT_NODEVPOLL, EVENT_NOPOLL or EVENT_NOSELECT. Setting EVENT_SHOW_METHOD makes libevent display the method in use.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
