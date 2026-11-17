---
id: computing-software.cybersecurity-defensive.system-hardening.read-only-root-filesystem
name: read-only-root-filesystem
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [read-only-root-filesystem, readonlyrootfilesystem, immutable-infrastructure, container-hardening, dm-verity, overlayfs]
level: practitioner
status: docs-checked
description: "Run containers and hosts with read-only root filesystems: Kubernetes readOnlyRootFilesystem with writable emptyDir mounts, Docker --read-only, and immutable OS images."
sources: ["https://github.com/kubernetes/website/blob/main/content/en/docs/tasks/configure-pod-container/security-context.md", "https://github.com/kubernetes/website/blob/main/content/en/docs/concepts/security/pod-security-standards.md", "https://github.com/docker/cli/blob/master/docs/reference/commandline/container_run.md", "https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/device-mapper/verity.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read-only root filesystems

If the root filesystem cannot be written, attackers cannot drop binaries, modify app code or install
persistence there, and drift is impossible by construction. FIM becomes almost trivial: only explicit writable
paths need watching.

## Kubernetes
```yaml
securityContext:
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  runAsNonRoot: true
  capabilities: {drop: ["ALL"]}
volumeMounts:
  - {name: tmp, mountPath: /tmp}
  - {name: cache, mountPath: /app/cache}
volumes:
  - {name: tmp, emptyDir: {sizeLimit: 64Mi}}
  - {name: cache, emptyDir: {sizeLimit: 512Mi}}
```
- Find write paths first: run the container normally and watch for `Read-only file system` errors in the logs.
- Common needs: `/tmp`, cache and run directories, runtime scratch space and application upload directories (use object storage for uploads instead); mount only those paths as writable volumes.
- Pod Security Admission's restricted profile does not require `readOnlyRootFilesystem`, so enforce it with an admission policy engine of your choice.

## Docker / Compose
`docker run --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m image` (`--read-only` mounts the container's root filesystem read-only; `--tmpfs` options are those of `mount -t tmpfs -o`).

## Hosts
- Immutable OS images keep the system partition read-only and update by replacing the image.
- General Linux: mount `/usr` read-only, or use a read-only root with a writable overlay for `/etc` and `/var`.
- **dm-verity** (device-mapper `verity` target) provides transparent integrity checking of block devices using a cryptographic digest; the target is read-only.

## Gotchas
- `emptyDir` volumes consume node storage; set `sizeLimit`.
- Writable mounts with `exec` allowed are still a drop zone; mount `/tmp` noexec where the app allows.
- Package managers in running containers stop working, which is the point; patch by rebuilding images.

## Verify
`kubectl exec pod -- touch /bin/x` fails with "Read-only file system"; a review of workload specs shows `readOnlyRootFilesystem: true` or a documented exception.

## Checked
Checked 2026-10-25 against the Kubernetes security-context task and Pod Security Standards (kubernetes/website, 2026-10-24: `readOnlyRootFilesystem` is a container securityContext field and is absent from the restricted profile), the Docker `container run` reference (`--read-only`, `--tmpfs`) and the kernel dm-verity documentation. Removed unconfirmed claims: `docker diff` usage, specific application paths, Kyverno policy name (not found in the kyverno/policies repository), Docker Bench check number, named immutable distributions and overlay tools, and the Windows Unified Write Filter note. The CIS Kubernetes benchmark was not read.

Method: documentation only; no commands were run.
