---
id: computing-software.devops-ci-cd.dagger.custom-runner-and-runtimes
name: custom-runner-and-runtimes
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, custom-runner, container-runtime, docker, podman, nerdctl, apple-container, gpu]
level: practitioner
status: docs-checked
description: "Point the Dagger CLI at a custom engine via _EXPERIMENTAL_DAGGER_RUNNER_HOST, pick a container runtime (Docker, Podman, nerdctl) and enable GPU."
sources: [https://docs.dagger.io/0.21/reference/configuration/custom-runner, https://docs.dagger.io/0.21/reference/container-runtimes, https://docs.dagger.io/0.21/reference/container-runtimes/podman, https://docs.dagger.io/0.21/reference/container-runtimes/nerdctl, https://docs.dagger.io/0.21/reference/container-runtimes/docker, https://docs.dagger.io/0.21/reference/container-runtimes/apple-container]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom runner and container runtimes

Goal: control where the Dagger Engine (the runner) executes: auto-provisioned in a local runtime, or your own engine. Dagger 0.21 docs.

## Default behaviour

The CLI detects an available OCI runtime on the host (Docker, Podman, nerdctl/finch, Apple `container`), downloads the engine image matching its own version, starts it in a container and connects. The same runtime backs `Host.containerImage` (load an image into the engine) and `Container.exportImage` (export to the host).

## Custom runner

Use the same engine version as your CLI/SDK. Image: `registry.dagger.io/engine:v<version>`. Requirements: root capabilities (e.g. `--privileged`), a volume at `/var/lib/dagger` (otherwise very slow, because overlayfs is needed), and the default entrypoint with no extra args.

Then export the experimental variable, accepted forms:

- `container://<name>` or `container+podman://<name>`
- `image://<image ref>` or `image+podman://registry.dagger.io/engine:latest`
- `kube-pod://<pod>?context=<ctx>&namespace=<ns>&container=<c>` (query params optional)
- `unix://<socket path>`
- `tcp://<address:port>`

Dagger adds no encryption; use a transport that provides it, or queries travel in plaintext.

## Runtime notes

- Docker: confirm with `docker info`; after `dagger core version` a `dagger-engine-v<version>` container is running.
- Podman: must be rootful; the default pids limit (2048) is low for the engine, so raise it. Podman Desktop on Mac and RHEL 8.x may need `modprobe iptable_nat` (on Mac via `podman machine ssh podman-machine-default`).
- nerdctl/finch: unprivileged use requires nerdctl in rootless mode. With lima, create `/usr/local/bin/nerdctl` containing `lima nerdctl "$@"` under a `#!/bin/sh` line.
- Apple `container`: experimental; run `container system start` first.

## GPU (experimental, NVIDIA only)

Needs a GPU-enabled runner and the NVIDIA Container Toolkit:

```shell
VERSION=$(dagger version | cut -d' ' -f2)
docker rm -f dagger-engine-${VERSION} 2>/dev/null && docker run --gpus all -d --privileged -e _EXPERIMENTAL_DAGGER_GPU_SUPPORT=true --name dagger-engine-${VERSION} registry.dagger.io/engine:${VERSION}-gpu -- --debug
```

Check with `dagger -m github.com/samalba/dagger-modules/nvidia-gpu call has-gpu`, which returns `true` when configured. The page also shows Fly.io (`deploy-dagger-on-fly`, exports a `tcp://` runner host; undo with `unset` plus `destroy-dagger-on-fly`) and Lambda Labs (same docker command; on the default `ubuntu` user run `sudo usermod -aG docker ubuntu` and restart the shell).

## Gotchas

- `_EXPERIMENTAL_DAGGER_RUNNER_HOST` is experimental and may change.
- Engine config files: computing-software.devops-ci-cd.dagger.engine-config-cache-gc. Kubernetes: computing-software.devops-ci-cd.dagger.deploy-kubernetes-openshift.

## Checked

2026-11-07

Read in full from the docs source: reference/configuration/custom-runner.mdx and reference/container-runtimes pages. Connection formats and runtime notes matched. No corrections needed.

Method: documentation only; no commands were run.
