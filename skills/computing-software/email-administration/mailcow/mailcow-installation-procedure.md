---
id: computing-software.email-administration.mailcow.mailcow-installation-procedure
name: mailcow-installation-procedure
category: computing-software
field: email-administration
product: mailcow
tags: [installation, generate-config, mailcow-conf, docker-compose, selinux, mtu, default-credentials]
level: practitioner
status: docs-checked
description: "Install mailcow dockerized from the git repository with generate_config.sh, including Docker prerequisites, SELinux, MTU and IPv6 caveats."
sources: ["https://docs.mailcow.email/getstarted/install/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing mailcow dockerized

Prerequisites: git, openssl, curl, awk, sha1sum, grep, cut and (since the 2025-09 release) jq; Docker 24.0.0 or newer and Docker Compose 2.0 or newer. Use the latest Docker Engine from Docker's own repository, not the distribution package. With the compose plugin the command is `docker compose`; the standalone binary is `docker-compose`.

Steps:
1. `umask 0022`, then `cd /opt` and `git clone https://github.com/mailcow/mailcow-dockerized`.
2. `./generate_config.sh` generates the configuration file `mailcow.conf`.
3. Review `mailcow.conf`.
4. `docker compose pull` and `docker compose up -d`.

Log in at `https://${MAILCOW_HOSTNAME}/admin` with `admin` and the default password `moohoo`, and change it immediately.

On SELinux hosts, make sure `container-selinux` is installed and add `"selinux-enabled": true` to `/etc/docker/daemon.json`, then restart Docker.

If your network MTU is not 1500 (for example OpenStack), set `com.docker.network.driver.mtu` under `mailcow-network` `driver_opts` in `docker-compose.yml`. If the host has no IPv6, disable IPv6 for the mailcow network.

Data lives in Docker volumes and survives container recreation. Without a reverse proxy, redirect HTTP to HTTPS.

## Checked

2026-11-09. Confirmed on the install page: package list including jq from 2025-09, Docker 24.0.0 and Compose 2.0 minimums, latest Docker Engine advice, plugin versus standalone commands, umask and clone steps, generate_config.sh, pull and up, admin and moohoo credentials, SELinux daemon.json, MTU driver_opts, IPv6 and the persistence and reverse proxy notes. Only the advice to change the default password is the skill's own.

Method: docs-checked 2026-11-09 against the full install page (install.en.md in mailcow-dockerized-docs).
