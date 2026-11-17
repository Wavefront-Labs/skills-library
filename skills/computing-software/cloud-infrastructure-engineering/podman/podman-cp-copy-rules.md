---
id: computing-software.cloud-infrastructure-engineering.podman.podman-cp-copy-rules
name: podman-cp-copy-rules
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [podman-cp, copy, tar-stream, archive, overwrite, podman-mount, container-files]
level: practitioner
status: docs-checked
description: "Copy files with podman cp: container paths relative to root, destination rules for files and directories, trailing slash versus /., tar streaming with -, no globbing."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-cp.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move files between host and containers predictably.

`podman cp [options] [container:]src_path [container:]dest_path` works between host and container or between two containers, running or stopped. Container paths are relative to `/`, so the leading slash is optional. If a local path contains a colon, be explicit with `/path/to/file:name.txt` or `./file:name.txt`.

Rules: a source file copied to a nonexistent destination becomes that file (parent must exist); onto an existing file it overwrites; into a directory it keeps its base name. A source directory to a nonexistent destination creates it with the contents; onto a file is an error; into an existing directory, a source ending `/` copies the directory itself, while one ending `/.` copies only its contents. Local symlink sources copy the target.

Streaming: `-` as source reads a tar archive from STDIN into a container directory (destination must be a directory); `-` as destination writes a tar to STDOUT, e.g. `podman cp - containerID:/myfiles.tar.gz < myfiles.tar.gz`.

Options: `--archive`/`-a` (default true) changes ownership to the container's primary UID/GID; false keeps archive IDs. `--overwrite` allows replacing a directory with a non-directory and vice versa.

Limits: no globbing; use xargs or find. Permission errors are ignored when copying from a running rootless container. Alternative: `mnt=$(podman mount CONTAINERID)`, use ordinary tools on `${mnt}`, then `podman umount CONTAINERID`.

## Checked
2026-11-09: read the podman-cp man page in full and confirmed the path rules, trailing slash and /. behaviour, colon handling, tar streaming with -, --archive and --overwrite, the rootless permission note, the globbing limit and the podman mount alternative. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
