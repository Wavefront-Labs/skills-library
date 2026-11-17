---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-run-container-image
name: tetragon-run-container-image
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [run-container]
level: practitioner
status: docs-checked
description: "Run the Tetragon container image without Kubernetes and configure it with CLI arguments, TETRAGON_ environment variables or mounted drop-in files."
sources:
  - "https://tetragon.io/docs/installation/container/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Run the Tetragon container image

Goal: run Tetragon as a plain container on a host without a Kubernetes cluster.

## Stable version

Pick a tag from the Tetragon quay repository (quay.io/cilium/tetragon):

```shell
docker run --name tetragon --rm -d                   \
    --pid=host --cgroupns=host --privileged          \
    -v /sys/kernel/btf/vmlinux:/var/lib/tetragon/btf \
    quay.io/cilium/tetragon:<version>
```

## Unstable development version

The `latest` tag of the Tetragon-CI repository is built from the latest commit on the Tetragon main branch:

```shell
docker run --name tetragon --rm -d                  \
   --pid=host --cgroupns=host --privileged          \
   -v /sys/kernel/btf/vmlinux:/var/lib/tetragon/btf \
   quay.io/cilium/tetragon-ci:latest
```

If Tetragon does not start because of BTF issues, see the BTF question in the FAQ.

## Configuration

There are three ways to set options; the full list is in the Tetragon daemon configuration reference.

1. CLI arguments appended after the image, for example:

```shell
docker run --name tetragon --rm -d \
    --pid=host --cgroupns=host --privileged \
    -v /sys/kernel:/sys/kernel \
    quay.io/cilium/tetragon:<version> \
    /usr/bin/tetragon --export-filename /var/log/tetragon/tetragon.log
```

2. Environment variables: prefix the setting name with `TETRAGON_` and upper-case it, so `--export-filename` becomes `TETRAGON_EXPORT_FILENAME`:

```shell
docker run --name tetragon --rm -d \
    --pid=host --cgroupns=host --privileged \
    --env "TETRAGON_EXPORT_FILENAME=/var/log/tetragon/tetragon.log" \
    -v /sys/kernel:/sys/kernel \
    quay.io/cilium/tetragon:<version>
```

3. Drop-in files in `/etc/tetragon/tetragon.conf.d/` on the host, mounted into the container:

```shell
docker run --name tetragon --rm -d \
    --pid=host --cgroupns=host --privileged \
    -v /sys/kernel:/sys/kernel \
    -v /etc/tetragon/tetragon.conf.d/:/etc/tetragon/tetragon.conf.d/ \
    quay.io/cilium/tetragon:<version>
```

## Checked

2026-11-08. Read the container deployment page in full (raw docs markdown). Checked run commands and the three configuration methods against it; no claims removed.

Method: documentation only; no commands were run.
