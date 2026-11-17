---
id: computing-software.web-development.directus.version-pinning-upgrade
name: version-pinning-upgrade
category: computing-software
field: web-development
product: directus
tags: [version-pinning, upgrade-directus, breaking-changes, auto-migrations]
level: practitioner
status: docs-checked
description: "Pin the Directus Docker image tag, review the breaking changes list, then upgrade by changing the tag; database migrations run automatically."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/self-hosting/4.upgrading.md
  - https://raw.githubusercontent.com/directus/docs/main/content/self-hosting/3.deploying.md
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/10.environment-sync/1.quickstart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pin an explicit tag in production, for example `directus/directus:11.1.1` (shown in the docs as an example), instead of `latest`, so restarts never pull in breaking changes.

Upgrade procedure:
1. Read the breaking changes list for every release between your version and the target. They can change environment variables, REST and GraphQL APIs, the JavaScript SDK, and internal services used by extension authors.
2. Change the tag in `docker-compose.yml` or your `Dockerfile`. If you used `latest`, restart the container.
3. All database migrations are handled automatically.

Releases arrive roughly monthly, with faster ones for critical fixes.

Gotcha: Environment Sync requires source and target instances to run the identical version, patch included, so upgrade environments together.

## Checked

2026-11-04: tag pinning with the 11.1.1 example, breaking-changes list contents, tag update in docker-compose.yml or Dockerfile, automatic migrations, monthly release cadence and the Environment Sync identical-version rule confirmed against the Directus Upgrading, Deploying and Environment Sync quickstart pages. Removed a backup step and a Verify line that the pages do not state.

Method: documentation only; no commands were run.
