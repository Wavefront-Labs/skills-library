---
id: computing-software.web-development.directus.docker-quickstart
name: docker-quickstart
category: computing-software
field: web-development
product: directus
tags: [docker-quickstart, docker-run, onboarding, no-persistence]
level: intro
status: docs-checked
description: "Try Directus locally with one docker run command on port 8055 and know why changes are lost when the container stops."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/getting-started/2.create-a-project.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run the official image and publish the default port:

```bash
docker run -p 8055:8055 directus/directus
```

Open `http://localhost:8055` (or `http://127.0.0.1:8055`). An onboarding screen asks you to configure the first Admin account.

Gotchas:
- This quickstart has no persistence. Once the container stops, every change is lost.
- The docs describe it as a way to explore Directus at a glance and call Docker Compose (with `database`, `uploads` and `extensions` subdirectories) the recommended way to get started.
- New self-hosted instances run on the core tier by default; a license key unlocks higher limits.
- Docker must be installed and running first.

## Checked

2026-11-04: the docker run command, port, onboarding screen, lack of persistence, core-tier default and Docker prerequisite confirmed against the Directus Create a Project page. Removed an unsupported Verify line and reworded the compose recommendation to match the page.

Method: documentation only; no commands were run.
