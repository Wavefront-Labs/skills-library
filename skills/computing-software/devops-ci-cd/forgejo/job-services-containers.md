---
id: computing-software.devops-ci-cd.forgejo.job-services-containers
name: job-services-containers
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [job-services, service-containers, docker-backend, container-network]
level: practitioner
status: docs-checked
description: "Run databases and similar services next to a job with the services key, on the docker backend only."
sources:
  - https://forgejo.org/docs/latest/user/actions/advanced-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A job can declare `services`, containers started before the job and terminated when it ends:

```
jobs:
  my-job:
    runs-on: docker
    services:
      pgsql:
        image: postgres:15
        env:
          POSTGRES_DB: test
          POSTGRES_PASSWORD: postgres
```

The job reaches the service by its name, here `pgsql`. The service IP is on the same network as the container running the steps, so there is no need to bind ports. The `postgres:15` image exposes port 5432 and a client can connect to it directly.

Restrictions:

- Services are supported only with the docker backend, not the lxc backend.
- They require `[container].network` in the runner configuration to be empty, so a new network can be created temporarily to connect the job container and the services.

The workflow reference lists the supported options, and the docs link to examples that illustrate configuration and usage.

A container with the given image is run before the job starts and is terminated when it completes. The job addresses the service by its name, for example pgsql, on the same network as the step container, so no port binding is needed.

## Checked

2026-11-04. Confirmed against the Forgejo Actions advanced features page (Services section): the services sample, name addressing, same-network behaviour, port 5432, docker-only support and the empty [container].network requirement. Nothing removed.

Method: documentation only; no commands were run.
