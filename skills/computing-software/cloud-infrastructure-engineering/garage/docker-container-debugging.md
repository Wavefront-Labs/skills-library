---
id: computing-software.cloud-infrastructure-engineering.garage.docker-container-debugging
name: docker-container-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [docker-debugging, distroless-image, docker-exec, proc-root]
level: practitioner
status: docs-checked
description: "Debug the shell-less dxflrs/garage image with logs, direct /garage commands and a namespace-sharing helper container."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/debugging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The official `dxflrs/garage` image is built `FROM scratch` and holds only the static `garage` binary, so `docker exec -it garage /bin/sh` fails.

Alternatives:

- Logs: `docker logs garage`, with more detail by starting the container with `RUST_LOG=garage=debug`.
- CLI: the entrypoint binary is `/garage`, so `docker exec garage /garage status` or `docker exec garage /garage --help` work for layout, buckets, keys and repairs.
- Inspect files and processes from a throwaway container sharing namespaces: `docker run --rm -it --pid=container:garage --net=container:garage alpine sh`. Inside, the Garage filesystem is under `/proc/1/root/`, for example `cat /proc/1/root/etc/garage.toml`, read-only. Shared networking lets curl and netstat behave as if run inside the container.
- Last resort: build your own image, such as `FROM debian:bookworm-slim` with `COPY --from=dxflrs/garage:v2.5.0 /garage /garage` and `ENTRYPOINT ["/garage"]`. This brings back the size and attack surface the page wants to avoid, so use it temporarily.

The page notes that the image is only a few MB, a deliberate choice that also reduces its attack surface.

## Checked

2026-11-04. Read the Debugging the Docker container page in full. Confirmed the FROM scratch image, the four debugging approaches, the /proc/1/root path, the read-only note and the example Dockerfile. Nothing removed.
Method: documentation only; no commands were run.
