---
id: computing-software.cloud-infrastructure-engineering.podman.container-checkpoint-and-migration-image
name: container-checkpoint-and-migration-image
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [checkpoint, criu, container-migration, export, create-image, compress, file-locks]
level: sme
status: docs-checked
description: "Checkpoint running containers with podman container checkpoint: --all, compression of exported archives, --export for migration, --create-image annotations and file locks."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-container-checkpoint.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: freeze a container's processes and move or restore them later.

`podman container checkpoint [options] container...` checkpoints all processes of one or more containers; restore them with `podman container restore`. A container using systemd as entrypoint might not be checkpointable.

`--all`/`-a` checkpoints all running containers and needs no container argument.

`--export`/`-e` writes the checkpoint to an archive for importing the container on another system, enabling live migration. The archive includes changes to the root filesystem unless `--ignore-rootfs` is used. `--compress`/`-c` picks `zstd` (default), `gzip` or `none`; none can create the archive faster.

`--create-image=image` makes an OCI image in the local store with a single layer holding the checkpoint files in the same format as `--export`. Push it to a registry and pull it elsewhere to migrate; it can also be exported with `podman image save` and inspected with `podman inspect`, which shows annotations about the checkpoint host: `io.podman.annotations.checkpoint.name`, `.rawImageName`, `.rootfsImageID`, `.rootfsImageName`, `.podman.version`, `.criu.version`, `.runtime.name`, `.runtime.version`, `.conmon.version`, `.host.arch`, `.host.kernel`, `.cgroups.version`, `.distribution.version` and `.distribution.name`.

`--file-locks` is required at checkpoint and restore if the application uses file locks; otherwise checkpointing such containers is expected to fail. If no locks are used the option is ignored.

## Checked

2026-11-09. Read against the official page text (podman-container-checkpoint.1); options, compression values, defaults and all listed annotations were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
