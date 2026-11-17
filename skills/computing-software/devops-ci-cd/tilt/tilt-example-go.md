---
id: computing-software.devops-ci-cd.tilt.tilt-example-go
name: tilt-example-go
category: computing-software
field: devops-ci-cd
product: tilt
tags: [example-go, tilt, golang, live-update]
level: practitioner
status: docs-checked
description: "Speed up the Tilt feedback loop for a Go server: baseline Tiltfile, local go build with only=, and live_update with restart_process."
sources:
  - "https://docs.tilt.dev/example_go.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Go with Tilt

Goal: shorten code-change-to-new-process time for a Go server (example repo: tilt-example-go).

## Step 0: simplest deployment

```python
docker_build('example-go-image', '.', 
    dockerfile='deployments/Dockerfile')
k8s_yaml('deployments/kubernetes.yaml')
k8s_resource('example-go', port_forwards=8000)
```

The image name must match the Deployment's container `image`; the resource name must match `metadata.name`. Server at `localhost:8000`.

## Step 1: measure

A `local_resource` runs a script that records start time, and the server prints elapsed time. Naive: 4.2s.

```python
k8s_resource(
    'example-go', 
    port_forwards=8000, 
    resource_deps=['deploy'])
local_resource(
    'deploy',
    './record-start-time.sh',
)
```

## Step 2: compile locally (3.5s)

The naive build copies source, downloads `gorilla/mux`, and compiles from scratch every time. Instead compile on the host and keep only the binary and web files in the build context:

```python
local_resource(
  'example-go-compile',
  'CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o build/tilt-example-go ./',
  deps=['./main.go', './start.go'],
  resource_deps = ['deploy'])
  
docker_build(
  'example-go-image',
  '.',
  dockerfile='deployments/Dockerfile',
  only=[
    './build',
    './web',
  ])
```

The Dockerfile copies only `./build` and `./web`, so other changes do not trigger builds.

## Step 3: live update (1.5s)

```python
load('ext://restart_process', 'docker_build_with_restart')
docker_build_with_restart(
  'example-go-image',
  '.',
  entrypoint='/app/build/tilt-example-go',
  dockerfile='deployments/Dockerfile',
  only=[
    './build',
    './web',
  ],
  live_update=[
    sync('./build', '/app/build'),
    sync('./web', '/app/web'),
  ],
)
```

The `sync` steps copy into the container; `docker_build_with_restart` (restart_process extension) re-executes `entrypoint`. It is a lowest-common-denominator reload tool.

## CI

Run `tilt ci` against a single-use cluster created with `ctlptl`.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/example_go.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
