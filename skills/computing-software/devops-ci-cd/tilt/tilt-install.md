---
id: computing-software.devops-ci-cd.tilt.tilt-install
name: tilt-install
category: computing-software
field: devops-ci-cd
product: tilt
tags: [install, tilt]
level: intro
status: docs-checked
description: "Install Tilt on macOS, Linux, or Windows, set up Docker, kubectl and a local Kubernetes cluster, and verify with tilt version."
sources:
  - "https://docs.tilt.dev/install.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Tilt

Goal: a working `tilt` binary plus Docker, kubectl and a local Kubernetes cluster.

## Prerequisites

- Docker, to build containers
- kubectl, to get information about your cluster
- A local Kubernetes cluster (on macOS and Windows, Docker for Desktop works for this)

## macOS and Windows

Docker for Mac / Docker for Windows contains Docker, kubectl, and a Kubernetes cluster.

1. Install Docker for Mac or Docker for Windows.
2. In the preferences, click Enable Kubernetes.
3. Make it your local cluster: `kubectl config use-context docker-desktop`
4. Install Tilt. macOS: `curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash`. Windows PowerShell: `iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))`

On Windows, if Scoop is installed the installer uses it. Otherwise add the `tilt` install directory to your $PATH (or create an alias).

## Linux

1. Install Docker and set it up as a non-root user.
2. Install kubectl.
3. Install ctlptl and use it to create Kind with a local registry.
4. Run the same install.sh one-liner as macOS.

Ubuntu users sometimes prefer Microk8s instead of Kind.

## Alternatives

The installer first checks for a package manager. You can also use:

```bash
brew install tilt
```

```bash
scoop bucket add tilt-dev https://github.com/tilt-dev/scoop-bucket
scoop install tilt
```

```bash
conda config --add channels conda-forge
conda install tilt
```

```bash
asdf plugin add tilt
asdf install tilt 0.37.8
asdf global tilt 0.37.8
```

Manual install: the installer otherwise downloads a static binary into `~/.local/bin`, `/usr/local/bin`, or `~/bin` depending on OS and $PATH. Specific versions are on Tilt's GitHub Releases page.

## Verify

```bash
tilt version
```

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Install page in full (prerequisites, macOS, Linux, Windows, Verify, Alternative Installations). Confirmed prerequisites, the install one-liners, Scoop handling, the ctlptl and Kind step, Microk8s note, the four package-manager commands, binary locations and `tilt version`. Fixed: step 1 said to install Docker Desktop, but the page names Docker for Mac and Docker for Windows, so the skill now uses those names. Not opened: the Docker install pages linked from it. 

Method: documentation only; no commands were run.
