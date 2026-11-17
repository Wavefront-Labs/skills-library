---
id: computing-software.systems-network-administration.audiobookshelf.docker-compose-deployment
name: docker-compose-deployment
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [docker, docker-compose, ports, volumes, config, metadata]
level: intro
status: docs-checked
description: "Deploy Audiobookshelf with Docker Compose: image, port 13378 mapped to 80, the /config and /metadata volumes, media mounts and TZ."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/2.docker-compose-install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docker is the recommended way to run Audiobookshelf. A minimal compose service:

```yaml
services:
  audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    ports:
      - 13378:80
    volumes:
      - </path/to/config>:/config
      - </path/to/metadata>:/metadata
      - </path/to/audiobooks>:/audiobooks
      - </path/to/podcasts>:/podcasts
    environment:
      - TZ=America/Toronto
    restart: unless-stopped
```

ABS runs on port 13378 by default in this example; if you change the port, change only the external (left) side, since the container listens on 80. `/config` holds the SQLite database and migration scripts; `/metadata` holds book metadata, cover and author images, logs and backups. Most people add `/audiobooks` and `/podcasts` mounts, but you can add as many or as few media mounts as you like.

Each mount point must be a separate directory not contained within another mount point. Replace the `</path/to/...>` placeholders with real host directories and remove the angle brackets.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Docker install page (compose example, mount-point note).

Method: documentation only; no commands were run.
