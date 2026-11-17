---
id: computing-software.cloud-infrastructure-engineering.podman.volume-create-drivers-and-options
name: volume-create-drivers-and-options
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [volume-create, local-driver, image-driver, tmpfs, opt, uid-gid, volume-plugin]
level: practitioner
status: docs-checked
description: "Create Podman volumes with podman volume create: local versus image drivers, --opt type/device/o/copy, tmpfs size, uid/gid ownership, --ignore and plugin drivers."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-volume-create.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create volumes with the right backend and ownership.

`podman volume create [options] [name]` makes an empty volume; without a name a random one is generated. `--label`/`-l` adds metadata visible in `volume inspect` and `volume ls`; `--ignore` prints the name instead of failing if the volume exists (new options are not applied to it).

Drivers (`--driver`/`-d`, default `local`): `local` uses a directory on disk, or the `mount(8)` command when `--opt` is set. `image` uses an image as backing store through an overlay filesystem so changes can be committed as a new layer; its only option is `image`, which is mandatory. Any other value is treated as a volume plugin defined in the `volume_plugins` section of containers.conf.

`--opt`/`-o` for `local`: `type` (mount `-t`), `device`, `o` (mount `-o` options) and `[no]copy` (copy image content from the mount path on first run; the default). The `o` option also accepts `uid`, `gid`, `size` (tmpfs and xfs), `inodes` (xfs), `noquota`, and `timeout`; non-UID/GID options need root. Use `-o=o=uid=1000`, not `-o=uid=1000`.

`--uid` and `--gid` set the volume's owner without passing the value to mount.

Example: `podman volume create --opt device=tmpfs --opt type=tmpfs --opt o=size=2M,nodev,noexec myvol`.

## Checked
2026-11-09: read the podman-volume-create man page in full and confirmed the drivers, --opt options for local and image, the o sub-options (uid, gid, size, inodes, noquota, timeout), the -o=o= note, --uid and --gid, --ignore, --label and the tmpfs example. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

