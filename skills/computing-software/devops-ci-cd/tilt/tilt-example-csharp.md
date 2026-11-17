---
id: computing-software.devops-ci-cd.tilt.tilt-example-csharp
name: tilt-example-csharp
category: computing-software
field: devops-ci-cd
product: tilt
tags: [example-csharp, tilt, csharp, live-update]
level: practitioner
status: docs-checked
description: "Speed up the Tilt feedback loop for an ASP.NET Core C# server: baseline Tiltfile, local dotnet publish, and live_update with restart_process."
sources:
  - "https://docs.tilt.dev/example_csharp.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C# with Tilt

Goal: shorten the time from code change to new process for an ASP.NET Core server on Kubernetes (example repo: tilt-example-csharp).

## Step 0: simplest deployment

Needs a Dockerfile, a Kubernetes Deployment, and a Tiltfile:

```python
docker_build('hello-tilt', './hello-tilt')
k8s_yaml('kubernetes.yaml')
k8s_resource('hello-tilt', port_forwards='8080:80')
```

The `docker_build` image name must match the Deployment's container `image`; the `k8s_resource` name must match the Deployment's `metadata.name`. The server is reachable at `localhost:8080`.

## Step 1: measure

A `local_resource` records the start time; the server shows elapsed time. Naive deploy: 10.4s.

```python
local_resource(
    'deploy',
    './record-start-time.sh',
    deps=['./record-start-time.sh']
)
```

## Step 2: compile locally

Compile with `dotnet` on the host, and build the image from only the output directory (8.2s):

```python
local_resource(
    'build',
    'dotnet publish -c Release -o out',
    deps=['hello-tilt'],
    ignore=['hello-tilt/obj'],
    resource_deps=['deploy'],
)
docker_build('hello-tilt', 'out', dockerfile='Dockerfile')
```

```dockerfile
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1
COPY . /app/out
WORKDIR /app/out
ENTRYPOINT ["dotnet", "hello-tilt.dll"]
```

## Step 3: live update (4.8s)

```python
load('ext://restart_process', 'docker_build_with_restart')
docker_build_with_restart(
    'hello-tilt',
    'out',
    entrypoint=['dotnet', 'hello-tilt.dll'],
    dockerfile='Dockerfile',
    live_update=[
        sync('out', '/app/out'),
    ],
)
```

`sync` copies build output into the container; `docker_build_with_restart` (restart_process extension) re-executes `entrypoint` after a live update. It is a lowest-common-denominator reload tool.

## CI

Run `tilt ci` against a single-use cluster created with `ctlptl`.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/example_csharp.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
