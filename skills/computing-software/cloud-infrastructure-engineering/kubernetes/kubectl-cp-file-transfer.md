---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-cp-file-transfer
name: kubectl-cp-file-transfer
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-debug, kubectl-cp, kubectl-exec, distroless]
level: practitioner
status: docs-checked
description: "Copy files to and from pods with kubectl cp, its tar dependency, container and path syntax, permissions, and alternatives for distroless images."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_cp/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/cp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl cp

```bash
kubectl cp shop/web-5d8:/var/log/app/app.log ./app.log
kubectl cp ./config.json shop/web-5d8:/tmp/config.json -c web
kubectl cp shop/web-5d8:/data ./data-backup              # directories recursively
kubectl cp ./dump.sql shop/db-0:/tmp/dump.sql --retries=5
```
Syntax: `<namespace>/<pod>:<path>`; `-c` picks the container.

## How it works and why it fails
`kubectl cp` runs `tar` inside the container through exec and streams it.
- Container has no `tar` (distroless, scratch): `exec: "tar": executable file not found`.
- Copying from a pod skips symlinks with a warning that suggests `kubectl exec ... -- tar cf - <path> | tar xf -`; the same pipe handles wildcards.
- Read-only filesystems: copy into a writable directory such as `/tmp`.
- Large files over flaky connections: use `--retries` (default 0, no retry; a negative value retries forever).

## Distroless alternatives
```bash
# 1. stream with cat if present
kubectl exec shop/web-5d8 -- cat /app/config.yaml > config.yaml
# 2. if the file is on a volume, mount the PVC in a helper pod and copy from there
```

## Security
`kubectl cp` runs `tar` through exec, so the caller needs permission to exec into the pod. Treat it like a shell.

## Verify
Compare a checksum of the file locally and inside the pod for important transfers.

## Checked
Checked 2026-10-24 against the kubectl cp source (main): the `tar` requirement stated in its help, the `--retries` default and semantics, the `<namespace>/<pod>:<path>` form, the symlink-skipping warning on download and the tar exec pipe it recommends. Removed the unconfirmed leading-slash warning, the debug-container recipe, the audit remark and the pinned image tag.
Method: documentation only; no commands were run.
