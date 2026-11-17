---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-services
name: woodpecker-services
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [services, service-containers, databases]
level: practitioner
status: docs-checked
description: "Run database and cache service containers beside Woodpecker steps."
sources: ["https://woodpecker-ci.org/docs/usage/services", "https://woodpecker-ci.org/docs/administration/configuration/backends/local"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker services

The `services` section defines containers that run for the whole workflow, such as databases or caches.

```yaml
steps:
  - name: build
    image: golang
    commands:
      - go test

services:
  - name: database
    image: mysql
    ports:
      - 3306
    environment:
      MYSQL_DATABASE: test
      MYSQL_ALLOW_EMPTY_PASSWORD: yes
  - name: cache
    image: redis
```

The service name becomes its hostname, so MySQL above is reachable at `database:3306`. In list syntax every service must set `name`; in map syntax the key is the name. Names must be unique within a workflow, otherwise the hostname resolves to an arbitrary one.

Declare ports explicitly with a protocol where needed, such as `51820/udp`.

Details:

- Services need time to initialize. If a connection fails, wait (for example `sleep 15`) or implement a backoff.
- On shutdown, services receive SIGTERM, then SIGKILL if they do not respond. Add `failure: ignore` to tolerate bad exits.
- Configure service images with their own environment variables.
- The local backend does not support services.

## Checked

2026-11-03. Confirmed against: services (hostnames, ports, SIGTERM/SIGKILL, initialization), workflow-syntax and local backend (services not supported). Removed: nothing.

Method: documentation only; no commands were run.
