---
id: computing-software.networking-hardware-and-wireless.apache-httpd.httpd-command-line-options
name: httpd-command-line-options
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, httpd, cli, configtest, vhosts, modules, debug]
level: practitioner
status: docs-checked
description: "Use the httpd binary options to test config, dump vhosts and modules, override files and directives, and run in foreground debug mode."
sources:
  - https://httpd.apache.org/docs/2.4/programs/httpd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# httpd command-line options
Normally invoke httpd through `apachectl` on Unix.

## Config and paths
- `-d serverroot` sets the initial ServerRoot; `-f file` picks the config file (relative to ServerRoot).
- `-C directive` runs a directive before the config files; `-c directive` after.
- `-D name` defines a name for `<IfDefine>`; it also enables `-DNO_DETACH` and `-DFOREGROUND`.

## Inspect and test
- `-t` syntax check only: exit 0 for Syntax OK.
- `-S` shows parsed settings (currently virtual hosts).
- `-M` lists loaded static and shared modules; `-l` only compiled-in ones; `-L` lists directives with contexts.
- `-t -D DUMP_VHOSTS` and `-t -D DUMP_MODULES` print vhost and module configuration.
- `-v` / `-V` print version / build settings.

## Startup and signals
- `-e level` sets LogLevel during startup; `-E file` writes startup errors to a file.
- `-X` runs debug mode with one worker, not detached.
- `-T` skips the document root check.
- `-k start|restart|graceful|stop|graceful-stop` signals the server.

```
httpd -t -D DUMP_VHOSTS
httpd -e debug -E /path/to/start.log
```

## Checked

2026-11-08. Every option listed (-d, -f, -C, -c, -D with NO_DETACH and FOREGROUND, -t with DUMP_VHOSTS and DUMP_MODULES, -S, -M, -l, -L, -v, -V, -e, -E, -X, -T, -k values) and the advice to use apachectl confirmed against the httpd program page.

Method: documentation only; no commands were run.
