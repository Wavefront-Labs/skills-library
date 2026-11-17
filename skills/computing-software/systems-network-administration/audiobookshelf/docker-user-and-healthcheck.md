---
id: computing-software.systems-network-administration.audiobookshelf.docker-user-and-healthcheck
name: docker-user-and-healthcheck
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [docker, user, puid, healthcheck, wget, restart-policy]
level: practitioner
status: docs-checked
description: "Run the Audiobookshelf container as a specific user with the user directive (no PUID/GUID) and decide whether a healthcheck is worthwhile."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/2.docker-compose-install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Running as another user: Audiobookshelf does not use `PUID` or `GUID` environment variables. Add the compose directive instead:

```yaml
user: 1000:1000
```

Make sure that user can read your media mounts and write to `/config` and `/metadata`.

Healthchecks: the project does not recommend them unless you have external monitoring. Continuously pinging the server and restarting the container on a crash is generally redundant with a `restart` policy such as `restart: unless-stopped`, and it adds noise to your logs.

If you do define a healthcheck, the container image includes `wget` but does not include `curl`, so a `curl`-based test will fail with the command missing. Use `wget` in the test command.

On Windows, the `docker run` example uses `\` line continuations; remove them and run it as a single line.

## Checked

Method: docs-checked 2026-11-09 against the Docker install page of the Audiobookshelf docs repo (full raw markdown read: compose comments, Healthchecks, Windows caution).
