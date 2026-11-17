---
id: computing-software.devops-ci-cd.gitea.install-from-binary
name: install-from-binary
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-from-binary, gitea, gitea-work-dir, gitea-web, sighup-restart, install-lock, secret-key]
level: intro
status: docs-checked
description: "Install Gitea from a release binary on Linux: dedicated git user, /var/lib/gitea and /etc/gitea layout, GITEA_WORK_DIR, run command, restart signals."
sources: ["https://docs.gitea.com/installation/install-from-binary/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Gitea from the binary

Release binaries include SQLite, MySQL and PostgreSQL support and embedded assets. Choose by platform: Linux `linux-amd64` (also `arm64`, `386`, `arm-5`, `arm-6`), Windows `windows-4.0-amd64` (a `gogit-windows` build exists for Windows performance problems), macOS `darwin-arm64` or `darwin-amd64`, FreeBSD `freebsd12-amd64`.

```sh
wget -O gitea https://dl.gitea.com/gitea/<version>/gitea-<version>-linux-amd64
chmod +x gitea
git --version          # Gitea needs Git >= 2.0
```
Create the service account (Debian family: `adduser --system --shell /bin/bash --gecos 'Git Version Control' --group --disabled-password --home <git-home> git`; Fedora family uses `groupadd --system git` plus `adduser ... --gid git --create-home`). Then:
```sh
mkdir -p /var/lib/gitea/{custom,data,log}
chown -R git:git /var/lib/gitea/ && chmod -R 750 /var/lib/gitea/
mkdir /etc/gitea && chown root:git /etc/gitea && chmod 770 /etc/gitea
cp gitea /usr/local/bin/gitea
export GITEA_WORK_DIR=/var/lib/gitea/
GITEA_WORK_DIR=/var/lib/gitea/ /usr/local/bin/gitea web -c /etc/gitea/app.ini
```
`/etc/gitea` is group-writable only so the web installer can write `app.ini`. Afterwards tighten: `chmod 750 /etc/gitea; chmod 640 /etc/gitea/app.ini`. For a pre-written read-only config, set `INSTALL_LOCK = true`, complete DB settings, and `SECRET_KEY` and `INTERNAL_TOKEN` (generate with `gitea generate secret`).

Shell completion (from 1.25): `gitea completion <shell>` for bash, fish, pwsh or zsh.

## Updating and restarting
Stop, replace the binary, start. Never rename the binary to include the version: repository git hooks embed its path, and a rename makes pushes fail with `hooks/pre-receive.d/gitea ... No such file or directory`. Fix with the admin task "Resynchronize pre-receive, update and post-receive hooks of all repositories" (overwrites customised hooks) and, without the built-in SSH server, the task that rewrites `.ssh/authorized_keys`.
Without systemd: `kill -1 $PID` / `killall -1 gitea` (SIGHUP) restarts; plain `kill` stops gracefully; avoid `-9`, which interrupts queues and indexers.

## Troubleshooting
- Old glibc ("GLIBC_2.14 not found"): the bundled SQLite needs it; build from source without SQLite.
- "address already in use" on 3000: run `./gitea web -p <port>` or find the other instance.
- Raspberry Pi: the docs say arm7 builds had a problem since v1.8; use arm6.

## Checked

2026-11-03: read https://docs.gitea.com/installation/install-from-binary/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
