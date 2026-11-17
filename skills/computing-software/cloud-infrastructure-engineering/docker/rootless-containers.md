---
id: computing-software.cloud-infrastructure-engineering.docker.rootless-containers
name: rootless-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, rootless, rootlesskit, dockerd-rootless, slirp4netns, vpnkit, user-namespace, newuidmap, newgidmap, subuid, subgid, podman-rootless, rootless-extras, cgroup-v2-delegation, systemd-user-service]
level: advanced
status: docs-checked
description: "Running dockerd itself without root: the rootless install, how networking and port <1024 binding actually work under it, and where it still falls short of a root daemon."
sources: ["https://docs.docker.com/engine/security/rootless/", "https://docs.docker.com/engine/security/rootless/tips/", "https://docs.docker.com/engine/security/rootless/troubleshoot/", "https://docs.docker.com/engine/security/rootless/uid-gid-mapping/", "https://docs.docker.com/engine/security/userns-remap/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rootless containers (rootless dockerd)

**Goal:** eliminate "anyone with `docker.sock` access is root on the host" at the source by
running the daemon itself as an unprivileged user — distinct from `userns-remap` (which
still runs `dockerd` as root and remaps container UIDs; see
`docker-daemon-configuration-and-hardening`). This is the daemon having no root at all.

## Install
```
curl -fsSL https://get.docker.com/rootless | sh
systemctl --user enable --now docker
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
```
Needs `/etc/subuid` and `/etc/subgid` entries for the user with at least 65,536 subordinate
UIDs/GIDs (the `dockerd-rootless-setuptool.sh install` script shows help when the prerequisites
are not met), and `newuidmap`/`newgidmap` on the host (the `uidmap` package on most
distributions). Rootless mode uses no SETUID or file-capability binaries except those two.

## How it actually isolates
`dockerd` runs entirely inside a user namespace created by `rootlesskit`: UID 0 inside the
namespace maps to the unprivileged host user, so a container "root" escape lands as that
user, not host root. Storage lives in `~/.local/share/docker` instead of `/var/lib/docker`,
so multiple rootless daemons (different users) coexist on one host without clobbering each
other — useful for shared dev boxes.

## Networking is the main cost
A user namespace can't create real network interfaces or iptables rules, so rootless Docker
tunnels all container networking through a user-mode TCP/IP stack: `slirp4netns` (the default when
installed), `pasta`, `VPNKit`, or `gvisor-tap-vsock` (the default when none of the others is installed).
The Docker docs rate this stack as slower than the kernel one. Set the RootlessKit network driver with
`DOCKERD_ROOTLESS_ROOTLESSKIT_NET`; the experimental `lxc-user-nic` driver avoids the user-mode stack but
needs a privileged helper configured in `/etc/lxc/lxc-usernet`. Benchmark your own workload.

## Binding privileged ports
Rootless containers can't bind host ports `<1024` directly. Either:
- `sudo setcap cap_net_bind_service=ep $(which rootlesskit)` once and restart the daemon, or
- set `net.ipv4.ip_unprivileged_port_start=0` in sysctl (host-wide), or
- run a reverse proxy on the host (as a normal privileged service) that forwards 443/80 to
  the rootless daemon's high ports.

## What still doesn't work (verify against your Docker version — this list shrinks over time)
- Only these storage drivers are supported: `overlay2` (kernel 5.11 or later), `fuse-overlayfs`
  (kernel 4.18 or later, with `fuse-overlayfs` installed), `btrfs` (kernel 4.18 or later, or a
  `user_subvol_rm_allowed` mount) and `vfs`.
- AppArmor, checkpoint, overlay networks and exposing SCTP ports are not supported (seccomp is).
- `--cap-add` capabilities apply only to resources governed by the container's user namespace, and
  a rootless daemon can't grant a container something it doesn't itself have.
- cgroup resource flags (`--memory`, `--cpus`, `--pids-limit`) work only with cgroup v2 and systemd;
  `docker info` showing `none` as Cgroup Driver means the flags are ignored, `systemd` means they
  work, and by default only the `memory` and `pids` controllers are delegated to users.

## When to actually use it
Shared multi-tenant dev/CI hosts where you can't trust every user with `docker.sock` root,
or any environment where "a compromised build step gets host root" is unacceptable and a
full VM-per-build is too expensive. Not generally recommended as the default for
single-tenant production hosts you already control at the OS level — the networking and
storage-driver costs buy you less there.

## Verify
`docker info` lists `rootless` under Security Options; inside a container, `cat /proc/self/uid_map`
shows the unprivileged host UID mapped, not a real 0.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main) Rootless mode, Tips, Troubleshooting and UID/GID mapping pages; Docker Engine API (SecurityOptions).
- Confirmed the install script URL, prerequisites (`newuidmap`/`newgidmap`, 65,536 subordinate IDs), the user namespace design, `~/.local/share/docker` data dir, the `setcap cap_net_bind_service=ep $(which rootlesskit)` and `net.ipv4.ip_unprivileged_port_start=0` options for privileged ports.
- Confirmed supported storage drivers and kernel gates, unsupported features (AppArmor, checkpoint, overlay networks, SCTP), cgroup v2 + systemd requirement and the `docker info` Cgroup Driver signals, the network driver list and defaults, and `DOCKERD_ROOTLESS_ROOTLESSKIT_NET`.
- Removed the tens-of-percent networking figure, the fuse-overlayfs speed claim and the `ps`/`cgroup.controllers` checks that no checked source covers.
Method: documentation only; no commands were run.
