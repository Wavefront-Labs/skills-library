---
id: computing-software.devops-ci-cd.rundeck.run-docker-image
name: run-docker-image
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, docker-image, docker-run, persistent-data, docker-zoo]
level: intro
status: docs-checked
description: "Run Rundeck Community or Enterprise in Docker with persistent data, pass database settings by RUNDECK_DATABASE variables, and avoid deploying public images straight to production."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/install/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Community image (`rundeck/rundeck` on Docker Hub), with a volume so server data survives the container:

```bash
docker run --name some-rundeck -p 4440:4440 -v data:/path/to/rundeck-home/server/data rundeck/rundeck:<version>
```

Enterprise image (`rundeckpro/enterprise`) needs an accessible MySQL instance with a database, user and privileges already set up. Pass the connection as environment variables:

```bash
docker run --name some-rundeck \
  -v data:/path/to/rundeck-home/server/data \
  -e RUNDECK_DATABASE_DRIVER=org.mariadb.jdbc.Driver \
  -e RUNDECK_DATABASE_USERNAME="${DB_USERNAME}" \
  -e RUNDECK_DATABASE_PASSWORD="${DB_PASSWORD}" \
  -e RUNDECK_DATABASE_URL="${DB_URL}" \
  rundeckpro/enterprise:<version>
```

Gotchas:
- The docs warn against deploying straight from a public repository such as Docker Hub. Build a derived image and keep it in your private registry.
- Full options are on the separate Docker configuration reference page.
- The rundeck/docker-zoo repository has compose examples: basic with persistent storage, MySQL, Oracle, LDAP and a cloud deployment. Use them as templates.

## Checked

2026-11-04: both docker run commands, image names, RUNDECK_DATABASE variables, MySQL prerequisite, the public-registry warning and the docker-zoo examples confirmed against the Running Docker Images page (data path shown as a placeholder). Removed the unsourced Verify line.
Method: documentation only; no commands were run.
