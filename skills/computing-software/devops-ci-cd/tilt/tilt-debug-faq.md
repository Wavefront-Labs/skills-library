---
id: computing-software.devops-ci-cd.tilt.tilt-debug-faq
name: tilt-debug-faq
category: computing-software
field: devops-ci-cd
product: tilt
tags: [debug-faq, tilt]
level: practitioner
status: docs-checked
description: "Diagnose a broken Tilt with tilt doctor, snapshots, tilt docker, pprof profiles, tilt dump engine, and the experimental_telemetry_cmd function."
sources:
  - "https://docs.tilt.dev/debug_faq.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Why is Tilt broken?

Goal: pick the right diagnostic for a Tilt problem.

## Crash on startup

```shell
tilt doctor
```

Prints Tilt version, operating system, Docker host and version, Kubernetes version, type of Kubernetes cluster, and container runtime. It is usually the first thing the team asks for in issues.

## Info to send when you need help

A snapshot is a link that lets someone interactively explore a frozen moment-in-time copy of your Tilt UI (services, alerts, Kubernetes events). Attach it to bug reports. See the snapshots guide.

## Image build fails in Tilt but not with docker build

```shell
tilt docker -- build ARGS
```

Runs Docker the way Tilt does. For example with minikube, `tilt docker -- build -t image-name .` may print a `DOCKER_HOST=tcp://... docker build -t image-name .` line because Tilt runs against Minikube's Docker instance.

## High CPU or memory

File an issue. As of v0.10.26 Tilt exposes Go pprof hooks over HTTP:

```shell
go tool pprof http://localhost:10350/debug/pprof/profile?seconds=30
go tool pprof http://localhost:10350/debug/pprof/heap
```

Type `web` in the REPL to see a CPU graph.

## What does Tilt think is happening?

Tilt's engine is a control loop like Kubernetes: it watches your Tiltfile, local source files, and the cluster, records changes in a central state store, and kicks off updates from it. With Tilt running, in another terminal:

```shell
tilt dump engine
tilt dump webview
```

The first prints JSON of all build and cluster state; the second the complete state of the web UI.

## Tracking team usage

`experimental_telemetry_cmd` takes a shell command that Tilt execs every minute, passing newline-separated JSON OpenTelemetry spans of the last minute's activity on STDIN:

```python
experimental_telemetry_cmd("/path/to/honeycomb_ingest.py")
experimental_telemetry_cmd("docker run --env USER -i my-telemetry-image")
```

It is experimental and designed for larger companies.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/debug_faq.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed. `experimental_telemetry_cmd` is documented on this guide only, not in the Tiltfile API page.

Method: documentation only; no commands were run.
