---
id: computing-software.systems-network-administration.audiobookshelf.config-volume-local-disk-only
name: config-volume-local-disk-only
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [sqlite, config, network-mount, nfs, corruption, docker]
level: practitioner
status: docs-checked
description: "Keep the Audiobookshelf /config directory on local disk because its SQLite database corrupts and slows when stored on a network mount."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/2.docker-compose-install.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `/config` mount (the `CONFIG_PATH` directory) contains the SQLite database for users, books, libraries and settings. The docs state it must be accessible directly on the machine running the server and not stored and accessed over the network, for example on a different NAS.

Failure mode: the server may appear to work with a networked database, but performance suffers and you will eventually hit database corruption (the page cites the SQLite guidance on use over a network).

Practical layout:

- `/config` on local disk of the Docker host.
- `/metadata` is the cache, streams, covers, downloads, backups and logs directory (`METADATA_PATH`).

Also keep every mount a separate directory not nested inside another mount. The environment page repeats that `CONFIG_PATH` must not be mounted over the network.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Docker install page (Network Mounts warning) and the environment configuration page (Filesystem table).

Method: documentation only; no commands were run.
