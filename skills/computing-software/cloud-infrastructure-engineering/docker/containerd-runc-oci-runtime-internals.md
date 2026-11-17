---
id: computing-software.cloud-infrastructure-engineering.docker.containerd-runc-oci-runtime-internals
name: containerd-runc-oci-runtime-internals
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, containerd, runc, oci, oci-runtime-spec, oci-image-spec, shim, containerd-shim-runc-v2, ctr, crictl, cri, dockerd, moby, runtime-v2, namespaces, cgroups, pivot_root, state-json, task, exec-form, gvisor, kata-containers, crun, oci-hooks]
level: advanced
status: docs-checked
description: "What actually runs a container below dockerd: containerd, containerd-shim, runc, and the OCI runtime/image specs, plus how to inspect and debug each layer."
sources: ["https://docs.docker.com/engine/daemon/alternative-runtimes/", "https://docs.docker.com/engine/daemon/live-restore/", "https://github.com/containerd/containerd/blob/main/docs/namespaces.md", "https://github.com/opencontainers/runtime-spec/blob/main/config.md", "https://github.com/opencontainers/image-spec/blob/main/manifest.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# containerd / runc / OCI — what actually runs a container

**Goal:** know what's below `dockerd` so you can debug a container that `docker` itself
can't explain, read `ctr`/`crictl` output, and understand why "docker restart" doesn't
kill your long-running process.

## The stack
`docker` CLI -> `dockerd` (API, image build, networking, volumes) -> `containerd` (image
pull/unpack, snapshotters, lifecycle) -> a containerd shim (`containerd-shim-runc-v2`, one per
container) -> `runc` (the OCI runtime that creates the container's namespaces and cgroups and
starts the process). Docker's docs describe alternative runtimes as either containerd shims
(runtimes that ship their own shim) or drop-in replacements for runc that use the runc shim.
By default, when the Docker daemon terminates it shuts down running containers; enable
`"live-restore": true` in `daemon.json` to keep containers running while the daemon is unavailable
(not supported for Windows containers).

## OCI Runtime Spec
A "container" to runc is a directory with a `config.json` (the OCI runtime spec: namespaces
to create, mounts, cgroup path, capabilities, seccomp profile, hooks) plus a root filesystem.
`runc` subcommands such as `create`, `start`, `kill`, `delete`, `list` and `state` are what a runc-based
shim drives. You rarely invoke `runc` directly against Docker containers; `runc` takes a `--root` flag for its state
directory, so point it at the root your containerd uses before running `runc list`.

## OCI Image Spec
An image is a manifest (JSON) pointing to a config blob and an ordered list of layer blobs
(usually gzip'd tarballs, `application/vnd.oci.image.layer.v1.tar+gzip`), addressed by
content digest. A manifest *list* (index) maps platforms to per-arch manifests — this is
what `docker buildx imagetools inspect` and multi-arch pulls read. `docker save`/`load`
round-trip images as a tarball.

## containerd namespaces and inspecting directly
containerd has its own namespace concept (unrelated to Linux namespaces) separating
callers (nerdctl lists namespaces such as `default`, `moby` and `k8s.io`; `moby` is Docker's and
`k8s.io` is the CRI's). Image names and metadata are separate per namespace, and namespaces are an
administrative construct, not a security feature.
```
sudo ctr --namespace moby containers list
sudo ctr --namespace moby tasks list
sudo crictl ps          # CRI endpoint required (Kubernetes nodes, not plain Docker)
```
`ctr` is deliberately low-level (no restart policies, no networking setup) — useful for
proving "is this a Docker problem or a containerd problem" but not a Docker CLI replacement.

## Swappable runtimes
runc is the default OCI runtime but not the only one. Per the Docker docs, a runtime that ships a
containerd shim (for example Kata via `io.containerd.kata.v2`, Wasmtime) needs no daemon
configuration once the shim is on `PATH`: `docker run --runtime io.containerd.kata.v2 hello-world`. To pass
shim options or use a shim that is not on `PATH`, register it in `/etc/docker/daemon.json` with a
`runtimeType`:
```json
{ "runtimes": { "gvisor": { "runtimeType": "io.containerd.runsc.v1",
    "options": { "TypeUrl": "io.containerd.runsc.v1.options", "ConfigPath": "/etc/containerd/runsc.toml" } } } }
```
Runtimes that are drop-in replacements for runc (youki is the documented example) use the `path` key:
`{ "runtimes": { "youki": { "path": "/usr/local/bin/youki" } } }`. Reload with `systemctl reload docker`,
then `docker run --runtime <name> ...`. Verify each runtime against your workload before using it in production.

## Gotchas
- Stop containers before removing Docker or containerd state directories; deleting data under a running
  daemon leaves the layers inconsistent.
- OCI runtime-spec `config.json` supports lifecycle hooks (`createRuntime`, `createContainer`,
  `startContainer`, `poststart`, `poststop`; `prestart` is deprecated), which tools use to modify containers
  at creation time.

## Verify
`sudo ctr --namespace moby tasks list` shows the running containers that `docker ps` shows,
with PIDs; if they disagree, the inconsistency is between layers, not in your application.

## Checked
Documentation release: Docker docs (alternative runtimes, live restore; docker/docs main 2026-10-23), containerd v2.4.2 docs and nerdctl v2.4.1 command reference (namespaces), opencontainers/runtime-spec config.md, checked 2026-10-26.
Confirmed: default daemon shutdown stops containers and `live-restore` option; shim vs runc-replacement runtime registration forms (`runtimeType`, `options.TypeUrl`, `ConfigPath`, `path`) and `systemctl reload docker`; `--runtime io.containerd.kata.v2`; containerd namespaces `default`, `moby`, `k8s.io`, per-namespace metadata and "not a security feature"; OCI layer media type.
Corrected: `systemctl restart docker` does not keep containers running by default (needs live-restore); gVisor registration uses `runtimeType` with the shim, not `path`.
Removed as unsupported: "since ~18.09", the `/run/containerd/runc/...` state path and `--root` value, `skopeo`/`crane` mentions, performance and compatibility remarks about gVisor, Kata and crun, the zombie-shim and nvidia-container-runtime paragraphs.
Method: documentation only; no commands were run.
