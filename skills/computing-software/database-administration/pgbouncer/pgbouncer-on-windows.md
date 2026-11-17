---
id: computing-software.database-administration.pgbouncer.pgbouncer-on-windows
name: pgbouncer-on-windows
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, windows, service, regservice, event-log]
level: advanced
status: docs-checked
description: "Building and running PgBouncer on Windows: MinGW, service registration, event log and unsupported switches."
sources:
  - https://www.pgbouncer.org/install.html
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run PgBouncer as a Windows service.

Build: the only supported environment is MinGW (Cygwin and Visual builds are not supported). Use `./configure` then `make`, or the experimental Meson build. Cross-compiling from Unix with Autoconf: `./configure --host=i586-mingw32msvc`. The LDAP build option is not supported on Windows.

Running from the command line works as usual except that `-d` (daemonize) and `-u` (switch user) do not work.

As a service: set `service_name` in the config (default `pgbouncer`; `job_name` is an alias), then:

```
pgbouncer -regservice config.ini
```

Remove it with:

```
pgbouncer -unregservice config.ini
```

The usage page spells the switches `--regservice` and `--unregservice`, and the pgbouncer.exe form `pgbouncer.exe --regservice <pgbouncer.ini>`.

Event log: set `syslog = 1` in the config, after registering the library:

```
regsvr32 pgbevent.dll
```

and unregister with `regsvr32 /u pgbevent.dll`.

Other Windows differences from the config docs: logfile rotation requires stopping and starting the service; unix_socket_dir defaults to empty; unix_socket_mode and unix_socket_group are not supported; ulimit does not apply, so file descriptor limit advice is Unix-only.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: the Visual Studio wording (the page says Visual builds are unsupported generically).

Method: documentation only; no commands were run.
