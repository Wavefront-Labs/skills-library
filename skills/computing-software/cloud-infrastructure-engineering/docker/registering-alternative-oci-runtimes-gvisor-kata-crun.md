---
id: computing-software.cloud-infrastructure-engineering.docker.registering-alternative-oci-runtimes-gvisor-kata-crun
name: registering-alternative-oci-runtimes-gvisor-kata-crun
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, runtime, runc, crun, gvisor, kata, runsc, runtime-registration, kata-runtime, kata-setup, crun-vs-runc, sandboxing]
level: advanced
description: "Register gVisor runsc, Kata Containers and crun as Docker runtimes in daemon.json, select them per container with --runtime, and know each one's trade-offs."
sources: ["https://docs.docker.com/engine/daemon/alternative-runtimes/", "https://docs.docker.com/reference/cli/dockerd/", "https://gvisor.dev/docs/user_guide/platforms/", "https://github.com/google/gvisor/blob/master/g3doc/user_guide/quick_start/docker.md", "https://github.com/kata-containers/kata-containers", "https://kubernetes.io/docs/concepts/containers/runtime-class/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registering alternative OCI runtimes (gVisor, Kata, crun)

## daemon.json
```json
{
  "runtimes": {
    "runsc": { "path": "/usr/local/bin/runsc", "runtimeArgs": ["--platform=systrap"] },
    "crun":  { "path": "/usr/bin/crun" },
    "kata":  { "runtimeType": "io.containerd.kata.v2" }
  },
  "default-runtime": "runc"
}
```
`systemctl reload docker` (`runtimes` and `default-runtime` are on the daemon's reloadable list). Use per container:
```sh
docker run --runtime=runsc --rm alpine dmesg       # gVisor prints "Starting gVisor..."
docker run --runtime=kata --rm alpine uname -r     # guest VM kernel version
```
Compose: `runtime: runsc`. `docker info -f '{{json .Runtimes}}'` lists what's registered.

Docker uses runc by default through containerd. A runtime with its own containerd shim (Wasmtime, gVisor,
Kata Containers) needs no daemon config if the shim binary is on `PATH`: `docker run --runtime
io.containerd.kata.v2 hello-world`. `runtimeType` in daemon.json registers a shim under a name (with
`options` such as gVisor's `TypeUrl` and `ConfigPath`); `path` registers a runc drop-in replacement (with
optional `runtimeArgs`) that is invoked through the runc shim.

## gVisor (runsc)
- Install: `sudo runsc install` adds a runtime named `runsc` to the Docker configuration; restart the
  Docker daemon afterwards (gVisor's guide).
- Platforms: `runsc` takes `--platform`; `systrap` is the default (it replaced `ptrace` in mid-2023). KVM is
  best on bare metal; inside a VM `systrap` often performs better, and KVM needs `/dev/kvm` access.
  Several runtimes with different platforms can be registered side by side (`runsc-kvm`, `runsc-systrap`).
- Debug: `"runtimeArgs": ["--debug-log=/tmp/runsc/", "--debug"]` (a trailing `/` makes it a directory).

## Kata Containers
- Runs workloads in lightweight virtual machines with their own guest kernel (hypervisor choices are in
  the Kata hypervisors document).
- `kata-runtime check` verifies that the host can run Kata; Kubernetes installs use the `kata-deploy` Helm chart.

## crun vs runc
- A runc drop-in replacement such as crun or youki is registered with `path` (and optional
  `runtimeArgs`); the Docker docs walk through youki, whose project claims it is faster and lighter than runc.
- runc is Docker's default; switch `"default-runtime"` only after testing your workloads.

## Gotchas
- Kubernetes selects a runtime with a `RuntimeClass` (`runtimeClassName` in the Pod spec), not Docker's
  daemon.json.

## Verify
`docker inspect -f '{{.HostConfig.Runtime}}' ctr`; inside, `dmesg` (gVisor) or a different
`uname -r` (Kata) proves the sandbox is active.

## Checked
Date: 2026-10-24. Documentation: Docker docs alternative runtimes page and `dockerd` reference (reloadable options) in docker/docs main, gVisor docs (`g3doc` quick start for Docker, platforms, debugging), Kata Containers README, Kubernetes RuntimeClass page.
- Confirmed runc as default via containerd, `--runtime` with a shim name such as `io.containerd.kata.v2`, `runtimeType`/`options` for shims, `path`/`runtimeArgs` for runc drop-ins, `runtimes` and `default-runtime` being reloadable, gVisor `runsc install`, the `--platform` flag with `systrap` default and `kvm`, the `dmesg` banner, `--debug-log` with a trailing slash, Kata `kata-runtime check` and `kata-deploy`, and `runtimeClassName`.
- Removed crun speed/default-in-Podman/Wasm claims, Kata startup-time and virtio-fs claims, Swarm per-service and Docker Desktop remarks, and gVisor performance-cost claims that no checked source covers.
Method: documentation only; no commands were run.
