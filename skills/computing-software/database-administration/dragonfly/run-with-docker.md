---
id: computing-software.database-administration.dragonfly.run-with-docker
name: run-with-docker
category: computing-software
field: database-administration
product: dragonfly
tags: [docker, docker-run, dragonfly, quickstart, memlock]
level: intro
status: docs-checked
description: "Start a single Dragonfly instance with docker run on Linux, macOS or Windows, note the prerequisites and connect with redis-cli."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/getting-started/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`docker run` is the simplest way to get Dragonfly running.

Prerequisites: at least 4GB of RAM to get the benefits of Dragonfly, 1 CPU core, Linux kernel 4.19 or higher.

On Linux:

```bash
docker run --network=host --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
```

On macOS, `network=host` does not work well, and the page gives the port-publishing form for macOS and Windows:

```bash
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
```

Dragonfly answers both `http` and `redis` requests on port 6379. Connect with `redis-cli` to `localhost:6379`, or open `http://localhost:6379` in a browser.

If initialisation errors appear on some configurations, running with `docker run --privileged ...` can fix them.

Connect with `redis-cli` then `set hello world`; `get hello` returns `"world"`.

## Checked

2026-11-04. Confirmed against the Dragonfly Docker install page: prerequisites, both docker run commands, http and redis answers, the `--privileged` note, the redis-cli example. Corrected the claim that host networking fails on Windows: the page says this only for macOS.

Method: documentation only; no commands were run.
