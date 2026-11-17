---
id: computing-software.networking-hardware-and-wireless.haproxy.config-check-and-reload
name: config-check-and-reload
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, config-check, reload, sigusr2, master-worker, hard-stop-after]
level: practitioner
status: docs-checked
description: "Validate HAProxy configuration with haproxy -c and reload safely in master-worker mode so old workers finish their connections."
sources:
  - https://docs.haproxy.org/3.0/management.html
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# config check and reload
Always check before reload: `haproxy -c -f /etc/haproxy/haproxy.cfg`. `-c` checks the configuration and exits before binding; the exit status is zero if everything is OK and non-zero on error, warnings are reported, and a success message is printed only with `-V` ("Configuration file is valid"). Scripts must use the exit status.

`-f` accepts several files or a directory: a directory adds only its files with a `.cfg` extension that are not hidden, in lexical order. Each file must start on a section boundary (`global`, `defaults`, `frontend`...). A single `--` before many file names works like repeated `-f`.

`-W` runs master-worker mode (`-Ws` adds systemd `notify` support, when built with `USE_SYSTEMD`). In that mode sending SIGUSR2 to the master reloads: it re-executes itself with `-sf` and the worker PIDs, parses the configuration and forks new workers, while old workers finish their connections. Service scripts verify the file with `haproxy -c` before reloading, so a bad config should not replace running workers.

Set `hard-stop-after <time>` in `global` (default unit milliseconds) so an old worker is stopped after a soft stop even if connections remain open (long TCP sessions, websockets). `show proc` on the master CLI lists the master, workers and `old workers`; a long-lived old worker means clients still hold connections.

Listening sockets can be passed to the new process with `-x` (in master-worker mode the master does it automatically on reload), so no connection is missed on Linux (see seamless-reload-and-listener-fd-passing).

Verify: after reload, `show info` on the runtime socket reports `Pid` and `Uptime`, and `show proc` shows the new worker with a fresh uptime.

## Checked
2026-11-03. Confirmed against management.html (command-line options `-c`, `-f`, `--`, `-W`, `-Ws`, `-x`, `-V`; SIGUSR2 reload in master-worker mode; `show proc`; `show info` fields Pid and Uptime) and configuration.html (`hard-stop-after`). Fixed: the directory rule (only `.cfg`, lexical order). Removed: exit code 2 with `-dW`, the systemd `ExecReload` line, `systemctl restart/reload` details and journalctl commands (unit files are distribution-specific and not in the docs), the "confirm" marker and the grep pipe; the `30m` example value.
Method: documentation only; no commands were run.
