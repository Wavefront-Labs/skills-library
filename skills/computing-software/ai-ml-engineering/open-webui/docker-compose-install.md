---
id: computing-software.ai-ml-engineering.open-webui.docker-compose-install
name: docker-compose-install
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [docker-compose-install, docker, compose, gpu, install, dev-channel]
level: practitioner
status: docs-checked
description: "Install Open WebUI with Docker Compose v2, add Nvidia GPU support, run a separate :dev pre-release instance, and uninstall cleanly."
sources:
  - https://docs.openwebui.com/getting-started/quick-start/tab-docker/DockerCompose
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Open WebUI under Docker Compose with persistent data and a fixed secret key.

## Steps
1. Generate a key: `openssl rand -hex 32`.
2. Save as `docker-compose.yml`:
```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    extra_hosts:
      - host.docker.internal:host-gateway
    environment:
      - WEBUI_SECRET_KEY=your-secret-key
    restart: unless-stopped
volumes:
  open-webui:
```
3. `docker compose up -d`. The UI is on port 3000 (container port 8080).

`extra_hosts` makes `host.docker.internal` resolve to the host on Linux. With no `OLLAMA_BASE_URL` set, the image looks for Ollama at `http://host.docker.internal:11434` (then `:12434`), so this line lets it reach an Ollama on the host.

## Update
`docker compose pull` then `docker compose up -d`. The Watchtower command in the docs targets a container named `open-webui`; Compose names the container `<project>-open-webui-1` unless you add `container_name: open-webui`.

## Nvidia GPU
Change the image to `ghcr.io/open-webui/open-webui:cuda` (pre-release: `:dev-cuda`) and add to the service:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```
The `:cuda` image moves Open WebUI's own local embedding, reranking and Whisper models to the GPU; Ollama's models use a GPU only if the Ollama container has one. With no GPU visible it falls back to CPU without error.

## Pre-release `:dev` side by side
Add a second service, for example `openwebui-dev`, image `ghcr.io/open-webui/open-webui:dev`, port `3001:8080`, its own volume `open-webui-dev:/app/backend/data`, its own secret key. Never share the volume with production: dev builds may include migrations a release image cannot read back.

## Helper scripts shipped in the codebase
`docker-compose-launcher.sh` (GPU auto-detect; quote bracket options in zsh, e.g. `'--enable-gpu[count=1]'`; `--drop` tears down), `docker-cleanup.sh` (deletes all volumes after confirmation), `docker-run.sh` (sets no `WEBUI_SECRET_KEY`; add one), `docker-ollama.sh`, `docker-update-models.sh`.

## Uninstall
`docker compose down`; add `-v` (or `docker volume rm <project>_open-webui`) to delete chats and settings; `docker rmi ghcr.io/open-webui/open-webui:main` for the image.

## Gotchas
- Use Compose v2 (`docker compose`, with a space), not `docker-compose`.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page getting-started/quick-start/tab-docker/DockerCompose (read in full): the compose file, extra_hosts and the Ollama fallback addresses, the update and Watchtower container name note, the cuda and dev-cuda tags with the deploy block and GPU fallback, the dev service on port 3001 with its own volume, all five helper scripts and their notes, Compose v2 syntax and the uninstall commands. Removed: the claim that a missing WEBUI_SECRET_KEY logs everyone out on recreate (not stated on this page).
Method: documentation only; no commands were run.
