---
id: computing-software.ai-ml-engineering.ollama.install-linux-script-and-upgrade
name: install-linux-script-and-upgrade
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [install-script, curl, upgrade, ollama-version, installsh]
level: intro
status: docs-checked
description: "Install or upgrade Ollama on Linux with the install script and pin a release with OLLAMA_VERSION."
sources:
  - https://docs.ollama.com/linux.md
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get Ollama running on Linux.

Install:

```
curl -fsSL https://ollama.com/install.sh | sh
```

Upgrade by running the same script again (the FAQ and Linux page both say to re-run the install script). Pin a specific version, including pre-releases, by setting `OLLAMA_VERSION` for the script (Linux and troubleshooting pages):

```
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION=0.5.7 sh
```

View logs when run as a service: `journalctl -e -u ollama`.

Manual install: download and extract the package into `/usr` (the page names `ollama-linux-amd64.tar.zst`, with separate ROCm and arm64 archives). If upgrading an older install manually, remove the old libraries first: `sudo rm -rf /usr/lib/ollama`.

Uninstall (Linux page): `sudo systemctl stop ollama`, `sudo systemctl disable ollama`, remove `/etc/systemd/system/ollama.service`, remove the libraries and the binary (`sudo rm $(which ollama)`), then `sudo userdel ollama`, `sudo groupdel ollama` and `sudo rm -r /usr/share/ollama`.

Verify a running install with `ollama -v` (the manual-install steps use it).

GPU driver requirements are listed in the GPU skills.

## Checked

2026-11-08. Install script, re-run to upgrade, `OLLAMA_VERSION`, manual install archives, `rm -rf /usr/lib/ollama` and the uninstall steps against the Linux page (docs.ollama.com/linux), the FAQ and the troubleshooting page. Removed the `ollama --version` and `GET /api/version` check, which none of the cited pages show; replaced with `ollama -v` from the Linux page.

Method: documentation only; no commands were run.
