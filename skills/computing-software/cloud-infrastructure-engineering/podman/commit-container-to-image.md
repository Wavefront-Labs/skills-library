---
id: computing-software.cloud-infrastructure-engineering.podman.commit-container-to-image
name: commit-container-to-image
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [podman-commit, change, image-format, oci, docker, squash, include-volumes]
level: practitioner
status: docs-checked
description: "Create an image from a changed container with podman commit: --change instructions, author and message, format oci versus docker, pausing, volumes and squash."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-commit.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: snapshot container state as a new image.

`podman commit [options] container [image]` (also `podman container commit`) creates an image from a changed container. If `image` has no registry component, `localhost` is added; if no image name is given, REPOSITORY and TAG are `<none>`. The container and its processes are paused during commit by default; `--pause`/`-p` defaults to true, and pausing prevents race conditions and potential security issues from other processes accessing the rootfs.

`--change`/`-c` applies instructions: CMD, ENTRYPOINT, ENV, EXPOSE, LABEL, ONBUILD, STOPSIGNAL, USER, VOLUME, WORKDIR; repeatable. Example: `podman commit --change CMD=/bin/bash --change ENTRYPOINT=/bin/sh --change "LABEL blue=image" reverent_golick image-committed`.

Metadata: `--author`/`-a`, and `--message`/`-m`, but the message is not supported in `oci` format. `--format`/`-f` is `oci` (default) or `docker`. `--config` merges a JSON-encoded Schema2Config file into the image config. `--iidfile` writes the image ID to a file. `--quiet`/`-q` suppresses output.

`--include-volumes` (default false) includes contents of volumes added by `--volume` or `--mount` in `podman create`/`run`. `--squash`/`-s` (default false) squashes newly built layers into one.

## Checked
2026-11-09: read the podman-commit man page in full and confirmed the synopsis, localhost and <none> naming, --change instructions and example, --author, --message (not supported in oci), --format default, --config, --iidfile, --quiet, --pause default, --include-volumes and --squash defaults. Removed the sentence about secrets not being committed (not on this page; it is on the secret-create page).

Method: documentation only; no commands were run.

