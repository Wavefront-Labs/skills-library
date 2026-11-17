---
id: computing-software.devops-ci-cd.forgejo.runner-labels-docker-lxc-host
name: runner-labels-docker-lxc-host
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [runner-labels, runs-on-label, label-types, pinned-images]
level: practitioner
status: docs-checked
description: "Define runner labels as name:type://image and choose docker, lxc or host execution for each."
sources:
  - https://forgejo.org/docs/latest/admin/actions/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Labels must be defined in the runner configuration file to say which jobs the runner executes; Forgejo inspects a job's `runs-on` field to evaluate which runners can run it. In the runner config:

```
runner:
  labels:
    - debian:docker://docker.io/library/node:lts
    - ubuntu-latest:docker://ghcr.io/catthehacker/ubuntu:act-22.04
```

Structure: `<label-name>:<label-type>://<default-image>`. The name is what workflows put in `runs-on`. Types: `docker` (Docker or Podman), `lxc`, and `host` (no containerization).

Docker/Podman: the runner does the equivalent of `docker run <image>`, so downloaded images are never updated. Steps run as root in the container. The page recommends pinning image versions (for example by `@sha256:` digest) instead of relying on tags, a prerequisite for reproducible jobs. Many common actions, such as `actions/checkout@v7`, need Node.js in the image. A workflow can override the image with `jobs.<job_id>.container`. A label like `ubuntu-latest:docker://node:lts` mimics GitHub names but lacks GitHub's tool set.

LXC: `template[:release[:lxc-helper config]]`, default template `debian` and release `bullseye`.

Host: for example `self-hosted:host`, with no isolation at all.

## Checked

Date: 2026-11-07
Confirmed against the "Forgejo Runner Configuration" page (Choosing labels, Docker or Podman, LXC and Host sections), read in full along with the rest of the page: the `runner.labels` example, the `<label-name>:<label-type>://<default-image>` structure, the three label types, `docker run <image>` and never-updated images, steps as root, the pinning advice, Node.js for common actions, the `jobs.<job_id>.container` override, the GitHub-mimicking `ubuntu-latest` label, the LXC `template[:release[:lxc-helper config]]` format with defaults `debian` and `bullseye`, and the `self-hosted:host` example with no isolation.
Corrected: removed the claim that labels are "the minimum runner configuration" (not stated); reworded the pinning advice to what the page says; removed a duplicated closing paragraph that also tied pinning to never-updated images, which the page does not link.
Method: documentation only; no commands were run.
