---
id: computing-software.ai-ml-engineering.ollama.install-linux-systemd-service
name: install-linux-systemd-service
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [systemd, ollama-service, restart-always, ollama-user]
level: advanced
status: docs-checked
description: "Create the ollama user and a systemd unit for a manual Linux install, and customise it with systemctl edit."
sources:
  - https://docs.ollama.com/linux.md
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a manually installed Ollama as a service.

Create a user and group and add yourself:

```
sudo useradd -r -s /bin/false -U -m -d /usr/share/ollama ollama
sudo usermod -a -G ollama $(whoami)
```

Create `/etc/systemd/system/ollama.service`:

```
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=$PATH"

[Install]
WantedBy=multi-user.target
```

Then:

```
sudo systemctl daemon-reload
sudo systemctl enable ollama
```

Start it with `sudo systemctl start ollama` and check it with `sudo systemctl status ollama`. The unit sets `Restart=always` with `RestartSec=3`, so systemd restarts the service three seconds after it exits, and it runs as the `ollama` user and group.

Customise without editing the unit: `sudo systemctl edit ollama` opens an override, or create `/etc/systemd/system/ollama.service.d/override.conf` with `[Service]` and `Environment=` lines.

The service user is why model storage needs `chown -R ollama:ollama` when you move it (FAQ), and why AMD GPU access can need the `video` or `render` group (troubleshooting and GPU pages).

An override file looks like:

```
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

After changing it, run `systemctl daemon-reload` and `systemctl restart ollama` (the FAQ's sequence).

Logs: `journalctl -e -u ollama`.

## Checked

2026-11-08. User creation, unit file, enable/start/status, the `systemctl edit` and override.conf routes, and `journalctl -e -u ollama` against the Linux page (docs.ollama.com/linux); the `OLLAMA_HOST` override and reload/restart commands and the `chown` note against the FAQ (docs.ollama.com/faq); the video/render group note against the troubleshooting page. Narrowed the GPU-group remark to AMD, which is what the sources state. Nothing removed.

Method: documentation only; no commands were run.
