---
id: computing-software.cybersecurity-defensive.dex.dex-custom-templates-container-image
name: dex-custom-templates-container-image
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [templates, docker, container-image, frontend]
level: practitioner
status: docs-checked
description: "Bake custom Dex templates into the official image with a Dockerfile setting DEX_FRONTEND_DIR instead of frontend.dir."
sources:
  - https://dexidp.io/docs/guides/templates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex is primarily distributed as a container image. To ship custom templates, build your own image on top of the official one and set the frontend directory through an environment variable:

```dockerfile
FROM ghcr.io/dexidp/dex:latest
ENV DEX_FRONTEND_DIR=/srv/dex/web
COPY --chown=root:root web /srv/dex/web
```

With this, you can leave out the `frontend.dir` setting in the config because `DEX_FRONTEND_DIR` points Dex at the copied directory.

Workflow:

1. Copy the stock `web` directory into your repository and edit the templates, keeping all existing variables.
2. Build the image with the Dockerfile above.
3. Run it with a config that may still set `frontend.issuer` and `frontend.extra` for titles and custom values.
4. Walk through a login to verify the pages.

Pin a tag in the `FROM` line instead of `latest` for repeatable builds.

Gotcha: the docs warn to retain all existing template variables, so diff your templates against the stock `web` directory when you upgrade the base image.

## Checked
2026-11-09: read the Dex Customizing Dex Templates guide in full; the Dockerfile and the `DEX_FRONTEND_DIR` note match. Removed the claim about Alpine and Distroless image variants (not on the page).
Method: documentation only; no commands were run.
