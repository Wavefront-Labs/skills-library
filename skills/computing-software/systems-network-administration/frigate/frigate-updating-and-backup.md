---
id: computing-software.systems-network-administration.frigate.frigate-updating-and-backup
name: frigate-updating-and-backup
category: computing-software
field: systems-network-administration
product: frigate
tags: [updating, config-backup, release-notes, image-tag, rollback]
level: practitioner
status: docs-checked
description: "Update a Docker Frigate install safely by stopping the container, backing up /config and pinning the new image tag."
sources: ["https://docs.frigate.video/frigate/updating/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Updating Frigate

Before updating, stop Frigate, back up the `/config` directory (the config file and `frigate.db`) and read the GitHub release notes for breaking changes or configuration changes. Check the Frigate releases page for the current stable version.

With Docker Compose: `docker compose down frigate`, edit the image tag in `docker-compose.yml` (for example `ghcr.io/blakeblackshear/frigate:<version>`), `docker pull` the image, then start it again. With plain `docker run`, `docker stop frigate`, pull the new tag and recreate the container with the same options. To roll back, stop Frigate, restore the backed-up config and database and set the previous image tag. The `stable` tag always points to the latest stable release after a pull.

Home Assistant App installs update from Settings, Apps instead: back up the app, press Update, then restart it.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/frigate/updating (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Removed the dated current-version claim and the 0.18.2 tag example (now a version placeholder), the unsupported claim that pinning a tag versus a floating tag eases rollback, and the unsupported remark about the Home Assistant integration being a separate component.
