---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-install-docker
name: tetragon-install-docker
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [install-docker]
level: intro
status: docs-checked
description: "Start Tetragon in a privileged Docker container on a local Linux host and run the Cilium demo workloads with Docker Compose."
sources:
  - "https://tetragon.io/docs/getting-started/install-docker/"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/docker-compose.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run Tetragon in Docker

Goal: experiment with Tetragon on a local Linux host using the released container image.

The guide was tested on Ubuntu 22.04 and 22.10 (kernels 5.15.0 and 5.19.0) on amd64 and arm64. Any recent distribution shipping a relatively recent kernel should work. Tetragon cannot run on Docker Desktop for macOS because of a limitation of its Linux virtual machine.

## Start Tetragon

```shell
docker run -d --name tetragon --rm --pull always \
    --pid=host --cgroupns=host --privileged             \
    -v /sys/kernel/btf/vmlinux:/var/lib/tetragon/btf    \
    quay.io/cilium/tetragon:<version>
```

This starts Tetragon in a privileged container in the background. Running privileged is required to load and attach BPF programs.

## Run a demo workload

Any workload works. The guide uses Cilium's demo app through `examples/quickstart/docker-compose.yaml`:

```yaml
name: starwars
networks:
  galaxyfaraway:
services:
  deathstar:
    hostname: deathstar
    image: quay.io/cilium/starwars:v2.1
    networks:
      - galaxyfaraway
    ports:
      - 8080:80
    restart: always
  tiefighter:
    hostname: tiefighter
    image: quay.io/cilium/json-mock:v1.3.8
    networks:
      - galaxyfaraway
    restart: always
  xwing:
    hostname: xwing
    image: quay.io/cilium/json-mock:v1.3.8
    networks:
      - galaxyfaraway
    restart: always
```

```shell
curl -LO https://github.com/cilium/tetragon/raw/main/examples/quickstart/docker-compose.yaml
docker compose -f docker-compose.yaml up -d
docker container ls
```

`docker container ls` should show the `starwars-deathstar-1`, `starwars-tiefighter-1` and `starwars-xwing-1` containers running; image downloads can take a short time. The next step in the guide is to look at execution events.

## Checked

Date: 2026-11-07

Docker install page read in full, plus the docker-compose.yaml it downloads (added to sources). The image tag is a placeholder.

Method: documentation only; no commands were run.
