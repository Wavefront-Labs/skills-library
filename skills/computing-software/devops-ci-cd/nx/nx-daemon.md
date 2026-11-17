---
id: computing-software.devops-ci-cd.nx.nx-daemon
name: nx-daemon
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, daemon, nx-daemon, usedaemonprocess, nx-socket-dir, containers, ci]
level: practitioner
status: docs-checked
description: "Control and debug the Nx Daemon: disable with useDaemonProcess or NX_DAEMON, read logs with nx daemon, relocate sockets with NX_SOCKET_DIR, container and CI defaults."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-daemon.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand when the daemon runs and how to turn it off, inspect it, or fix socket problems.

The daemon is a per-workspace background process that watches files and keeps the project graph in memory so commands update it incrementally. It uses a Unix socket on macOS/Linux and a named pipe on Windows, and shuts down after 3 hours without requests or file changes. `nx reset` stops it and clears other workspace state.

Disable:
```jsonc
// nx.json
{ "useDaemonProcess": false }
```
or per command/environment: `NX_DAEMON=false nx show projects`. The environment variable wins over `nx.json`. Nx disables the daemon by default in CI and containers; set `NX_DAEMON=true` to opt in on a long-lived environment. It cannot run in WebAssembly environments. In AI agent sandboxes the sandbox must allow the unix sockets.

Logs: `nx daemon` prints the PID and log file path; then `tail -f <daemon-log-path>`.

Socket directory (macOS/Linux): Nx tries `/tmp/.nx/<uid>/sockets`, then `~/.nx/sockets`, then a directory inside the workspace (last resort; deep checkouts may exceed socket path length, and Nx warns once). `NX_SOCKET_DIR=<your-directory> nx daemon` replaces that list entirely with no fallback (falls to the workspace dir with a warning if unusable, errors if refused). It takes precedence over older `NX_DAEMON_SOCKET_DIR`. The directory must be reachable only by your user; Nx rejects the system temp directory and its own container and cache roots.

Security: the socket is effectively remote code execution inside the daemon. Never point it at a shared or world-writable directory.

Containers: enable only in persistent dev containers; volume mounts can disturb file watching, restarts invalidate the socket, permission differences can block it. One daemon per container; never mount one socket directory into several.

## Checked

2026-11-07. Confirmed: the daemon lifetime, NX_DAEMON / useDaemonProcess, NX_SOCKET_DIR fallback order and container notes against the Nx daemon page. Removed: an invented Verify step.

Method: documentation only; no commands were run.
