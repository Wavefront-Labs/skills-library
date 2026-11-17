---
id: computing-software.software-engineering.php.php-xdebug-debugging
name: php-xdebug-debugging
category: computing-software
field: software-engineering
product: php
tags: [php, xdebug-debugging, debugging]
level: practitioner
status: docs-checked
description: "Set up Xdebug 3 step debugging: modes, client_host and client_port, triggers, remote and Docker hosts, and logging."
sources: ["https://xdebug.org/docs/step_debug"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with Xdebug

Xdebug talks to an IDE over the DBGp protocol. Xdebug initiates the connection to the IDE, not the other way round, so the IDE must be listening and reachable.
```ini
; php.ini or 99-xdebug.ini (xdebug.mode cannot be set in .htaccess, .user.ini or php_admin_value)
xdebug.mode=debug              ; off, develop, coverage, debug, gcstats, profile, trace; combine with commas
xdebug.start_with_request=trigger   ; default for debug mode: start only when a trigger is present
xdebug.client_host=localhost   ; default; the machine where the IDE listens
xdebug.client_port=9003        ; default, shared by Xdebug and the CLI client
xdebug.log=/tmp/xdebug.log     ; absolute path the PHP user can write
```
Triggers (with `start_with_request=trigger`): `XDEBUG_TRIGGER` in the environment, GET/POST or a cookie; the legacy `XDEBUG_SESSION` name also works for step debugging.
```sh
export XDEBUG_SESSION=1        # CLI (Unix); on Windows: set XDEBUG_SESSION=1
php myscript.php               # or vendor/bin/phpunit
```
For web requests use a browser extension that sets the cookie (Xdebug Helper for Firefox, Chrome and Edge; XDebugToggle for Safari), or pass `XDEBUG_SESSION=name` as a GET/POST parameter for one request. `XDEBUG_SESSION_START=name` sets the session cookie and `XDEBUG_SESSION_STOP` removes it. `XDEBUG_IGNORE` set to any value other than `no` or `0` suppresses a trigger. Set `xdebug.trigger_value` to require a specific value (comma-separated list allowed from Xdebug 3.1).

## Remote and Docker
- If PHP runs in a container or on another machine, set `xdebug.client_host` to the IDE machine and make sure the port is not blocked by a firewall. On Linux `xdebug://gateway` (system network gateway) and `xdebug://nameserver` are also accepted; `xdebug_info()` shows whether they are available.
- `xdebug.discover_client_host=1` connects back to the address in the HTTP request headers; it has no filter, so anybody who can reach the web server can start a session. It does not apply to the CLI.
- Configure IDE path mappings from container paths to local paths. The log's `<init>` message lists the `fileuri` entry point to compare with breakpoint paths.

## Troubleshooting
- `xdebug.log` records connection attempts and failures; `xdebug.log_level` 0 to 10 sets verbosity (7 is the default). Under systemd the real `/tmp` path may differ for services such as Apache.
- `xdebug_info()` shows active modes and diagnostic warnings; `xdebug_info('mode')` (Xdebug 3.1+) returns the enabled modes.
- `xdebug.connect_timeout_ms` defaults to 200; raise it on slow networks, but requests then hang when no IDE listens.
- `xdebug_break()` forces a breakpoint; `xdebug.start_upon_error=yes` starts a session on a notice, warning or throwable.

## Gotchas
- `XDEBUG_MODE` in the environment overrides `xdebug.mode` (PHP-FPM's `clear_env` must be off for that). `off` gives close to zero overhead; use it where debugging is not needed, and load only the modes you need.
- Port 9003 is the default; leave it unless you have a reason.

Verify: call `xdebug_info('mode')` or view `xdebug_info()` output to confirm `debug`, then hit a breakpoint with `XDEBUG_SESSION=1`.

## Checked

Date: 2026-11-08. Read in full: the Xdebug step debugging page including its settings and function reference. Removed: the default-port history (9000), `host.docker.internal` and `--add-host` Docker advice, `php --ri xdebug`, the PCOV comparison, the max_nesting_level and Composer-warning statements, and the unread install page source, as none appear on the page read.

Method: documentation only; no commands were run.
