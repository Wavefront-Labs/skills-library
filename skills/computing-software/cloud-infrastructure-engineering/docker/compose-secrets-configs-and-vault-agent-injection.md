---
id: computing-software.cloud-infrastructure-engineering.docker.compose-secrets-configs-and-vault-agent-injection
name: compose-secrets-configs-and-vault-agent-injection
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, secrets, compose-secrets, secrets-file, compose-configs, config-mount, secret-injection]
level: advanced
status: docs-checked
description: "Mount secrets and config files into Compose services with top-level secrets and configs (file, environment, content), long-syntax target, uid, gid and mode, and build secrets."
sources: ["https://docs.docker.com/compose/how-tos/use-secrets/", "https://docs.docker.com/reference/compose-file/secrets/", "https://docs.docker.com/reference/compose-file/configs/", "https://docs.docker.com/reference/compose-file/services/#secrets"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Compose secrets and configs

## Secrets (no Swarm needed)
```yaml
services:
  api:
    image: app/api
    secrets:
      - db_password                          # -> /run/secrets/db_password
      - source: tls_key
        target: /etc/app/tls.key             # absolute path, or a name under /run/secrets/
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt          # host file (keep out of git)
  tls_key:
    environment: TLS_KEY                     # value of a host environment variable
```
- A secret's source is `file` or `environment`; `environment` is only supported by Docker
  Compose, not by `docker stack deploy`.
- Secrets are mounted as files in `/run/secrets/<secret_name>`. They are supported on Linux
  containers only, because Compose delivers each secret by bind-mounting a single file.
- Defining a top-level secret does not grant access; each service must list the secret.
- Long syntax fields: `source`, `target`, `uid`, `gid`, `mode` (default `0444`). In Compose
  these `uid`, `gid` and `mode` attributes are only implemented when the secret source is
  `environment`; with a `file` source Compose uses a bind mount that cannot remap
  ownership, and the attributes are silently ignored.
- The `*_FILE` variables above are an image convention (used by the official mysql and
  postgres images), not something Compose provides.
- Build-time secrets are declared under `build.secrets` and use the same top-level
  definitions (for example `environment: NPM_TOKEN`).

## Configs
```yaml
services:
  nginx:
    image: nginx
    configs:
      - source: nginx_conf
        target: /etc/nginx/conf.d/default.conf
configs:
  nginx_conf:
    file: ./nginx/default.conf
  feature_flags:
    content: |                                # inline value; variables are interpolated
      {"newCheckout": ${NEW_CHECKOUT:-false}}
  app_env:
    environment: APP_SETTINGS
```
- A config's source is `file`, `environment`, `content` or `external`; `environment` and
  `content` were introduced in Compose 2.23.1.
- Short syntax mounts the config at `/<config_name>` in Linux containers. Long syntax has
  `source`, `target`, `uid`, `gid` and `mode` (default `0444`, world-readable).
- With `content`, Compose infers variables when creating the config, so the content can
  follow service configuration through interpolation.

## Runtime-injected secrets
When a secret is fetched at runtime by a separate tool, have that tool write files into a
volume that the application container mounts, and keep the volume out of the image and of
version control. The Compose features above (files in `/run/secrets`) do not themselves
rotate or fetch anything.

## Verify
`docker compose exec api ls -l /run/secrets`; `docker compose config` shows the normalised
secret and config definitions (including short syntax expanded to a `target`).

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the "Secrets in Compose" how-to and the Compose file reference for services,
secrets and configs: secret sources and the `environment` Compose-only note, `/run/secrets`
mount and Linux-only note, long-syntax fields and the `uid`/`gid`/`mode` limitation
(file-sourced secrets ignore them), config sources and the 2.23.1 introduction of
`environment` and `content`, config default mount path and mode, build secrets example.
Removed: the Vault Agent sidecar, its tmpfs volume trick and image tag, which no checked
Docker documentation covers; the claims that mounts are read-only or encrypted, that
recreation follows content changes, and the `docker inspect` remark.
