---
id: computing-software.cybersecurity-defensive.zeek.install-zeek
name: install-zeek
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, install, docker-image, binary-packages]
level: intro
status: docs-checked
description: "Install Zeek from official Docker images, OBS Linux binary packages (LTS vs latest), or third-party Homebrew, FreeBSD and OpenBSD ports."
sources: ["https://docs.zeek.org/en/current/install.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# install zeek

Pick a channel:

- **Docker**: `docker pull zeek/zeek:latest` (feature release), `zeek/zeek:lts`, a series tag, or a specific release. Nightly is `zeek/zeek-dev:latest`. Images are also on public.ecr.aws/zeek. They are Debian-based with zeek, zkg and the Spicy toolchain, otherwise minimal. To add plugins or Spicy packages install g++, cmake, make and libpcap-dev.
- **Linux binary packages** (openSUSE Build Service): add the OBS repository, then install a package group: `zeek-X.0` (a specific LTS line), `zeek` (latest release), `zeek-nightly`, `zeek-rc`. The LTS packages keep you on that line until you switch.
- **macOS**: `brew install zeek`. **FreeBSD**: `sudo pkg install -y zeek`. **OpenBSD**: `doas pkg_add zeek`. These are not maintained by the Zeek project.

Binary packages install under `/opt/zeek` with zeek, zkg and Spicy included. Distribution packages may be older, so check the version before installing.

```
sudo apt install zeek-8.0
```

## Checked

2026-11-08. Read the Installing Zeek page in full; every claim confirmed.

Method: documentation only; no commands were run.
