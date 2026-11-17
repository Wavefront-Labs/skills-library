---
id: computing-software.ai-ml-engineering.open-webui.podman-install
name: podman-install
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [podman-quadlet, podman, systemd, kube-play, rootless]
level: practitioner
status: docs-checked
description: "Run Open WebUI under Podman with plain run, a systemd Quadlet unit, or kube play, including host Ollama access via host.containers.internal."
sources:
  - https://docs.openwebui.com/getting-started/quick-start/tab-docker/Podman
  - https://docs.openwebui.com/getting-started/quick-start/tab-docker/PodmanQuadlet
  - https://docs.openwebui.com/getting-started/quick-start/tab-docker/PodmanKubePlay
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Open WebUI on Podman, optionally as a systemd service, reaching Ollama on the host.

## Plain run
```bash
podman run -d --name openwebui -p 3000:8080 -v open-webui:/app/backend/data -e WEBUI_SECRET_KEY=your-secret-key ghcr.io/open-webui/open-webui:main
```

## Reaching the host
Use the DNS name `host.containers.internal`. The image default `http://host.docker.internal:11434` does not resolve under Podman, so add `-e OLLAMA_BASE_URL=http://host.containers.internal:11434` or set the Ollama connection in Settings > Admin > Connections. Pasta (default in Podman 5+) usually needs no special flags. slirp4netns is deprecated and removed in Podman 6; on old Podman use `--network=slirp4netns:allow_host_loopback=true`.

## Quadlet (rootless systemd; recommended for production on systemd distros)
Create the rootless directory `~/.config/containers/systemd/` (`mkdir -p`) and, in it, `open-webui.container`:
```ini
[Unit]
Description=Open WebUI Container
After=network-online.target

[Container]
Image=ghcr.io/open-webui/open-webui:main
ContainerName=open-webui
PublishPort=3000:8080
Volume=open-webui:/app/backend/data
Environment=WEBUI_SECRET_KEY=your-secret-key
AddHost=host.containers.internal:host-gateway
Environment=OLLAMA_BASE_URL=http://host.containers.internal:11434

[Service]
Restart=always

[Install]
WantedBy=default.target
```
Then `systemctl --user daemon-reload`, `systemctl --user start open-webui`, `systemctl --user enable open-webui`. Status: `systemctl --user status open-webui`; logs: `journalctl --user -u open-webui -f`. Update: `podman pull ghcr.io/open-webui/open-webui:main` then `systemctl --user restart open-webui`.

## Kube play
A `play.yaml` with a Pod (image `ghcr.io/open-webui/open-webui:main`, env `WEBUI_SECRET_KEY`, containerPort 8080 with hostPort 3000, volumeMount `/app/backend/data`) plus a 5Gi `PersistentVolumeClaim` named `open-webui-pvc`; start it with `podman kube play ./play.yaml`. For Nvidia use the `:cuda` image, set `nvidia.com/gpu=all: 1` under `resources.limits`, and have the GPU's Container Device Interface installed in the Podman Machine.

## Uninstall
`podman rm -f openwebui`; `podman rmi ghcr.io/open-webui/open-webui:main`; `podman volume rm open-webui` (deletes all data).

## Checked
2026-11-04. Confirmed against the Open WebUI docs pages getting-started/quick-start/tab-docker/Podman, PodmanQuadlet and PodmanKubePlay (all read in full): the podman run command, host.containers.internal and the unresolvable host.docker.internal default, the OLLAMA_BASE_URL option and the Connections setting, pasta default in Podman 5+, slirp4netns deprecation and removal in Podman 6 with the allow_host_loopback flag, the Quadlet unit file and systemctl and journalctl commands, the update tip, the play.yaml contents with the 5Gi claim, podman kube play, the :cuda image, the nvidia.com/gpu limit and CDI requirement, and the three uninstall commands. Fixed a garbled directory sentence to the page's rootless path and softened pasta to usually needing no special flags.
Method: documentation only; no commands were run.
