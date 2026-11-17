---
id: computing-software.digital-forensics-incident-response.evidence-handling.preserving-container-images-and-filesystems
name: preserving-container-images-and-filesystems
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [container-image-preservation, container-forensics, cloud-evidence, docker-forensics, dfir]
level: advanced
status: docs-checked
description: "Preserve evidence from running containers: docker export (and its volume limit), the Kubernetes kubelet checkpoint API, and docker-explorer for offline review."
sources: ["https://docs.docker.com/reference/cli/docker/container/export/", "https://kubernetes.io/docs/reference/node/kubelet-checkpoint-api/", "https://github.com/google/docker-explorer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preserving container images and filesystems

**Goal:** containers are ephemeral, so capture filesystem and, where possible, state before orchestration replaces them. Hash everything you collect and log it.

## Docker: export the filesystem
```bash
docker export --output=container_fs.tar CONTAINER
sha256sum container_fs.tar
```
- `docker export` writes a container's filesystem as a tar archive; `-o`/`--output` writes to a file instead of STDOUT.
- It does not export the contents of volumes associated with the container. If a volume is mounted on top of an existing directory in the container, it exports the underlying directory, not the volume. Capture volumes separately (Docker's user guide covers backing up volumes).

## Kubernetes: kubelet checkpoint
- The kubelet checkpoint API is Beta since Kubernetes v1.30 and enabled by default. A checkpoint is a stateful copy of a running container.
- Request: `POST /checkpoint/{namespace}/{pod}/{container}` on the kubelet, with an optional `timeout` query (seconds). Time depends on container memory use. Responses: 200, 401, 404 (feature gate disabled or pod/container not found), 500 (CRI error or CRI does not implement checkpointing).
- The archive is named `checkpoint-<podFullName>-<containerName>-<timestamp>.tar` and stored in the checkpoints directory under the kubelet root dir, `/var/lib/kubelet/checkpoints` by default. It is a tar, and its contents depend on the container runtime.
- A checkpoint typically contains all memory pages of all processes in the container, so it can include private data and encryption keys. Treat the archive as highly sensitive, and note that it is readable by its owner if you move it.

## Offline analysis
docker-explorer helps a forensic analyst explore offline Docker filesystems (AuFS or OverlayFS layers stored as folders plus JSON files on the host). Its README shows listing containers (`de.py -r <docker root> list running_containers`), mounting a container's filesystem and showing image history. Note it is not an officially supported Google product.

## Gotchas
- Running commands inside a live container changes its state; prefer collecting from outside where you can.
- Keep the original pod or container running until analysis ends where policy allows.

## Verify
Captured archive hashes are recorded and the collection time and command are logged.

## Checked
Confirmed against the Docker `container export` reference (output, volume behaviour), the Kubernetes Kubelet Checkpoint API page (feature state, request, timeout, response codes, archive name and directory, memory-page warning) and the docker-explorer README. Removed unconfirmed content: kubectl label/cordon steps, node auto-repair, `docker inspect/diff/image save/logs/top/exec` commands, overlay2 and containerd paths, container-diff, managed-node (Fargate, Autopilot) claims and the "loses timestamps" claim.

Method: docs-only read of cited pages, 2026-11-09
