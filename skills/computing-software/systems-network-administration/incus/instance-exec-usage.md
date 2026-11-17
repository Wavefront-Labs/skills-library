---
id: computing-software.systems-network-administration.incus.instance-exec-usage
name: instance-exec-usage
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, exec, interactive, non-interactive, environment, user, cwd, shell]
level: practitioner
status: docs-checked
description: "Run commands in Incus instances with incus exec: interactive vs non-interactive mode, --user/--group/--cwd, environment variables and their defaults, opening a shell."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/instance-exec.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# incus exec

`incus exec <instance> -- <command>` needs no network access. Containers always work; VMs need `incus-agent` running.

Modes:
- Interactive (PTS) is chosen automatically on a terminal; force with `--force-interactive` or `--mode interactive`.
- Non-interactive (separate pipes, for scripts): `--force-noninteractive` or `--mode non-interactive`.

Identity: Incus does not read `/etc/passwd`, `/etc/group` or nsswitch in the instance, so it does not know home directories or supplementary groups. Default is UID 0, GID 0, cwd `/root`. Override with absolute values `--user`, `--group`, `--cwd`.

Environment:
- Persistent: `incus config set <instance> environment.ENVVAR=value`.
- Per session: `--env ENVVAR=VALUE`.
- Defaults: `PATH` (standard directories, plus `/snap` and `/etc/NIXOS` where applicable), `LANG=C.UTF-8`, `HOME=/root` and `USER=root` when root.

Shells: `incus exec <instance> -- /bin/bash` (root); other user: `incus exec <instance> -- su --login <user>`. Leave with `exit` or `Ctrl`+`d`.

## Checked

2026-11-04: confirmed against the Incus run-commands page (execution modes and flags, no parsing of passwd/group/nsswitch, root and `/root` defaults, `--user`/`--group`/`--cwd`, environment options and default variables, shell examples). Nothing removed.

Method: documentation only; no commands were run.
