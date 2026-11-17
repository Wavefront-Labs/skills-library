---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-supported-platforms
name: woodpecker-supported-platforms
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [platforms, backends, architectures]
level: practitioner
status: docs-checked
description: "Check which OS and architecture each Woodpecker component and backend supports."
sources: ["https://woodpecker-ci.org/docs/administration/installation/supported-platforms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker supported platforms

Woodpecker ships as container images and pre-built binaries. The server and Docker/Kubernetes backends are Linux-centric, while the agent and CLI run on more operating systems through the Local backend.

Components: `woodpecker-server` (UI, API, webhook receiver, scheduler), `woodpecker-agent`, `woodpecker-cli`, and `plugin-git` (the default clone plugin, run as a container; binaries exist for the Local backend).

Highlights of the matrix:

- linux/amd64 and linux/arm64: image and binary for server, agent, CLI and plugin-git.
- Windows amd64: binaries for server, agent, CLI and plugin-git.
- macOS (Intel and Apple Silicon): agent, CLI and plugin-git binaries; no server.
- FreeBSD amd64: server, agent, CLI images and binaries.
- OpenBSD: agent, CLI and plugin-git binaries.

Backend support: Docker works on Linux, and on Windows through WSL2 with Docker Desktop or native Windows containers. Kubernetes works on Linux only. Local works everywhere, and is the only backend on macOS and OpenBSD. FreeBSD Docker support is work in progress.

DEB and RPM packages are built for linux/amd64 and linux/arm64.

On hosts without Docker or Kubernetes, use the `plugin-git` binary with the Local backend, or disable the clone step and clone manually.

## Checked

2026-11-03. Confirmed against: supported-platforms (components, matrix, backend table, packages, plugin-git note). Removed: nothing.

Method: documentation only; no commands were run.
