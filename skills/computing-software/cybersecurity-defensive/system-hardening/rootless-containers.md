---
id: computing-software.cybersecurity-defensive.system-hardening.rootless-containers
name: rootless-containers
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [container-hardening, rootless-containers, rootless-podman, rootless-docker, user-namespaces, subuid, run-as-non-root]
level: advanced
status: docs-checked
description: "Run containers rootless with Podman or rootless Docker and run workloads as non-root inside images: subuid setup, networking and port limits, volumes and Kubernetes equivalents."
sources: ["https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/security/rootless/_index.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/security/rootless/tips.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/tasks/configure-pod-container/security-context.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/tasks/configure-pod-container/user-namespaces.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rootless containers

**Goal:** a container breakout lands as an unprivileged user, not host root.

## Two different things
1. **Rootless engine:** the container runtime itself runs as a normal user (Podman rootless, Docker rootless mode). Container "root" maps to the user's subordinate UIDs.
2. **Non-root workload:** the process inside the container runs as a non-zero UID (`USER` in Dockerfile, `runAsNonRoot`). Do both where possible.

## Podman rootless
```
grep $USER /etc/subuid /etc/subgid        # e.g. alice:100000:65536 ; add with usermod --add-subuids 100000-165535 --add-subgids 100000-165535 alice
podman run --rm -d -p 8080:8080 --name web docker.io/library/nginx:alpine
podman unshare cat /proc/self/uid_map
loginctl enable-linger alice              # keep user services running after logout
```

## Docker rootless
Run `dockerd-rootless-setuptool.sh install` as the non-root user (shipped in the `docker-ce-rootless-extras` package if missing), then `export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock`.

## Limitations
- Binding ports below 1024 needs a lower `net.ipv4.ip_unprivileged_port_start` (the Docker rootless tips page uses a value of 0 as its example) or a proxy.
- Current Podman uses pasta for rootless networking (see the Podman rootless tutorial).
- Volume ownership: files appear owned by mapped UIDs on the host; use the `:U` volume suffix (Podman, which sets the correct host UID and GID) or `podman unshare chown`.
- Docker rootless resource limits (`--cpus`, `--memory`, `--pids-limit`) need cgroup v2 with systemd.

## Non-root images
In the image, create an unprivileged user and switch to it with a numeric `USER` so Kubernetes `runAsNonRoot` can verify it.
Kubernetes:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  allowPrivilegeEscalation: false
  capabilities: { drop: ["ALL"] }
```
Kubernetes user namespaces (`hostUsers: false` in the pod spec; feature gate `UserNamespacesSupport` is GA from Kubernetes 1.36, beta from 1.30 and on by default from 1.33) give a rootless-like UID mapping per pod.

## Verify
- [ ] `podman unshare cat /proc/self/uid_map` shows the subordinate UID mapping (Podman).
- [ ] `docker run --rm img id -u` returns non-zero.
- [ ] Pod Security Admission `restricted` profile accepts the workloads.

## Checked
Checked 2026-10-25 against the Podman rootless tutorial (containers/podman, 2026-10-23), Docker Engine rootless mode and tips pages (docker/docs, 2026-10-23), the Kubernetes security-context and user-namespaces tasks and the UserNamespacesSupport feature-gate file (kubernetes/website, 2026-10-24). Confirmed: /etc/subuid and /etc/subgid usage and the pause-process note, `usermod --add-subuids/--add-subgids`, `podman unshare`, `:U`, pasta networking, `dockerd-rootless-setuptool.sh install`, `DOCKER_HOST`, `loginctl enable-linger`, cgroup v2 requirement for rootless resource limits, `runAsNonRoot`/`runAsUser` fields, `hostUsers`. Corrected: Kubernetes user namespaces are no longer beta (GA in 1.36). Removed unconfirmed Quadlet/`podman generate systemd`, slirp4netns performance, Dockerfile image example and conmon verification claims.

Method: documentation only; no commands were run.
