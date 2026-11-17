---
id: computing-software.cloud-infrastructure-engineering.docker.save-and-load-specific-platforms
name: save-and-load-specific-platforms
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-save, docker-load, save-platform, multi-platform, air-gapped, containerd-image-store]
level: practitioner
status: docs-checked
description: "Export and import the right architecture: docker save/load --platform, multi-platform archives on the containerd store, and pulling all needed platforms before saving."
sources: ["https://docs.docker.com/reference/cli/docker/image/save/", "https://docs.docker.com/reference/cli/docker/image/load/", "https://docs.docker.com/engine/storage/containerd/", "https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# save and load for specific platforms

Air-gapped targets are often a different architecture from the machine preparing the bundle
(amd64 laptop, arm64 edge devices).

## Saving
`docker save` saves all platform variants that are present in the daemon's image store;
`--platform` saves only the given variant(s), formatted `os[/arch[/variant]]` (comma-separated
list), and produces an error if the platform is not present locally.
```bash
docker pull --platform linux/arm64 nginx:1.27
docker image inspect -f '{{.Architecture}}' nginx:1.27      # arm64
docker save --platform linux/arm64 -o nginx-arm64.tar nginx:1.27
```
A missing variant gives an error such as `no suitable export target found for platform ...`.
To produce a multi-arch archive, pull each platform first, then save without `--platform`:
```bash
for p in linux/amd64 linux/arm64; do docker pull --platform $p nginx:1.27; done
docker save -o nginx-multi.tar nginx:1.27
```
Registry-side alternative that does not depend on the local store:
`skopeo copy --all docker://nginx:1.27 oci-archive:nginx-multi.tar`.

Which image store you have matters: since Docker Engine 29.0, fresh installations use the
containerd image store by default, while an upgraded daemon keeps the legacy graph drivers
(overlay2) until you switch. Docker's containerd-store page notes that with classic storage
drivers you need external builders for multi-platform images. Check `docker info` for the
storage driver in use.

## Load
```bash
docker load -i nginx-multi.tar                          # loads all platform variants in the archive
docker load --platform linux/arm64 -i nginx-multi.tar   # only one
docker image ls --tree nginx
```
`--platform` on `load` loads only the given platform(s) and errors if the requested platform is
not in the archive (message: `requested platform (...) not found`). Both `--platform` options
need API version 1.48 or later (Docker Engine 28+).

## Verify on the target
```bash
docker run --rm nginx:1.27 uname -m        # aarch64 on the arm64 device
docker image inspect -f '{{.Os}}/{{.Architecture}}{{if .Variant}}/{{.Variant}}{{end}}' nginx:1.27
```

## Gotchas
- `exec format error` at runtime means the wrong architecture was saved.
- arm variants matter: a 32-bit Raspberry Pi OS needs `linux/arm/v7` (or v6), not `linux/arm64`.

## Checked

2026-10-26 against Docker CLI reference data (docker/docs main, 2026-10-23), containerd image store page, skopeo, containers-transports and crane documentation. Confirmed in the docker image save and load reference: --platform syntax, behaviour, error cases and the 1.48 minimum API version; containerd image store default for fresh Engine 29.0+ installations and the classic-driver multi-platform note; skopeo --all. Removed the claims about the classic store keeping one platform per tag, tag replacement on a second pull, and load behaviour of old engines.

Method: documentation only; no commands were run.
