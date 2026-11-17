---
id: computing-software.cloud-infrastructure-engineering.docker.choosing-userns-remap-vs-rootless
name: choosing-userns-remap-vs-rootless
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, user-namespaces, userns-vs-rootless, rootless, userns-remap, hardening, threat-model]
level: advanced
status: docs-checked
description: "Choose between userns-remap, rootless Docker and plain rootful Docker for a host: what each protects against, feature limits, operational cost, and typical fits."
sources: ["https://docs.docker.com/engine/security/userns-remap/", "https://docs.docker.com/engine/security/rootless/", "https://docs.docker.com/engine/security/rootless/troubleshoot/", "https://docs.docker.com/engine/security/rootless/tips/", "https://kubernetes.io/docs/concepts/workloads/pods/user-namespaces/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing userns-remap vs rootless

## What runs as root
| Mode | dockerd | containerd/runc | Container root |
|---|---|---|---|
| Rootful (default) | root | root | host root (constrained by caps, seccomp, AppArmor) |
| userns-remap | root | root | unprivileged host UID range from /etc/subuid (e.g. 231072+) |
| Rootless | your user | your user | your user's subordinate UIDs |

## Threats addressed
- **Container breakout via kernel or runtime bug**: both remap and rootless land the attacker
  as an unprivileged host user instead of root. Rootless additionally protects against bugs in
  the daemon itself.
- **docker.sock / API abuse**: only rootless helps: a rootful daemon (remapped or not) can still
  be told to run `--privileged --userns=host` containers by anyone with socket access.
  Rootless limits the blast radius to that user.

## Limitations
| | userns-remap | Rootless |
|---|---|---|
| `--privileged`, host namespaces | `--privileged`, `--pid=host`, `--network=host` need `--userns=host` for that container | `--cap-add` only applies inside the user namespace and grants no host privileges |
| Ports < 1024 | Not listed as a limitation | Needs `net.ipv4.ip_unprivileged_port_start` sysctl or CAP_NET_BIND_SERVICE on `rootlesskit` |
| Networking | Not listed as a limitation | User-mode TCP/IP stack is slower; `-p` does not propagate source IPs by default |
| Resource limits | Normal | cgroup v2 + systemd required; only memory and pids are delegated by default |
| Storage drivers | External volume/storage drivers must understand the mappings | `overlay2` (kernel 5.11+), `fuse-overlayfs` (kernel 4.18+), `btrfs`, `vfs` |
| AppArmor | Supported | Not supported |
| Bind mount ownership | Container UID n is host subuid + n | Container root is your UID; UID n>=1 is subuid + (n - 1) |
| Multi-user host | One remap user/range for the daemon | One daemon per user |
| Existing images/containers | Masked: stored under `/var/lib/docker/<uid>.<gid>/` | Separate per-user data dir (`~/.local/share/docker`) |

## Typical fits
- **CI runners / shared build hosts / developer laptops**: rootless (socket access is the
  real risk).
- **Single-tenant production servers with ops tooling needing host access**: rootful with
  userns-remap, opting out a few trusted services.
- **Kubernetes nodes**: neither via Docker; Kubernetes pods opt in to user namespaces with
  `pod.spec.hostUsers: false` (containerd 2.0+ or CRI-O 1.25+ per the Kubernetes docs).
- **Need `--privileged` workloads (DinD, system agents)** regularly: rootful, isolate the host.

## Combining
Rootless already implies a user namespace; userns-remap does not apply to rootless daemons.
Both modes still benefit from seccomp, dropped capabilities, read-only rootfs and
no-new-privileges.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: userns-remap, Rootless mode, UID/GID mapping, Rootless tips and troubleshooting pages), Kubernetes docs (user namespaces page).
- Confirmed the daemon still runs as root with userns-remap, the `--privileged`/`--pid=host`/`--network=host` limits and the `--userns=host` opt-out, masked existing images, the UID mapping formulas for both modes, the 231072 example range, and that `userns-remap` does not apply to rootless.
- Confirmed rootless storage drivers and kernel gates (overlay2 5.11+, fuse-overlayfs 4.18+, btrfs, vfs), AppArmor unsupported, cgroup v2 + systemd for resource limits (memory and pids delegated by default), privileged-port sysctl or `setcap` on `rootlesskit`, the user-mode network stack and source-IP default.
- Confirmed `pod.spec.hostUsers` and the containerd 2.0 / CRI-O 1.25 minimums in the Kubernetes docs.
- Removed unsourced "native networking", "overlay2 only" and CI-fit performance claims.
Method: documentation only; no commands were run.
