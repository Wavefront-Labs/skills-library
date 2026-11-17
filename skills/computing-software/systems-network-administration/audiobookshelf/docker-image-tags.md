---
id: computing-software.systems-network-administration.audiobookshelf.docker-image-tags
name: docker-image-tags
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [docker, image-tags, latest, edge, versions, ghcr]
level: intro
status: docs-checked
description: "Choose between the :latest, :edge and pinned :#.#.# Audiobookshelf image tags and know what each one tracks."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/2.docker-compose-install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The image is `ghcr.io/advplyr/audiobookshelf`. Three kinds of tag are documented:

- `:latest` is the most recent stable release from the GitHub releases page.
- `:edge` is rebuilt for every commit to the `master` branch, usually available within 15 minutes. It lets you help test features before a release and is described as generally safe. If you hit a problem with a new feature on `:edge`, report it on GitHub and include the commit hash.
- `:#.#.#` pins a specific release. For v2.19.0 use the tag `:2.19.0`.

If you manually specified a server version number, update it to pull the correct version on upgrade.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Docker install page (tag list, upgrading note about manually specified versions).

Method: documentation only; no commands were run.
