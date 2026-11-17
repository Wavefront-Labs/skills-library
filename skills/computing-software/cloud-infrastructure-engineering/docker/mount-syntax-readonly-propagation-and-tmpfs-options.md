---
id: computing-software.cloud-infrastructure-engineering.docker.mount-syntax-readonly-propagation-and-tmpfs-options
name: mount-syntax-readonly-propagation-and-tmpfs-options
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volumes, bind-mount, tmpfs, mount-flag, v-flag, mount-syntax, readonly-mount, ro-mount, bind-propagation, rshared, tmpfs-size, tmpfs-mode]
level: practitioner
description: "Choose --mount over -v, mount read-only (including recursive read-only), set bind propagation for nested mounts, and size tmpfs mounts with mode and size."
sources: ["https://docs.docker.com/engine/storage/bind-mounts/", "https://docs.docker.com/engine/storage/tmpfs/", "https://docs.docker.com/engine/storage/volumes/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mount syntax, read-only, propagation and tmpfs options

## --mount vs -v
```sh
-v data:/var/lib/app                 # named volume
-v "$PWD/conf:/etc/app:ro"           # bind (path starts with / or .)
--mount type=volume,src=data,dst=/var/lib/app
--mount type=bind,src="$PWD/conf",dst=/etc/app,readonly
--mount type=tmpfs,dst=/run,tmpfs-size=64m,tmpfs-mode=1770
```
Key difference: with `-v`, a **missing host path is automatically created** (always as a
directory); with `--mount type=bind` Docker errors (`bind source path does not exist`) unless
`bind-create-src` is set. Typos in `-v` give you an app staring at an empty dir. Prefer
`--mount`, which is more explicit and supports all options.

## Read-only
```sh
--mount type=bind,src=/etc/ssl/certs,dst=/etc/ssl/certs,readonly
-v certs:/certs:ro
--mount type=bind,src=/mnt,dst=/mnt,readonly,bind-recursive=readonly
```
Submounts under a bind source are included in the bind mount by default. For a read-only bind
mount, Docker makes a best-effort attempt to make submounts read-only too (`bind-recursive=enabled`,
the default), which needs Linux kernel 5.12 or later; on older kernels submounts stay read-write.
`bind-recursive=readonly` requires kernel 5.12+ and errors otherwise. Values: `enabled`,
`disabled`, `writable`, `readonly`. `bind-recursive` works only with `--mount`.

## Bind propagation
Controls whether mounts created **after** the container starts, under the bind source or
target, are visible on the other side.
| Mode | Host -> container | Container -> host |
|---|---|---|
| `rprivate` (default) | no | no |
| `rslave` | yes | no |
| `rshared` | yes | yes |
```sh
--mount type=bind,src=/mnt/disks,dst=/mnt/disks,bind-propagation=rslave
```
Use `rslave` when a container should see mounts added later under the source. The host
filesystem must already support bind propagation before you set it on a mount point.
Mount propagation does not work with Docker Desktop.

## tmpfs options
```sh
--tmpfs /tmp:rw,noexec,nosuid,size=128m
--mount type=tmpfs,dst=/var/cache/nginx,tmpfs-size=64m,tmpfs-mode=1777
```
- If `tmpfs-size` is unset the default maximum is 50% of the host's total RAM, and tmpfs
  usage counts against the container's memory limit, so filling it can OOM the container - set a
  size.
- `--tmpfs` takes mount options such as `noexec`, `nosuid`, `size`, `mode`, `uid`, `gid`;
  `--mount type=tmpfs` uses `tmpfs-size` and `tmpfs-mode`. `--tmpfs` cannot be used with swarm
  services; use `--mount`.
- Mode default 1777. Contents vanish on stop; tmpfs mounts cannot be shared between containers.

## Verify
`docker inspect -f '{{json .Mounts}}' app` shows type, RW and propagation;
`docker exec app sh -c 'touch /etc/app/x'` fails with read-only file system.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine storage docs (docker/docs main).
Confirmed against the bind mounts, tmpfs and volumes pages: `-v` auto-creates a missing host directory while
`--mount` errors (and `bind-create-src`), `bind-recursive` values and the kernel 5.12 requirement, propagation
modes and default `rprivate`, Docker Desktop not supporting propagation, `--tmpfs` option list, `tmpfs-size`
default of 50% of host RAM, `tmpfs-mode` default 1777, tmpfs counting against the memory limit, `--tmpfs` not usable
with swarm services. Removed: the root-owned claim, the Engine 25 gate, the `--tmpfs` default-flags claim
(noexec/nosuid/nodev), the findmnt commands and the unlisted-use-case advice.

Method: documentation only; no commands were run.
