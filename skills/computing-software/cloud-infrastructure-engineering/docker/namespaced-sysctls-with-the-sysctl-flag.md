---
id: computing-software.cloud-infrastructure-engineering.docker.namespaced-sysctls-with-the-sysctl-flag
name: namespaced-sysctls-with-the-sysctl-flag
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, sysctl-flag, net-sysctl, namespaced-sysctls, somaxconn, ip-unprivileged-port-start, ipc-sysctls, compose-sysctls, kernel-tuning]
level: advanced
status: docs-checked
description: "Tune kernel parameters per container with --sysctl: which net.* and IPC sysctls are namespaced, common settings, host-only ones like vm.max_map_count, Compose and Swarm syntax."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/compose-file/services/", "https://docs.docker.com/reference/cli/docker/service/create/", "https://github.com/moby/moby/blob/master/daemon/oci_linux.go", "https://kubernetes.io/docs/tasks/administer-cluster/sysctl-cluster/", "https://github.com/moby/moby/blob/master/api/swagger.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Namespaced sysctls with --sysctl

Containers cannot write `/proc/sys` at runtime (it is mounted read-only), so kernel tuning
happens at container creation with `--sysctl`, and only for parameters the kernel
**namespaces**.

## What Docker accepts
- **IPC namespace**: `kernel.msgmax`, `kernel.msgmnb`, `kernel.msgmni`, `kernel.sem`,
  `kernel.shmall`, `kernel.shmmax`, `kernel.shmmni`, `kernel.shm_rmid_forced`, `fs.mqueue.*`.
  Not allowed with `--ipc=host`.
- **Network namespace**: `net.*`. Not allowed with `--network=host` (that would change the
  host).
- Everything else is not supported: Docker does not support changing sysctls inside a container
  that also modify the host system (for example `vm.*`). Set those on the **host**.

Not all sysctls are namespaced, and the Docker docs expect more to become namespaced as the kernel
evolves; if a container fails to start with a sysctl, check that the kernel namespaces it.

## Common per-container settings
```bash
docker run \
  --sysctl net.core.somaxconn=4096 \
  --sysctl net.ipv4.ip_local_port_range="10240 65000" \
  --sysctl net.ipv4.tcp_keepalive_time=300 \
  --sysctl net.ipv4.ip_unprivileged_port_start=0 \
  nginx
```
- `net.ipv4.ip_unprivileged_port_start=0`: bind :80 as non-root without `NET_BIND_SERVICE`. The daemon
  already sets it to 0 for containers with a private network namespace (Engine source,
  `daemon/oci_linux.go`).
- `net.*` keys such as `net.core.somaxconn` and `net.ipv4.ip_forward` are accepted because the whole
  `net.*` family is allowed in a private network namespace.
- `kernel.shmmax` / `kernel.shmall`: IPC-namespaced, accepted unless `--ipc=host`.

## Compose and Swarm
```yaml
services:
  proxy:
    sysctls:
      net.core.somaxconn: 4096
      net.ipv4.tcp_keepalive_time: 300
```
```bash
docker service create --sysctl net.core.somaxconn=4096 --name proxy nginx   # Swarm services
```
Kubernetes classes sysctls as safe or unsafe; unsafe sysctls are disabled by default and must be allowed
by the cluster admin per node, which matters when migrating.

## Host-only parameters that apps ask for
Applications that ask for `vm.*` or `fs.*` sysctls (for example `vm.max_map_count`) need them set on the
host, not with `--sysctl`; check each application's documentation for the value. On Docker Desktop the
"host" is the Docker VM.

## Verify
```bash
docker exec proxy sysctl net.core.somaxconn
docker inspect -f '{{json .HostConfig.Sysctls}}' proxy
```

## Checked
Date: 2026-10-24. Documentation: Docker docs `docker run` reference (sysctl section), Compose services reference, `docker service create` reference (docker/docs main); moby/moby `daemon/oci_linux.go`; Kubernetes sysctl page; Docker Engine API (HostConfig.Sysctls).
- Confirmed the supported namespaced sysctls: IPC (`kernel.msgmax`, `kernel.msgmnb`, `kernel.msgmni`, `kernel.sem`, `kernel.shmall`, `kernel.shmmax`, `kernel.shmmni`, `kernel.shm_rmid_forced`, `fs.mqueue.*`, not with `--ipc=host`) and `net.*` (not with `--network=host`), the host-modification caveat, Compose `sysctls` array and map forms, `docker service create --sysctl`, and `HostConfig.Sysctls`.
- Confirmed the daemon default `net.ipv4.ip_unprivileged_port_start=0` and the Kubernetes safe/unsafe sysctl split.
- Removed the quoted error text, per-sysctl tuning explanations, the application host-sysctl table and the Docker Desktop shell commands, none of which a checked source covers.
Method: documentation only; no commands were run.
