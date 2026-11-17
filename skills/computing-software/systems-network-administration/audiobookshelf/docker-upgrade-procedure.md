---
id: computing-software.systems-network-administration.audiobookshelf.docker-upgrade-procedure
name: docker-upgrade-procedure
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [docker, upgrade, compose-pull, container-manager, portainer]
level: intro
status: docs-checked
description: "Upgrade a Docker Audiobookshelf container with compose pull/down/up and fix upgrades that leave MODULE_NOT_FOUND errors from caching managers."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/2.docker-compose-install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To upgrade, pull the new image and restart the container. With Docker Compose:

```bash
docker compose pull
docker compose down
docker compose up --detach
```

If you manually specified a version number in the image tag, update that tag to the version you want.

Some docker managers (Container Manager on Synology, Portainer and others) cache old container versions and do not upgrade properly. Typical startup errors are:

- `Error: Cannot find module '/index.js'`
- `code: 'MODULE_NOT_FOUND',`

Force the manager to reset the container so it uses the new image:

- Synology Container Manager: stop the container, then choose "Reset" under "Actions".
- Portainer: "Recreate" the container or stack.

Warning from the page: resetting deletes any files that are not accessible outside the container, i.e. anything not on a mounted volume.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Docker install page (Upgrading and Common Upgrade Problems sections).

Method: documentation only; no commands were run.
