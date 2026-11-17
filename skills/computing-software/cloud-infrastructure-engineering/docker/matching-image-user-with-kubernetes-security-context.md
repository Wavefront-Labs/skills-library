---
id: computing-software.cloud-infrastructure-engineering.docker.matching-image-user-with-kubernetes-security-context
name: matching-image-user-with-kubernetes-security-context
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, non-root, run-as-user, fsgroup, runasnonroot, security-context, numeric-uid, kubernetes]
level: advanced
status: docs-checked
description: "Align a Dockerfile USER with Kubernetes runAsUser, runAsNonRoot and fsGroup so pods start, volumes are writable and Pod Security restricted passes without chown hacks."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/security-context/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://docs.docker.com/reference/dockerfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching image USER with Kubernetes securityContext

## The contract
- Set a numeric `USER uid:gid` in the image and use the same numbers in the pod spec.
- `runAsUser` in the pod overrides the image's user; files owned by the image's UID may then be
  unwritable to the new UID, so keep the two equal.
- The Pod Security Standards "restricted" profile requires `runAsNonRoot: true` (container fields
  may be unset if the pod-level field is `true`), `allowPrivilegeEscalation: false`, and a seccomp
  profile that is not `Unconfined` (allowed: unset, `RuntimeDefault`, `Localhost`). Read the
  current profile page for its capability rules.
- An image with no `USER` runs as root, which `runAsNonRoot: true` is meant to refuse.

## Pod spec that matches the image
```dockerfile
RUN groupadd -g 10001 app && useradd -u 10001 -g 10001 -M -s /sbin/nologin app
COPY --chown=10001:10001 --chmod=755 app /app
USER 10001:10001
```
```yaml
securityContext:                 # pod level
  runAsNonRoot: true
  runAsUser: 10001
  runAsGroup: 10001
  fsGroup: 10001                 # supported volumes become owned and writable by GID 10001
  fsGroupChangePolicy: OnRootMismatch
  seccompProfile: { type: RuntimeDefault }
containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities: { drop: ["ALL"] }
```

## fsGroup and volumes
- Volumes that support ownership management are modified to be owned and writable by the
  `fsGroup` GID, so the image does not need an init container running `chown`.
- By default Kubernetes recursively changes ownership and permissions for the volume contents
  when it is mounted; for large volumes this slows Pod start. `fsGroupChangePolicy: OnRootMismatch`
  only changes them when the root directory's ownership or permissions do not match.
- `fsGroupChangePolicy` applies only to volume types that support fsGroup-controlled ownership.
- If `runAsGroup` is omitted the primary GID stays 0 (root).

## Reproduce locally with Docker
```bash
docker run --rm --user 10001:10001 --group-add 10001 --read-only --cap-drop ALL \
  --security-opt no-new-privileges -v data:/data <image>
```
`--user` takes `<name|uid>[:<group|gid>]`.

## Gotchas
- `runAsUser` different from the image UID plus `readOnlyRootFilesystem` exposes every path
  the app writes; fix with emptyDir mounts, not by reverting to root.
- Base images define their own non-root users; read your base image's documentation rather than
  assuming a UID.

## Checked
Checked 2026-10-28 against the Kubernetes pages "Configure a Security Context" and "Pod Security
Standards", the `docker run` reference (`--user`, `--group-add`, `--read-only`, `--cap-drop`,
`no-new-privileges`) and the Dockerfile reference (`COPY --chown`): fsGroup ownership, default
recursive change, `OnRootMismatch`, runAsGroup default, restricted-profile fields and values.
Removed as unconfirmed: the two kubelet error strings and the "non-numeric user" failure row,
hostPath and CSI `fsGroupPolicy` remarks, and the per-distro UID numbers (65532, 1000).
Method: documentation only; no commands were run.
