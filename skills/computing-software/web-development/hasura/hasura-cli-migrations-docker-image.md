---
id: computing-software.web-development.hasura.hasura-cli-migrations-docker-image
name: hasura-cli-migrations-docker-image
category: computing-software
field: web-development
product: hasura
tags: [hasura, docker, cli-migrations, auto-apply, deployment]
level: advanced
status: docs-checked
description: "Auto-apply Hasura migrations and metadata at server startup with the cli-migrations-v3 Docker image and mounted directories."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/migrations-metadata-seeds/auto-apply-migrations.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/deployment-guides/docker.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: boot a server that already has your schema.

Use the image tag `hasura/graphql-engine:<VERSION>.cli-migrations-v3`. Mount your project folders into the container:

```yaml
services:
  graphql-engine:
    image: hasura/graphql-engine:<VERSION>.cli-migrations-v3
    volumes:
      - ./migrations:/hasura-migrations
      - ./metadata:/hasura-metadata
    environment:
      HASURA_GRAPHQL_METADATA_DATABASE_URL: <METADATA_DB_URL>
      HASURA_GRAPHQL_ADMIN_SECRET: <ADMIN_SECRET>
```
Behaviour per the docs: at start the image runs a temporary server securely through `localhost` with the Migrations API allowed, applies the migrations and metadata, then reboots in secure mode for consumer GraphQL usage. The container paths are `/hasura-migrations` and `/hasura-metadata`.

Docker deployment basics: fetch the sample `docker-compose.yaml` from the Hasura install manifests, set the metadata database URL and admin secret, then `docker compose up -d`.

Gotcha: the docs say this image is not intended to be used as an init container that deploys metadata and migrations and then shuts down before the real server runs.

## Checked

2026-11-04. Confirmed against the cited pages: auto-apply-migrations and docker deployment pages: image tag form, mount paths, startup sequence, init-container warning, docker compose steps. Removed or corrected: Verify step with `hasura metadata diff`/`migrate status` and the health-endpoint claim.

Method: documentation only; no commands were run.
