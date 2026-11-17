---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-run-in-docker
name: grafana-alloy-run-in-docker
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [docker, grafanaalloy, boringcrypto, distroless, listen-addr, container-image]
level: intro
status: docs-checked
description: "Run Alloy in Docker with the grafana/alloy image, the listen-addr 0.0.0.0 requirement for the UI, BoringCrypto and distroless tags, and Windows image tags."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/install/docker.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Alloy in Docker

Images exist for Linux (AMD64, ARM64, ppc64le, s390x), macOS via Docker Desktop (a transparent Linux VM) and Windows containers (AMD64).

```shell
docker run \
  -v /path/to/config.alloy:/etc/alloy/config.alloy \
  -p 12345:12345 \
  grafana/alloy:latest \
    run --server.http.listen-addr=0.0.0.0:12345 --storage.path=/var/lib/alloy/data \
    /etc/alloy/config.alloy
```
Everything after the image name is passed to the Alloy binary as the `run` command and its flags. Gotcha: without `--server.http.listen-addr=0.0.0.0:12345` the debugging UI is not reachable from outside the container. Verify by opening http://localhost:12345.

## Image variants
- `grafana/alloy:boringcrypto` (latest stable) and `grafana/alloy:VERSION-boringcrypto` (for example `v1.1.0-boringcrypto`): public preview, Linux AMD64/ARM64, released since 1.10.
- Distroless (experimental, since 1.20): `latest-distroless`, `VERSION-distroless`, `boringcrypto-distroless`, `VERSION-boringcrypto-distroless`. Same entrypoint, config path and storage path as the standard image.
- Windows: `grafana/alloy:windowsservercore-ltsc2022` and `VERSION-windowsservercore-ltsc2022`; the host must be Windows Server 2022 or support `ltsc2022` containers, and the same listen-addr rule applies.

## Checked

2026-11-04. Confirmed against the Run Alloy in a Docker container page (set-up/install/docker.md): platforms, docker run form, listen-addr note, BoringCrypto tags (since 1.10), distroless tags (since 1.20, experimental), Windows ltsc2022 tags. No claims changed.

Method: documentation only; no commands were run.
