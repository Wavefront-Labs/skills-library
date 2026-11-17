---
id: computing-software.cloud-infrastructure-engineering.docker.capturing-core-dumps-from-containers
name: capturing-core-dumps-from-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, core-dump, ulimit-core, core-pattern, systemd-coredump, coredumpctl, gdb, crash-analysis, segfault]
level: advanced
status: docs-checked
description: "Get usable core dumps when a containerised process crashes: host-global core_pattern, --ulimit core, writing cores to a volume, systemd-coredump, and analysing with gdb."
sources: ["https://man7.org/linux/man-pages/man5/core.5.html", "https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/compose-file/services/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capturing core dumps from containers

**Goal:** when a native process in a container segfaults, end up with a core file and the
exact binary + libraries to load it in a debugger.

## Where the core goes: `core_pattern`
`/proc/sys/kernel/core_pattern` decides the core file name or handler (see core(5)). Set it on the
host, not from inside the container. Two cases:
- **Pipe** (the pattern starts with `|`, for example the `systemd-coredump` line on systemd hosts):
  the handler runs in the **initial namespaces**, not the crashing process's, so the core is
  handled on the host side (`coredumpctl list` on systemd hosts), not inside the container.
  core(5): `RLIMIT_CORE` is not enforced for cores piped to a program.
- **Path** (for example `/cores/core.%e.%p.%t`): core(5) says paths are interpreted using the
  crashing process's mount namespace, working directory and root directory, so the file is written
  **inside the container's filesystem** and is lost with the container unless that path is a
  volume. Template codes used here: `%e` command name, `%p` PID, `%t` time of dump in seconds
  since the Epoch.

## Recipe A: cores into a volume
```bash
# host: set the pattern (persist it with your distro's sysctl.d mechanism)
echo '/cores/core.%e.%p.%t' | sudo tee /proc/sys/kernel/core_pattern

docker run -d --name app --ulimit core=-1 -v cores:/cores myimage
```
```yaml
# compose
services:
  app:
    ulimits: { core: -1 }
    volumes: [cores:/cores]
```
The directory must exist and be writable by the container user. `--ulimit` takes
`<type>=<soft>[:<hard>]`; `core` is the maximum size of core files (`RLIMIT_CORE`). With no value
given, limits are inherited from the daemon's default ulimits.

## Recipe B: systemd-coredump on the host
On systemd hosts the default pattern pipes cores to `systemd-coredump`, which stores them under
`/var/lib/systemd/coredump/` (typically compressed); `coredumpctl` lists and extracts them.
Because the limit is not enforced for piped dumps, `--ulimit core` is not what decides whether a
piped core is written; check the systemd-coredump documentation for its own size limits.

## Analysing
Load the core with the **same image** (binary and libraries must match), in a debugger such as gdb.
Use a debug build or separate debug symbols from the same build; a stripped binary gives addresses only.

## Gotchas
- Docker Desktop: the "host" kernel is inside its VM, so the pattern must be set there.
- Disk: cores of multi-GB processes fill a volume quickly; rotate them.
- Cores contain process memory (secrets, customer data); treat them as sensitive.

## Checked
Checked 2026-10-28 against core(5) (pipe handler namespaces, `RLIMIT_CORE` not enforced for piped
dumps, path interpretation, `%e` `%p` `%t`, systemd storage directory), Docker Docs (`docker run
--ulimit` format, `core` type, daemon-default inheritance) and the Compose `ulimits` reference.
Corrected: the earlier advice to raise `--ulimit core` for the piped systemd case contradicts core(5).
Removed as unconfirmed: the Apport behaviour, `coredump.conf` key names and default sizes, the
`default-ulimits` daemon.json snippet, language-runtime flags (Go, Node, JVM), the gdb command line,
the nsenter recipe for Docker Desktop and the `/proc/sys` read-only claim. systemd.io manual page
was unreadable (stub), so no systemd limits are stated.
Method: documentation only; no commands were run.
