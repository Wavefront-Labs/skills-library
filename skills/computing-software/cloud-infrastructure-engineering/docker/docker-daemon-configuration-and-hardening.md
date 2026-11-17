---
id: computing-software.cloud-infrastructure-engineering.docker.docker-daemon-configuration-and-hardening
name: docker-daemon-configuration-and-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerd, daemon-json, docker-socket, docker-sock, tls, mtls, dockerd-tls, icc, inter-container-communication, userns-remap, no-new-privileges, live-restore, default-ulimits, default-address-pools, insecure-registries, cis-docker-benchmark, docker-bench-security, apparmor, seccomp-default-profile]
level: advanced
status: docs-checked
description: "Hardening dockerd itself: the docker.sock privilege-escalation path, daemon.json options that matter, TLS for the remote API, and the CIS Docker Benchmark checks worth automating."
sources: ["https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/engine/security/protect-access/", "https://docs.docker.com/engine/security/rootless/", "https://docs.docker.com/engine/manage-resources/contexts/", "https://github.com/docker/docker-bench-security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker daemon configuration and hardening

**Goal:** the daemon itself — not the containers — is usually the bigger attack surface.
Anyone who can talk to `docker.sock` or the API is root on the host; configure accordingly.

## `docker.sock` is root
Membership in the `docker` group, or any access to `/var/run/docker.sock`, is equivalent to
passwordless root: the daemon can share any host directory with a container without limiting the
container's access, and the Docker docs say socket access gives root access on the host. This is
not a bug to "fix" — it's how the daemon works — so treat socket access as a root grant in
your access model. Never bind-mount `docker.sock` into a container unless that container is
fully trusted (CI runners doing docker-in-docker, monitoring agents), and prefer an authorization
plugin or a proxy that allow-lists API endpoints.

## Remote API: TLS or nothing
Never expose `dockerd -H tcp://0.0.0.0:2375` (unauthenticated). If you need the remote API, enable TLS
client-cert auth:
```json
{ "tls": true, "tlsverify": true,
  "tlscacert": "/etc/docker/ca.pem",
  "tlscert": "/etc/docker/server-cert.pem",
  "tlskey": "/etc/docker/server-key.pem",
  "hosts": ["tcp://0.0.0.0:2376"] }
```
Prefer not exposing it at all — use `docker context create --docker "host=ssh://user@host"`
to drive a remote daemon over SSH instead of opening a TCP port.

## `/etc/docker/daemon.json` options worth knowing
- `"icc": false` - disables inter-container communication on the default bridge network
  (the default is true); user-defined networks are not covered.
- `"userns-remap": "default"` — remaps container UID 0 to an unprivileged host UID range, so
  a container-root-to-host-root escape (e.g. via a kernel bug) lands as an unprivileged host
  user, not root. Breaks some volume ownership assumptions and bind-mounted sockets; test
  before rolling to prod.
- `"no-new-privileges": true` - sets no-new-privileges by default for new containers
  (equivalent to `--security-opt no-new-privileges` on every `run`).
- `"live-restore": true` - containers keep running while the daemon is down (standalone containers only,
  not Swarm services; see `containerd-runc-oci-runtime-internals`).
- `"log-driver": "local"` (or `json-file`) with `"log-opts": {"max-size": "10m", "max-file": "3"}` - set
  rotation globally, not per-container, so you don't rely on every Dockerfile author remembering; the
  `local` driver already defaults to 20m x 5 files with compression.
- `"default-address-pools"` — fixes Compose/VPN subnet collisions; see `container-networking`.
- `"insecure-registries"` — only for a private registry you control without TLS; never for
  anything reachable outside a lab network (no cert validation, trivially MITM'd).

## Rootless and capabilities
Daemon hardening overlaps two other skills: running `dockerd` itself rootless (see
`rootless-containers`) removes the "socket access = root" problem at its root; dropping
Linux capabilities and applying seccomp/AppArmor per-container (see
`linux-capabilities-seccomp-apparmor`) limits blast radius even when the daemon runs as root.

## CIS Docker Benchmark
Docker Bench for Security (`docker/docker-bench-security`) automates the CIS checks. Its README runs
the script from a container with `--net host --pid host --userns host --cap-add audit_control`, a
`DOCKER_CONTENT_TRUST` environment variable and read-only mounts of `/etc`, `/usr/bin/containerd`,
`/usr/bin/runc`, `/usr/lib/systemd`, `/var/lib` and `/var/run/docker.sock`. The README notes the published
`docker/docker-bench-security` image is out of date, so build the image from the repository (or use its
Compose file) instead of pulling it.

## Gotchas
- Enabling `live-restore` itself needs a daemon restart, so plan one maintenance window for the first rollout.
- `userns-remap` is incompatible with external volume or storage drivers that do not understand the
  daemon's mappings; enable it on a fresh install where possible.

## Verify
Docker Bench for Security (built as above) shows the host-config checks passing; `docker info` lists
`name=userns` or `rootless` under Security Options when remap or rootless mode is actually active, not
just configured.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: `dockerd` reference, protect-access, Rootless, contexts and local logging pages), docker/docker-bench-security README, Docker Engine API (SecurityOptions).
- Confirmed `icc`, `no-new-privileges`, `live-restore`, `userns-remap`, `default-address-pools`, `insecure-registries`, TLS keys (`tls`, `tlsverify`, `tlscacert`, `tlscert`, `tlskey`, `hosts`) and `docker context create --docker "host=ssh://..."` against the current references; `local` driver defaults.
- Confirmed the Docker Bench run flags and mounts in its README, and that its published image is out of date (the skill previously told readers to pull it).
- Removed the socket-proxy image name, botnet remark, GPU-compatibility and chicken-and-egg restart claims that no checked source covers.
Method: documentation only; no commands were run.
