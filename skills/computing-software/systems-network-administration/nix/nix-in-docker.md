---
id: computing-software.systems-network-administration.nix.nix-in-docker
name: nix-in-docker
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, docker, container-image, ghcr]
level: practitioner
status: docs-checked
description: "Run Nix in the official docker.io/nixos/nix image, get pre-release images from ghcr.io, and build a non-root single-user image with docker.nix."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/installing-docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Latest stable:

```
docker run -ti docker.io/nixos/nix
```

Check the version inside with `nix --version`. For the latest pre-release use `ghcr.io/nixos/nix`; tags are listed at github.com/nixos/nix/pkgs/container/nix.

The official image is built with `pkgs.dockerTools.buildLayeredImage`, not a Dockerfile, has no base image and contains only minimal runtime dependencies. You can base your own image on it.

Latest development build from Hydra:

```
curl -L https://hydra.nixos.org/job/nix/master/dockerImage.x86_64-linux/latest/download/1 | docker load
```

Build from source:

```
nix build ./\#hydraJobs.dockerImage.x86_64-linux
docker load -i ./result/image.tar.gz
```

Non-root image (single-user Nix as another user):

```
nix build --file docker.nix \
    --arg uid 1000 \
    --arg gid 1000 \
    --argstr uname user \
    --argstr gname user \
    --argstr name nix-user \
    --out-link nix-user.tar.gz
docker load -i nix-user.tar.gz
docker run -ti nix-user
```

## Checked

2026-11-04: image names, ghcr.io pre-releases, buildLayeredImage and no-base-image notes, the Hydra download command, the source build and the docker.nix arguments confirmed against the Using Nix within Docker manual page. Removed nothing (the nix --version check is shown in the page's first example).

Method: documentation only; no commands were run.
