---
id: computing-software.systems-network-administration.pi-hole.docker-upgrade-and-watchtower
name: docker-upgrade-and-watchtower
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [docker-upgrade, compose-pull, watchtower]
level: practitioner
status: docs-checked
description: "Upgrade a Pi-hole container by replacing it with a new image, and why unattended updates such as Watchtower are discouraged."
sources: ["https://docs.pi-hole.net/docker/upgrading/", "https://docs.pi-hole.net/docker/tips-and-tricks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading Pi-hole in Docker

Inside the container, `pihole -up` and `pihole -r` are disabled. You upgrade by replacing the container with a fresh image. Keep configuration in volumes, because the container is removed during the process, and avoid mounting config files read-only.

**Docker Compose**

```bash
docker compose pull
docker compose down
docker compose up -d
```

**Docker run**

```bash
docker pull pihole/pihole:latest
docker stop pihole
docker rm pihole
docker run [ ... original arguments ... ]
```

**Read release notes first** for Docker, Core, FTL and Web; sometimes more than the image tag must change.

**Watchtower.** The docs say not to let a tool update Pi-hole unattended: sometimes things go wrong and you need to set aside time to update manually. To exclude the container, see Full Exclude in Watchtower's documentation.

The manual process:

1. Read the release notes.
2. Pull the new image.
3. Stop and remove the running container; anything not volume-mapped (logs, customisations) is deleted.
4. Recreate the container from the new image.

**Checklist**

1. Confirm `/etc/pihole` is on a volume.
2. Run the three compose commands in the directory holding your compose file.

## Checked

2026-11-03. Read the Docker Upgrading page (compose and docker run sequences, `pihole -up` and `pihole -r` disabled, release notes, read-only mount warning) and the Docker Tips and Tricks Note on Watchtower (manual upgrade steps, Full Exclude). Removed the post-upgrade verification item.

Method: documentation only; no commands were run.
