---
id: computing-software.ai-ml-engineering.open-webui.docker-run-and-image-variants
name: docker-run-and-image-variants
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [docker-run-manual, docker, image-tags, cuda, ollama, version-pinning]
level: practitioner
status: docs-checked
description: "Start Open WebUI with docker run, pick the right image tag (main, slim, cuda, ollama, dev), pin release versions, and use common run variants."
sources:
  - https://docs.openwebui.com/getting-started/quick-start/tab-docker/ManualDocker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a single Open WebUI container and choose an image tag deliberately.

## Base command
Replace the key with the output of `openssl rand -hex 32`:
```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data -e WEBUI_SECRET_KEY=your-secret-key --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```
- `-p 3000:8080`: UI on host port 3000.
- `-v open-webui:/app/backend/data`: chats, users and settings live here; never run without it.
- `--add-host=host.docker.internal:host-gateway`: lets the container reach services on the host such as Ollama.
- `WEBUI_SECRET_KEY`: set once and keep it, otherwise every recreated container logs everyone out.

## Image variants
| Tag | Use |
|---|---|
| `:main` | standard, includes bundled speech-to-text and embedding models |
| `:dev` | nightly pre-release from the `dev` branch |
| `:slim` / `:main-slim` | same image; about 197 MB vs 1.62 GB download |
| `:cuda` | Nvidia, CUDA 12.8 (add `--gpus all`); `:cuda126` for CUDA 12.6 |
| `:ollama` | Ollama bundled in the container |

Each has a `:dev-<variant>` build. Slim cannot combine with CUDA or bundled Ollama.

## Tag behaviour
`:main` and `:latest` are the same rolling image from the `main` branch (`:latest` is NOT the newest stable release). `:vX.Y.Z` and `:X.Y.Z` are pinned and immutable, `:X.Y` follows the newest patch of that minor, `:git-<sha>` pins one commit. For production, pin a version tag, e.g. `ghcr.io/open-webui/open-webui:vX.Y.Z` (also `-slim`, `-cuda`, `-ollama` suffixes). Docker Hub `openwebui/open-webui` mirrors only `latest`, `latest-<variant>`, bare `<variant>`, `X.Y.Z` and `X.Y`; `:main`, `:dev`, `:vX.Y.Z`, `:git-<sha>` exist on ghcr.io only.

## Variants of the command
- GPU: add `--gpus all`, image `:cuda`.
- Bundled Ollama: add `-v ollama:/root/.ollama` and use `:ollama` (with GPU add `--gpus=all`).
- Remote Ollama: `-e OLLAMA_BASE_URL=https://example.com`.
- Single-user (no login): `-e WEBUI_AUTH=False`. You cannot switch between single-user and multi-account mode afterwards.
- Dev: `-p 3001:8080 -v open-webui-dev:/app/backend/data --name open-webui-dev ... :dev`. Use a separate volume, never the production one.

## Uninstall
`docker rm -f open-webui`; optionally `docker rmi ghcr.io/open-webui/open-webui:main`; `docker volume rm open-webui` deletes all data.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page getting-started/quick-start/tab-docker/ManualDocker (read in full): the base docker run command and flag explanations, the image variant table including the 197 MB versus 1.62 GB slim sizes (page figures dated October 2026), dev-variant builds, slim not combining with CUDA or Ollama, tag behaviour and immutability, the Docker Hub mirror subset, version-pinned pull examples, GPU, bundled Ollama, remote Ollama, single-user mode and its one-way warning, the dev run with a separate volume, and the uninstall commands. Nothing removed.
Method: documentation only; no commands were run.
