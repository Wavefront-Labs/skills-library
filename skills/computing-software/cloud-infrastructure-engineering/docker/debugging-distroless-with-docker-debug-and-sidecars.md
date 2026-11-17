---
id: computing-software.cloud-infrastructure-engineering.docker.debugging-distroless-with-docker-debug-and-sidecars
name: debugging-distroless-with-docker-debug-and-sidecars
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-debug, debug-container, ephemeral-debug, docker-debug-cli, debug-shell, cdebug, pid-container, shared-pid-namespace, network-container-join, netshoot, netshoot-usage, netshoot-sidecar, static-busybox, busybox-static]
level: advanced
description: "Get a shell and tools next to a shell-less container: docker debug, cdebug, sidecars sharing --pid/--network=container:, netshoot, and copying in a static busybox."
sources: ["https://docs.docker.com/reference/cli/docker/debug/", "https://github.com/iximiuz/cdebug", "https://github.com/nicolaka/netshoot", "https://docs.docker.com/reference/cli/docker/container/run/", "https://github.com/compose-spec/compose-spec/blob/main/spec.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging distroless containers

`docker exec -it app sh` -> `executable file not found`: no shell, no tools. Options,
from least to most invasive:

## 1. docker debug
```sh
docker debug app                 # shell with a toolbox (nix-based), sees app's FS at /
docker debug app --shell bash
docker debug <image>             # works on images and stopped containers too
```
- Brings its own toolbox (vim, nano, htop, curl, ...); the built-in `install <tool>` adds
  Nix packages, and `/nix` is never visible to the target. Shells supported: bash, fish, zsh.
- For images and stopped containers all changes are discarded when you leave the shell. For
  running or paused containers, filesystem changes **are** directly visible to the container.
- `--host` points it at a remote daemon (`ssh://...` or a unix socket).

## 2. cdebug (open source equivalent)
```sh
cdebug exec -it app                         # busybox shell in app's namespaces
cdebug exec -it --image nicolaka/netshoot app
cdebug exec --privileged -it app            # if the default fails with "Permission denied"
```
cdebug's default debugger image is `busybox:musl`; it starts the debugger with the same
privileges as the target, so non-privileged targets can fail until you add `--privileged`.
The target's root filesystem is reachable at `/proc/1/root` from the debug shell.
Kubernetes equivalent: `kubectl debug -it pod/app --image=busybox --target=app`.

## 3. Sidecar sharing namespaces (plain Docker)
```sh
# processes: see and signal app's processes, read its FS via /proc/<pid>/root
docker run --rm -it --pid=container:app --cap-add SYS_PTRACE busybox sh
  ps; ls /proc/1/root/etc
# network: same interfaces, localhost, ports
docker run --rm -it --network=container:app nicolaka/netshoot
# both
docker run --rm -it --pid=container:app --network=container:app nicolaka/netshoot
```
netshoot also runs on the host network: `docker run --rm -it --net host nicolaka/netshoot`.
The `docker run` reference's own PID-sharing example adds `--cap-add SYS_PTRACE` and
`--security-opt seccomp=unconfined` for strace. Compose sidecar for networking:
`network_mode: "service:app"` (the spec lists `service:{name}` as a value).

## 4. Copy a static busybox in
```sh
docker cp $(docker create busybox:musl):/bin/busybox ./busybox
docker cp ./busybox app:/tmp/busybox
docker exec -it app /tmp/busybox sh
```
Needs a writable path in the container. Remove the copy afterwards; it changes the container.

## Verify
In the sidecar `ps` shows the app as PID 1; `ls /proc/1/root/app` lists its files;
`curl localhost:<port>` reaches the app.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23), `docker debug` and `docker container run` reference data; iximiuz/cdebug README; nicolaka/netshoot README; compose-spec `network_mode`. Confirmed: docker debug behaviour and toolbox, `--shell`/`--host`, cdebug default image and `--privileged` fix, `--pid=container:` and `--net container:` forms, netshoot host-network usage. Removed as unconfirmed: the subscription-tier claim, "tools persist across sessions", the compose `pid: service:` form, `/proc/<pid>/environ` and tcpdump/dig examples, the privilege gotcha for `/proc/1/root`, the busybox volume-copy line, read-only rootfs advice.
Method: documentation only; no commands were run.
