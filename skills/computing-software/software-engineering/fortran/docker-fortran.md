---
id: computing-software.software-engineering.fortran.docker-fortran
name: docker-fortran
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, docker-fortran, fortran-containers-ci]
level: practitioner
status: draft
description: "Build reproducible Fortran images with gfortran, fpm or CMake, multi-stage builds and a small runtime image."
sources:
  - https://docs.docker.com/
  - https://github.com/fortran-lang/setup-fortran
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Docker images for Fortran builds
**Goal:** containerise Fortran builds.
```dockerfile
FROM debian:stable-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends gfortran cmake make \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY . .
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j
FROM debian:stable-slim
RUN apt-get update && apt-get install -y --no-install-recommends libgfortran5 && rm -rf /var/lib/apt/lists/*
COPY --from=build /src/build/app /usr/local/bin/app
USER 10001
ENTRYPOINT ["/usr/local/bin/app"]
```
- Runtime image needs `libgfortran` (and `libgomp` for OpenMP) unless linked statically.
- Pin base image digests for reproducibility; run as non-root.
## Gotchas
- `-march=native` baked at build time may not match the deployment CPU.
- Package name for libgfortran varies by distribution release (libgfortran5 on current Debian-family; verify).
## Self-check
`docker build` then `docker run` and confirm the result matches the local build.
