---
id: computing-software.devops-ci-cd.gitea.docker-rootless
name: docker-rootless
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-docker-rootless, gitea, rootless-image, latest-rootless, user-directive, builtin-ssh]
level: practitioner
status: docs-checked
description: "Differences and setup for the Gitea rootless Docker image: /var/lib/gitea and /etc/gitea mounts, port 2222, UID 1000 ownership, custom user."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/with-docker-rootless.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea rootless Docker image

Compared to the rootful image: no host root privilege needed but stricter UID/GID requirements; it must use Gitea's built-in SSH server (the rootful one uses a managed OpenSSH); volume layout differs. Port mapping, customisation, upgrading and environment variables otherwise work the same. The two images are not compatible; do not swap `image:` between them on existing data.

```sh
mkdir -p gitea/{data,config}
```
```yaml
services:
  server:
    image: docker.gitea.com/gitea:<version>-rootless
    restart: always
    volumes:
      - ./data:/var/lib/gitea
      - ./config:/etc/gitea
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "3000:3000"
      - "2222:2222"
```
Tags: `latest-rootless`, `1-rootless`, `<version>-rootless`, `main-nightly-rootless`, `1.x-nightly-rootless`.

## Ownership
Default is uid 1000 / gid 1000: `sudo chown 1000:1000 config/ data/`. Wrong ownership shows in logs as `mkdir: can't create directory '/var/lib/gitea/git': Permission denied`, `/var/lib/gitea/git is not writable`, `docker setup failed`.

## Named volumes
Declare `gitea-data` and `gitea-config` (driver local) and mount them at `/var/lib/gitea` and `/etc/gitea`; permissions are then handled by Docker. DB containers are separate.

## Custom user
Use the compose `user:` key (docker `--user` semantics), e.g. `user: 1001` taken from `id -u git`, and make sure the mounted folders are writable by that user.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
