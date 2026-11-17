---
id: computing-software.cloud-infrastructure-engineering.docker.running-wasm-workloads-with-containerd-shims
name: running-wasm-workloads-with-containerd-shims
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, runtime, wasm-containers, runwasi, wasmtime, wasmedge, containerd-shim, wasi]
level: advanced
status: docs-checked
description: "Run WebAssembly containers through containerd runwasi shims: Docker Desktop Wasm setup, installing shims on Engine, --runtime and --platform wasi/wasm flags, and limits."
sources: ["https://docs.docker.com/desktop/features/wasm/", "https://docs.docker.com/engine/daemon/alternative-runtimes/", "https://github.com/containerd/runwasi"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Wasm workloads with containerd shims

Docker runs Wasm modules by handing them to a containerd shim (from the runwasi project)
instead of runc. The image is a scratch image containing the `.wasm` file (see the Wasm OCI
artifact skill).

## Docker Desktop
The Docker docs mark Wasm workloads in Docker Desktop as deprecated (to be removed in a future release, no longer actively maintained).
1. Settings > General: enable "Use containerd for pulling and storing images".
2. Settings > Beta features: enable "Enable Wasm". Desktop installs the runtimes
   `io.containerd.slight.v1`, `io.containerd.spin.v2`, `io.containerd.wasmedge.v1`, `io.containerd.wasmtime.v1`,
   `io.containerd.lunatic.v1`, `io.containerd.wws.v1` and `io.containerd.wasmer.v1`.
```bash
docker run --rm --runtime=io.containerd.wasmedge.v1 --platform=wasi/wasm \
  secondstate/rust-example-hello
```

## Docker Engine on Linux
- Enable the containerd image store (`"features": {"containerd-snapshotter": true}`).
- Restart the Docker daemon, then install the shim binary on `PATH` (the Docker docs build
  `containerd-shim-wasmtime-v1` from the containerd/runwasi `containerd-shim-wasmtime` crate).
- With the shim on `PATH`, reference it by its fully qualified name:
```bash
docker run --rm --runtime io.containerd.wasmtime.v1 --platform wasi/wasm32 michaelirwin244/wasm-example
```
(the Engine example in the docs uses `wasi/wasm32`; the Desktop page uses `wasi/wasm`).
- A shim that is not on `PATH` can be registered by path, and shim options go under `options`:
```json
{
  "runtimes": {
    "foo": { "runtimeType": "/path/to/containerd-shim-foobar-v1" }
  }
}
```
```bash
docker run --rm --runtime foo hello-world
```
Reload the daemon with `systemctl reload docker` after editing `daemon.json`.

## Compose
```yaml
services:
  app:
    image: reg.example.com/app-wasm:1.0
    platform: wasi/wasm
    runtime: io.containerd.wasmtime.v1
```

## Limits to know
- The Wasm runtime provides sandboxing in addition to container isolation, but features vary per shim and runtime;
  test your module with the specific shim and pin its version.
- Build the image `FROM scratch` with the `.wasm` file as the `ENTRYPOINT` and build with
  `docker buildx build --platform wasi/wasm`.

## Verify
```bash
docker info -f '{{json .Runtimes}}'
docker inspect -f '{{.HostConfig.Runtime}}' <container>
docker image inspect -f '{{.Os}}/{{.Architecture}}' reg.example.com/app-wasm:1.0   # wasi/wasm
```

## Checked
Documentation release: Docker docs (Wasm workloads in Docker Desktop, alternative container runtimes; docker/docs main 2026-10-23) and containerd/runwasi (latest release containerd-shim-wasmtime v0.6.1), checked 2026-10-26.
Confirmed: containerd image store required; Desktop setting names and the installed runtime list; `--runtime` and `--platform` flags; Compose `platform` and `runtime` keys; Engine steps (`features.containerd-snapshotter`, daemon restart, shim on `PATH`, `runtimeType` path registration, `systemctl reload docker`); Wasm deprecation notice for Docker Desktop; Dockerfile and buildx pattern for `wasi/wasm`.
Corrected: Desktop setting is under "Beta features"; the Engine registration with `runtimeType` set to a runtime name is replaced by the documented shim-on-`PATH` and path forms; the `--platform` value is `wasi/wasm32` in the Engine example.
Removed as unsupported: WASI preview 1 socket and HTTP claims, "no docker exec" and filesystem limits, Kubernetes RuntimeClass usage, and `jq` key listing.
Method: documentation only; no commands were run.
