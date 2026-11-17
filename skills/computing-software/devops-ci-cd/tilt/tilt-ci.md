---
id: computing-software.devops-ci-cd.tilt.tilt-ci
name: tilt-ci
category: computing-software
field: devops-ci-cd
product: tilt
tags: [ci, tilt, tilt-ci, kind, ctlptl]
level: practitioner
status: docs-checked
description: "Run tilt ci in CI to build images and verify servers start, debug it with the Session object, and choose a single-use Kubernetes cluster."
sources:
  - "https://docs.tilt.dev/ci.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt in CI

Goal: on every change, verify images build and servers start. You need `tilt ci` plus a Kubernetes cluster in CI.

## What `tilt ci` does

1. Executes the Tiltfile.
2. Runs all `local_resource` commands.
3. Builds all images.
4. Deploys all Kubernetes resources.
5. Waits until everything is healthy.

It streams logs to the terminal (the web UI is still available at `http://localhost:10350/`). Any failed step, crashed resource, or resource that looks like it will never succeed (for example a pod slow to schedule) exits with an error code. When all services are healthy it exits 0. Port-forwards are not active after exit.

## Debugging a wait

```
tilt describe session
tilt get session -o yaml
tilt get session -o json
```

The Session status shows the Tilt PID, start time, and each awaited target with its state (waiting, running or terminated).

## Cluster options

- Easiest, VM-based CI: create a VM, install dependencies including Docker, create a `kind` cluster with a local registry at `localhost:5000` (kind's local-registry script). Tilt auto-detects that registry and pushes there. Downside: VMs are slower and heavier to upgrade.
- Recommended, remote Docker-based CI: container with your code, a remote Docker environment, a `kind` cluster with local registry inside it, and `socat` to expose the registry and cluster to the container. `ctlptl` will try to detect a remote Docker environment and set up the `socat` forwarding automatically.
- Not recommended, remote registry: needs a dedicated CI registry, a service account or token secret, and `kind`. Secrets and permissions are painful, and it is hard to guarantee images do not leak between tests. It may be the only option if you cannot change where tools push and pull images.

Most Tilt example projects run `tilt ci` on CircleCI and use `ctlptl` to create a single-use cluster.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/ci.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). Softened ctlptl socat detection to "will try to detect", as the page words it.

Method: documentation only; no commands were run.
