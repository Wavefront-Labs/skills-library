---
id: computing-software.devops-ci-cd.gitea.linux-systemd-service
name: linux-systemd-service
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-systemd-unit, gitea, systemctl-enable-now, supervisor, gitea-service, contrib-service]
level: intro
status: docs-checked
description: "Run Gitea as a Linux service from the contrib sample: systemd unit edits, enable --now (systemd 220+), or a supervisor program with a log directory."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/run-as-service-in-ubuntu.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea as a Linux service

The docs were tested on Ubuntu 16.04 and say the steps work on other distributions with small changes.

## systemd
1. Copy the sample `gitea.service` from the Gitea repository (`contrib/service/systemd/gitea.service`) to `/etc/systemd/system/gitea.service`.
2. Edit it: uncomment any service that needs to be enabled, change the user and home directory and other startup values, and change `PORT` or drop the `-p` flag if you use the default port.
3. Enable and start:
```sh
sudo systemctl enable gitea
sudo systemctl start gitea
# systemd 220 or later: both at once
sudo systemctl enable gitea --now
```

## supervisor
```sh
sudo apt install supervisor
mkdir <git-home>/gitea/log/supervisor     # log dir, adjust to your install
```
Append the sample program section from the repository (`contrib/service/supervisor/gitea`) to `/etc/supervisor/supervisord.conf`, change the `git` user and `<git-home>` home to your deployment, and set the port or drop `-p`. Then `sudo systemctl enable supervisor` and `sudo systemctl start supervisor` (or `enable supervisor --now` on systemd 220+).

## Checked
2026-11-03. Steps confirmed against the Gitea docs page run-as-service-in-ubuntu.md (raw markdown, gitea/docs main branch). Removed: the specific Wants/After wording (page says only to uncomment services that need enabling), the WorkingDirectory/GITEA_WORK_DIR sentence, the SELinux cross-reference, and the Failure modes section (daemon-reload and database-ordering claims are not on the page).
Method: documentation only; no commands were run.
