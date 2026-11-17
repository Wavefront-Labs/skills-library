---
id: computing-software.devops-ci-cd.tilt.tilt-tutorial-ui
name: tilt-tutorial-ui
category: computing-software
field: devops-ci-cd
product: tilt
tags: [tutorial-ui, tilt, web-ui, install]
level: intro
status: docs-checked
description: "Install Tilt and Docker for the tutorial, then use the Tilt web UI: resource overview, resource details and log filtering."
sources:
  - "https://docs.tilt.dev/tutorial/1-prerequisites.html"
  - "https://docs.tilt.dev/tutorial/3-tilt-ui.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tutorial: prerequisites and the Tilt UI

## Prerequisites

To follow along you need Docker and Tilt. Tilt can be used without Docker or Kubernetes, but the sample project uses both.

```bash
# macOS/Linux: uses Homebrew if available, otherwise a direct download
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

```powershell
# Windows: uses Scoop if available, otherwise a direct download
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

Docker has install instructions for Mac, Windows (including WSL) and Linux; a convenience script auto-detects the distribution: `curl -fsSL https://get.docker.com | sh`. On Linux, Docker's post-install guide for managing Docker as a non-root user is suggested, so you need not run Tilt with `sudo`. Test Docker with `docker run --rm hello-world`.

## Opening the UI

In the terminal running `tilt demo`, press Spacebar; the default browser opens the UI.

## Resource Overview

The first view; click the Tilt logo (upper left) to return. It shows all resources grouped by resource label, with:

- Update and runtime status: for a Kubernetes Deploy resource the update is the image build plus `kubectl apply`; runtime reflects the Pod state, such as running and passing readiness checks.
- Pod ID: copy in one click for use with `kubectl`.
- Widgets: custom buttons for one-off tasks such as tests or lint.
- Endpoints: links to Tilt-managed port forwards, plus custom endpoints such as a wiki page.
- Trigger mode: toggle automatic updates per resource; a manual-mode resource can still be updated on demand.

## Resource Details

Logs are the focus; overview info is also shown. The Trigger Update button runs a manual update (rebuild and redeploy). "All Resources" in the navbar shows all logs at once.

Log filters: source (build/update versus runtime), level (errors and warnings, from sources such as Docker build errors and Kubernetes events), and keyword or regex, which filters non-destructively.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read tutorial step 1 (Preparation) and step 3 (Tilt UI) in full. Confirmed the install scripts, the Docker install options and convenience script, the non-root note, the `hello-world` test, opening the UI with Spacebar, the Resource Overview items, Resource Details, Trigger Update and the three log filters. Not opened: the Docker docs linked from step 1. Softened: the non-root advice, which the page words as "suggested". 

Method: documentation only; no commands were run.
