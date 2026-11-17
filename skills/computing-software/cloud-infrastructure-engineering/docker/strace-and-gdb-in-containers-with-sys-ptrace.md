---
id: computing-software.cloud-infrastructure-engineering.docker.strace-and-gdb-in-containers-with-sys-ptrace
name: strace-and-gdb-in-containers-with-sys-ptrace
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, sys-ptrace, strace-container, gdb, gdbserver, ptrace, yama-ptrace-scope, seccomp, perf, debugging, pid-namespace]
level: advanced
status: docs-checked
description: "Trace and debug processes in containers: why strace -p fails, adding SYS_PTRACE, tracing from the host or a sidecar sharing the PID namespace, gdb/gdbserver attach, perf."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/engine/security/seccomp/", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/LSM/Yama.rst", "https://man7.org/linux/man-pages/man7/capabilities.7.html", "https://github.com/strace/strace/blob/master/doc/strace.1.in"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# strace and gdb in containers (SYS_PTRACE)

**Goal:** attach `strace`/`gdb` to a process inside a container, on a running production
container if possible, without rebuilding it as privileged.

## Why `strace -p 1` fails with "Operation not permitted"
- Docker's default capability set does **not** include `CAP_SYS_PTRACE`.
- On hosts with Yama `kernel.yama.ptrace_scope=1` (Ubuntu default) a process may only trace
  its own descendants unless it has `CAP_SYS_PTRACE`. A shell from `docker exec` is not an
  ancestor of PID 1, so attach fails. Starting the program *under* strace (`strace -f ./app`)
  works without the capability.
- The default seccomp profile blocks `ptrace` on Linux kernels before 4.8 (to avoid a seccomp bypass) and
  otherwise leaves it to the capability: tracing arbitrary processes is gated by `CAP_SYS_PTRACE`.

## Option A: recreate with the capability (dev/staging)
```bash
docker run --cap-add SYS_PTRACE --name app myimage
# compose:  cap_add: [SYS_PTRACE]
docker exec -it app strace -f -tt -e trace=network,file -p 1
```
Capabilities cannot be added to a running container.

## Option B: debug sidecar sharing the PID namespace (no restart)
```bash
docker run --rm -it --pid=container:app --cap-add SYS_PTRACE ubuntu:24.04 \
  sh -c 'apt-get update -qq && apt-get install -yqq strace && strace -f -p 1'
```
`--pid=container:<name|id>` joins another container's PID namespace; the Docker `docker run` reference
uses this pattern to run `strace` from an Alpine container against another container. The target image
need not contain strace or gdb. (The reference example also passes `--security-opt seccomp=unconfined`;
on current kernels the default profile allows `ptrace` once `SYS_PTRACE` is added.)

## Option C: from the host
```bash
PID=$(docker inspect -f '{{.State.Pid}}' app)
sudo strace -f -p "$PID"
```
Host root has all capabilities; the PID differs from the in-container PID. `strace -p` attaches to a
process id and `-f` follows forks (strace(1)).

## perf
`perf_event_open` is not allowed by the default seccomp profile unless the container holds `CAP_SYS_ADMIN`
or `CAP_PERFMON` (the profile's `includes.caps` rules); `CAP_PERFMON` exists since Linux 5.8
(capabilities(7)). Adding the capability is the supported way; otherwise profile from the host.

## Gotchas
- `strace -f` slows the traced process; filter with `-e trace=` (for example `%network`, `%file`) and
  detach quickly in production.
- Remove `SYS_PTRACE` again after debugging; the Docker docs describe dropping it as what blocks
  tracing arbitrary processes.

## Verify
```bash
docker run --rm -it --pid=container:app --cap-add SYS_PTRACE ubuntu:24.04 \
  sh -c 'apt-get update -qq && apt-get install -yqq strace && strace -c -p 1'
# interrupt after a few seconds: -c prints a syscall summary table
```

## Checked
Date: 2026-10-24. Documentation: Docker docs `docker run` reference (PID namespace join example) and seccomp page (docker/docs main), Linux kernel Yama documentation, man-pages capabilities(7), strace manual page source, moby/profiles default.json.
- Confirmed `CAP_SYS_PTRACE` is not in Docker's default set, Yama `ptrace_scope` restricts tracing to descendants unless the tracer has `CAP_SYS_PTRACE`, the seccomp `ptrace` row (blocked before kernel 4.8, otherwise gated by the capability), `--pid=container:<name|id>` with `--cap-add SYS_PTRACE` and `strace`, `strace -p`, `-f`, `-c` and `-e trace=%network|%file`, and `CAP_PERFMON` since Linux 5.8.
- Confirmed in default.json that `perf_event_open` is allowed only with `CAP_SYS_ADMIN` or `CAP_PERFMON`.
- Removed `docker debug`, nicolaka/netshoot, gdb/gdbserver, `nsenter`, JVM slowdown and `dmesg` claims that no checked source covers; the debian image tag was replaced by `ubuntu:24.04` used in the Docker docs.
Method: documentation only; no commands were run.
