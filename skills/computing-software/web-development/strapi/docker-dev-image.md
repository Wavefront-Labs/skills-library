---
id: computing-software.web-development.strapi.docker-dev-image
name: docker-dev-image
category: computing-software
field: web-development
product: strapi
tags: [strapi, docker, dockerfile, node-alpine, vips, develop]
level: practitioner
status: docs-checked
description: "A development Dockerfile for Strapi on node alpine, with native build packages and the database pool min of 0."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/installation/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker: development image

Shape of the development Dockerfile:

```dockerfile
FROM node:22-alpine
# system packages for native modules and image processing:
# build-base, vips-dev, etc. (full apk list on the page)
ARG NODE_ENV=development
ENV NODE_ENV=${NODE_ENV}
# copy package files, then:
RUN npm ci
# copy the project
EXPOSE 1337
CMD ["npm", "run", "develop"]
```

Install the apk packages the page lists before `npm ci`, since sharp and other native modules need them on alpine.

## Database pool
The page's troubleshooting steps set the connection pool `min` to `0` in the database configuration, as Docker may kill idle connections (`computing-software.web-development.strapi.database-pool-docker`).

The page's production Dockerfile is a separate multi-stage image whose final command is `npm run start`, not `develop` (`computing-software.web-development.strapi.production-build-launch`).

## Checked

Checked 2026-11-04 against the Strapi Docker installation page (dev Dockerfile, production Dockerfile, troubleshooting). Reworded the pool and production notes to what the page states.

Method: documentation only; no commands were run.
