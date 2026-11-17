---
id: computing-software.cloud-infrastructure-engineering.docker.compose-vs-swarm-secret-behaviour
name: compose-vs-swarm-secret-behaviour
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm-secrets, compose-vs-swarm-secrets, compose-secrets, docker-secret, secret-target, external-secret]
level: advanced
status: docs-checked
description: "The same secrets: block behaves differently under docker compose and docker stack deploy: storage, encryption, tmpfs vs bind mount, uid/gid/mode, environment and external sources."
sources: ["https://docs.docker.com/compose/how-tos/use-secrets/", "https://docs.docker.com/reference/compose-file/secrets/", "https://docs.docker.com/reference/compose-file/services/#secrets", "https://docs.docker.com/engine/swarm/secrets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compose vs Swarm secret behaviour

## Side by side
| Aspect | `docker compose up` | `docker stack deploy` (Swarm) |
|---|---|---|
| Source `file:` | Compose bind-mounts a single file into the container | Swarm secret created from the file |
| Source `environment:` | Supported (Compose only) | Not supported |
| `external: true` | Declared in the file; the Swarm docs show it for a secret created with `docker secret create` | References the existing Swarm secret |
| Storage | Whatever the host file is | Stored in the Raft log, which is encrypted; replicated across managers |
| In the container | `/run/secrets/<name>` (Linux containers only) | `/run/secrets/<name>` on a `tmpfs` filesystem, only while the task runs |
| Long syntax `uid`, `gid`, `mode` | Only implemented for `environment`-sourced secrets; ignored for `file` sources | Applied (Linux containers; not supported for Windows containers) |
| Changing a value | Edit the source and recreate the container | Rotate by creating a new secret and updating the service (`--secret-rm` / `--secret-add`), ideally with versioned names |

## Portable definition
```yaml
services:
  app:
    image: app:1.0
    secrets:
      - source: db_password
        target: db_password       # /run/secrets/db_password
        uid: "10001"              # not applied by Compose for a file source
        mode: 0400
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```
The same top-level definition is accepted by both `docker compose` and `docker stack deploy`
(the Swarm secrets page says both support defining secrets in a Compose file). With
`external: true` the secret file never sits next to the stack definition.

## Consequences
- A non-root container under Compose with a `file` source cannot rely on `uid` or `mode`;
  the bind mount keeps the host file's ownership and permissions, so set them on the host.
- Compose secrets are only as protected as the host file; keep them out of Git and the
  build context.
- Swarm secrets can hold generic strings or binary content up to 500 KB.
- Docker secrets in Swarm are only available to Swarm services, not standalone containers.

## Verify
```bash
docker compose exec app sh -c 'ls -ln /run/secrets; mount | grep secrets'
docker service ps shop_app                      # then inspect the task container on its node
docker secret ls
```

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the Compose services/secrets reference and "Secrets in Compose" how-to: sources,
`environment` Compose-only, `uid`/`gid`/`mode` implemented only for `environment` sources,
`/run/secrets`, Linux only, single-file bind mount. Confirmed in the Swarm secrets page:
Raft log encryption and replication, tmpfs mount, only while tasks run, 500 KB limit,
Swarm-services-only, rotation with `--secret-add`/`--secret-rm`, versioned names, Windows
container limitation, `external: true` example, and that both `docker compose` and
`docker stack` support secrets in a Compose file. Corrected: an earlier claim that
`uid`/`gid`/`mode` are never enforced under Compose, and that `external` is meaningless
there. Removed: the "read-only" bind mount claim and the secrets-are-immutable wording.
