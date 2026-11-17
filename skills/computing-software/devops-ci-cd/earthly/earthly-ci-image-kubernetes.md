---
id: computing-software.devops-ci-cd.earthly.earthly-ci-image-kubernetes
name: earthly-ci-image-kubernetes
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, ci-image, earthly-earthly, tmp-earthly, cgroups-v2, kubernetes, privileged, earthly-tmp-dir]
level: advanced
status: docs-checked
description: "Build a custom CI image from earthly/earthly or add earthly to an image, mount /tmp/earthly, handle cgroups v2, and run earthly/earthly on Kubernetes in privileged mode."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/build-an-earthly-ci-image.md
  - https://github.com/earthly/earthly/blob/main/docs/ci-integration/guides/kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom Earthly CI image and Kubernetes

## Extend earthly/earthly (recommended)
```docker
FROM earthly/earthly:v0.8.13
RUN ... # Add your agent, certificates, tools...
```
Pin the version. The image is Alpine-based, so add tools with `apk add --no-cache my-cool-tool`; Alpine uses musl, which can break some software. Embed needed configuration with the `earthly config` command rather than in build scripts.

## Add earthly to an existing image
Docker-in-Docker: install the binary and bootstrap (pin the version):
```docker
RUN wget https://github.com/earthly/earthly/releases/download/v0.8.13/earthly-linux-amd64 -O /usr/local/bin/earthly && \
    chmod +x /usr/local/bin/earthly && \
    /usr/local/bin/earthly bootstrap
```
Remote daemon: install the same way, then set the host with `earthly config global.buildkit_host ...`.

## Mount /tmp/earthly
Unless you use a remote daemon, BuildKit runs in the same container, so mount `/tmp/earthly` as a Docker volume; otherwise expect excess disk use, slowness or malfunction. Without it you may see "rm: can't remove '/var/earthly/dind/...': Resource busy". On EKS, users reported that an EBS volume worked instead of a Kubernetes `emptyDir`.

## cgroups v2 with a custom entrypoint
The default entrypoint moves itself to an isolated cgroup. A custom entrypoint must do so before buildkitd starts, else it fails with `sh: write error: Resource busy`:
```bash
if [ -f "/sys/fs/cgroup/cgroup.controllers" ]; then
    mkdir -p /sys/fs/cgroup/my-entrypoint
    echo "$$" > /sys/fs/cgroup/my-entrypoint/cgroup.procs
fi
```

## Kubernetes (earthly/earthly only)
The pod must be privileged:
```yaml
securityContext:
  privileged: true
volumeMounts:
  - mountPath: /tmp/earthly
    name: buildkitd-temp
volumes:
  - name: buildkitd-temp
    emptyDir: {}
```
Change that path with `EARTHLY_TMP_DIR`; source is expected in the default working directory `/workspace`. With Calico, set `CNI_MTU` if the network MTU mismatches. Taints and tolerations can isolate privileged pods.

## Gotcha
Multi-node `earthly/buildkitd` setups are unsupported.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: ci-integration/build-an-earthly-ci-image.md, ci-integration/guides/kubernetes.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: the EKS EBS note is now attributed to user reports, as on the page.

Method: documentation only; no commands were run.
