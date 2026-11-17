---
id: computing-software.cloud-infrastructure-engineering.docker.read-only-parity-with-kubernetes-readonlyrootfilesystem
name: read-only-parity-with-kubernetes-readonlyrootfilesystem
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, read-only-rootfs, readonlyrootfilesystem, kubernetes, emptydir, security-context, tmpfs]
level: advanced
status: docs-checked
description: "Prove an image runs with Kubernetes readOnlyRootFilesystem using Docker first: mapping --read-only/--tmpfs to emptyDir mounts, medium Memory, sizeLimit, and option differences."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/security-context/", "https://kubernetes.io/docs/concepts/storage/volumes/", "https://docs.docker.com/reference/cli/docker/container/run/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read-only parity with Kubernetes readOnlyRootFilesystem

Make the image's writable-path contract explicit and test it locally with Docker, so the
Kubernetes manifest is a translation, not a debugging session.

## Mapping
| Docker | Kubernetes |
|---|---|
| `--read-only` | `securityContext.readOnlyRootFilesystem: true` |
| `--tmpfs /tmp:size=64m` | `emptyDir: { medium: Memory, sizeLimit: 64Mi }` mounted at `/tmp` |
| `-v data:/var/lib/app` | PVC or `emptyDir` (disk) at `/var/lib/app` |
| `--user 10001:10001` | `runAsUser: 10001`, `runAsGroup: 10001` |
| `--cap-drop ALL` | `capabilities: { drop: ["ALL"] }` |
| `--security-opt no-new-privileges` | `allowPrivilegeEscalation: false` |

## Local test that mirrors the pod
```bash
docker run --rm --read-only --user 10001:10001 --cap-drop ALL \
  --security-opt no-new-privileges \
  --tmpfs /tmp:size=64m --tmpfs /var/cache/app:size=128m \
  -e APP_ENV=staging app:1.4
```
Docker docs: `--read-only` mounts the root filesystem read-only and prohibits writes to locations
other than the volumes you specify. The `--tmpfs` options are identical to `mount -t tmpfs -o`.

## Manifest
```yaml
containers:
  - name: app
    image: reg.example.com/app:1.4
    securityContext:
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 10001
      allowPrivilegeEscalation: false
      capabilities: { drop: ["ALL"] }
    volumeMounts:
      - { name: tmp, mountPath: /tmp }
      - { name: cache, mountPath: /var/cache/app }
volumes:
  - { name: tmp, emptyDir: { medium: Memory, sizeLimit: 64Mi } }
  - { name: cache, emptyDir: { sizeLimit: 128Mi } }
```

## Differences to remember
- Pass mount options to `--tmpfs` explicitly (the Docker docs example uses `rw,noexec,nosuid`); an
  `emptyDir` has its own behaviour, so test executable-from-/tmp assumptions in the cluster too.
- `emptyDir` with `medium: Memory` is a tmpfs, and files written there count against the memory
  limit of the container that wrote them. With no size set, memory-backed volumes are sized to
  node allocatable memory, so set `sizeLimit`.
- A disk `emptyDir` `sizeLimit` is allocated from node ephemeral storage, which can fill from other
  sources first. The medium is whatever backs the kubelet root directory.

## Make it a contract
Document writable paths in the image (for example an organisation-specific label listing
`/tmp,/var/cache/app`) and run the Docker command above in CI as a smoke test.

## Checked
Checked 2026-10-28 against the Kubernetes "Volumes" page (emptyDir medium, sizeLimit, memory
accounting) and "Configure a Security Context" (`readOnlyRootFilesystem`), and the `docker run`
reference (`--read-only`, `--tmpfs`, `--user`, `--cap-drop`, `no-new-privileges`).
Removed as unconfirmed: that Docker `--tmpfs` defaults to `noexec,nosuid,nodev` and that
Kubernetes emptyDir is always executable, the list of files Kubernetes mounts writable, and the
claim that Pods ignore image `VOLUME` instructions.
Method: documentation only; no commands were run.
