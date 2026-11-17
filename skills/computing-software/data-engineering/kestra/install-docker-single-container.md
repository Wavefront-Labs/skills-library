---
id: computing-software.data-engineering.kestra.install-docker-single-container
name: install-docker-single-container
category: computing-software
field: data-engineering
product: kestra
tags: [docker, install, server-local, h2, port-8080, slim-image]
level: intro
status: docs-checked
description: "Run Kestra in one Docker container with server local for testing, and choose between slim, latest, latest-lts and pinned image tags."
sources:
  - https://kestra.io/docs/installation/docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kestra runs in a single container for quick testing. It needs Docker running (WSL on Windows) and publishes port 8080.

```bash
docker run --pull=always --rm -it -p 8080:8080 --user=root \
  --name kestra \
  -v kestra_data:/app/storage \
  -v kestra_db:/app/data \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp:/tmp \
  kestra/kestra:latest-slim server local
```

Open http://localhost:8080.

- This uses an embedded H2 database, for testing not production. For PostgreSQL use the Docker Compose install.
- `-slim` images bundle no plugins; auto-install is on by default for `server local`. `kestra/kestra:latest` bundles all plugins.

Tags:

- `latest`: rolling stable, not LTS.
- `latest-lts`: rolling LTS line.
- `v<X.X>`: patch updates within a minor line.
- `v<X.X.X>`: immutable, recommended for locked-down production.
- `develop`: nightly, unstable, testing only.

Custom images: build `FROM kestra/kestra:$IMAGE_TAG`, install plugins with `/app/kestra plugins install`, or copy JARs into `/app/plugins`.

## Checked

2026-11-04. Confirmed against the Kestra single Docker container page: the docker run command with server local, embedded H2 database and kestra_data and kestra_db volumes, slim images shipping without plugins with auto-install on for server local, latest bundling all plugins, the tag list (latest, latest-lts, v<X.X>, v<X.X.X>, develop), custom image building with kestra plugins install and /app/plugins. Reworded the port 8080 line, which the page does not call a free-port requirement.

Method: documentation only; no commands were run.
