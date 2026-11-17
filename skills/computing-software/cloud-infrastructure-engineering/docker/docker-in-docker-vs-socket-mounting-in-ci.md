---
id: computing-software.cloud-infrastructure-engineering.docker.docker-in-docker-vs-socket-mounting-in-ci
name: docker-in-docker-vs-socket-mounting-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-in-docker, dind, dood, dind-vs-dood, dind-tls, dind-privileged, sysbox, rootless-dind, ci]
level: advanced
description: "Choose between Docker-in-Docker, mounting the host socket (DooD) and Sysbox for CI jobs that build or run containers, with TLS and privilege trade-offs."
sources: ["https://hub.docker.com/_/docker", "https://github.com/docker-library/docs/blob/master/docker/README.md", "https://github.com/nestybox/sysbox/blob/master/docs/quickstart/dind.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker-in-Docker vs socket mounting in CI

| | DinD (`docker:dind`) | DooD (mount `/var/run/docker.sock`) | Sysbox |
|---|---|---|---|
| Isolation from host | weak: needs `--privileged` | none: job controls host daemon | strong: no privileged |
| Layer cache | empty per job unless persisted | shared with host | per container |
| Paths for `-v` | inside dind | **host** paths | inside |
| Concurrent jobs interfering | no | yes (names, ports, prune) | no |

## DinD with TLS
```sh
docker network create ci
docker run -d --name dind --privileged --network ci \
  -e DOCKER_TLS_CERTDIR=/certs -v dind-certs-client:/certs/client docker:dind
docker run --rm --network ci -e DOCKER_HOST=tcp://dind:2376 -e DOCKER_TLS_VERIFY=1 \
  -e DOCKER_CERT_PATH=/certs/client -v dind-certs-client:/certs/client:ro docker:cli docker info
```
- The official image's `dind` variants generate TLS certificates under `DOCKER_TLS_CERTDIR`
  (enabled by default since 19.03); the daemon then listens on `tcp://0.0.0.0:2376` with
  `--tlsverify`, and the client container must share the `client` subdirectory. With TLS
  disabled it listens on 2375 without authentication.
- `--privileged` is required for Docker-in-Docker; the image README warns it gives full access
  to the host environment. Treat DinD runners as single-tenant.
- Storage: to keep or share dind's data, mount a volume at `/var/lib/docker`.

## DooD
```sh
docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli docker build -t app .
```
Fast and cached, but the job is root on the host, sees all containers, and `-v $PWD:/src`
refers to the host's path, not the job container's. Only for trusted, single-tenant runners.

## Sysbox
Install the Sysbox runtime on the host, then run a system-container image that bundles
Docker (the Sysbox quickstart uses Nestybox images):
```sh
docker run --runtime=sysbox-runc -it nestybox/alpine-docker:latest      # no --privileged
```
The Sysbox quickstart describes running Docker inside system containers with plain
`docker run` commands and no insecure privileged containers.

## Rootless DinD
The `docker:dind-rootless` variant is experimental per the image README and still needs
`--privileged`; the inner daemon runs as the image's `rootless` user (UID/GID 1000 by default).

## Verify
In the job: `docker info -f '{{.Name}} {{.SecurityOptions}}'` shows the dind/sysbox host, not
the runner; `docker ps` lists only the job's containers.

## Checked
Date: 2026-10-26. Documentation: docker-library/docs `docker` image README (tags at 29.x), Sysbox quickstart (nestybox/sysbox, last commit 2026-10-21). Confirmed: `DOCKER_TLS_CERTDIR` behaviour, ports 2376/2375, `--privileged` requirement, client cert sharing, `/var/lib/docker` volume, rootless variant and UID 1000, Sysbox runtime flag and no-privileged claim. Removed as unconfirmed: the pinned `27` tags (README now lists 29.x; the unpinned `dind` and `cli` tags are used), `docker:dind` under Sysbox, start-up race and MTU advice, overlay-on-overlay claim, Kubernetes RuntimeClass line, the "prefer not to need a daemon" list.
Method: documentation only; no commands were run.
