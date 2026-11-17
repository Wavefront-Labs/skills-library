---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-linux-packages
name: woodpecker-linux-packages
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [packages, systemd, deb-rpm]
level: practitioner
status: docs-checked
description: "Install Woodpecker from DEB or RPM packages or Linux tarballs and run it under systemd."
sources: ["https://woodpecker-ci.org/docs/administration/installation/packages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker distribution packages and systemd

Official DEB and RPM packages exist for linux/amd64 and linux/arm64, attached to the GitHub releases. Packages `woodpecker-server`, `woodpecker-agent` and `woodpecker-cli` install systemd unit files and example environment files.

```shell
sudo apt --fix-broken install ./woodpecker-{server,agent,cli}_${RELEASE_VERSION}_amd64.deb
sudo dnf install https://github.com/woodpecker-ci/woodpecker/releases/download/v${RELEASE_VERSION}/woodpecker-{server,agent,cli}-${RELEASE_VERSION}-1.x86_64.rpm
```

Copy `/etc/woodpecker/woodpecker-server.env.example` to `/etc/woodpecker/woodpecker-server.env`, and likewise for the agent, then adjust values. Server env example: `WOODPECKER_OPEN`, `WOODPECKER_HOST`, forge client and secret, `WOODPECKER_AGENT_SECRET`. Agent env: `WOODPECKER_SERVER=localhost:9000` and the same `WOODPECKER_AGENT_SECRET`. The units refuse to start while the env file is missing or empty.

Manual install from tarballs:

1. Put `woodpecker-server` and `woodpecker-agent` in `/usr/local/bin/`.
2. Create `/etc/woodpecker` and both env files.
3. Create the `woodpecker` system user with home `/var/lib/woodpecker`.
4. Save the unit files under `/etc/systemd/system/` and run `sudo systemctl daemon-reload` then `sudo systemctl enable --now woodpecker-server woodpecker-agent`.
5. Check `systemctl status woodpecker-server woodpecker-agent` and `journalctl -u woodpecker-agent -b`.

Community packages exist for Alpine, Arch, openSUSE, NixOS and Homebrew (CLI only).

## Checked

2026-11-03. Read the Woodpecker packages installation page and confirmed the package names, install commands and service settings. Nothing removed. 

Method: documentation only; no commands were run.
