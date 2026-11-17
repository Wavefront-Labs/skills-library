---
id: computing-software.devops-ci-cd.tilt.tilt-index
name: tilt-index
category: computing-software
field: devops-ci-cd
product: tilt
tags: [index, tilt]
level: intro
status: docs-checked
description: "Orient to Tilt: what it automates, the one-step install commands, and which manual to read for new users, existing services, or Tiltfile tuning."
sources:
  - "https://docs.tilt.dev/index.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tilt overview

Goal: get a complete dev environment for a microservice team running with `tilt up`, and know where to go next.

## What Tilt does

Run `tilt up` to work in a complete dev environment configured for your team. Tilt automates all the steps from a code change to a new process: watching files, building container images, and bringing your environment up-to-date. Think `docker build && kubectl apply` or `docker-compose up`.

## Get the binary

Installing the `tilt` binary is a one-step command.

macOS/Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Windows (PowerShell):

```powershell
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

## Pick the right manual

- Completely new to Tilt: watch the two minute explanation video, browse the FAQs, then follow the tutorial to run Tilt for the first time.
- Setting up Tilt for existing services: use the best practice guides, listed per language/example on the docs site.
- Optimizing your Tiltfile: search the API reference for the function you need.

## Community and help

- Questions: join the Kubernetes slack (slack.k8s.io) and find the #tilt channel, or file an issue on the tilt-dev/tilt GitHub repo.
- Code snippets of Tiltfile functionality shared by the community live in Tilt Extensions (tilt-dev/tilt-extensions); extensions add new Tiltfile functionality.
- Tilt sends anonymized usage data to improve Tilt on every platform.

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Getting Started page in full (the examples list is generated at build time; read from src/_data/examples.yml). Confirmed the one-step install commands, the description of what Tilt automates, the three manual pointers, the Slack channel, issue tracker and Tilt Extensions references and the anonymized usage data note. Not opened: the two minute video. Reworded the anonymized-data sentence to the page's wording. The per-language guide list was confirmed from the repo's src/_data/examples.yml (static HTML, Go, NodeJS, Python, Java, C#, Bazel). The skill is thin. 

Method: documentation only; no commands were run.
