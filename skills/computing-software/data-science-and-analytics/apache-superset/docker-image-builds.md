---
id: computing-software.data-science-and-analytics.apache-superset.docker-image-builds
name: docker-image-builds
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [docker-builds, build-args, lean-image, chromium, python-version]
level: practitioner
status: docs-checked
description: "Superset Docker image presets (superset, lean, dev, py311, py312) and build args BUILD_TRANSLATIONS, DEV_MODE, INCLUDE_CHROMIUM and PY_VER."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/docker-builds.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick or build an image with the right size and capabilities.

Published build presets (tags without a suffix are the `superset` preset):
- `superset`: the default image, frontend and backend, with `psycopg2-binary`, `mysqlclient`, the MCP server dependencies and a headless Chromium (Playwright). You still add drivers for your analytics databases.
- `lean` (tags such as `7.0.0-lean`): frontend and backend but no database drivers at all, metadata database included; layer `mysqlclient` or `psycopg2-binary` plus your analytics drivers.
- `dev`: development utilities and root access, some common drivers, no headless browser by default.
- `py311` and `py312`: like lean with a different Python version.
- From 7.0.0 tags follow this superset/lean naming; for 6.1.0 and earlier the plain tag is the minimal image.

Key build arguments in the Dockerfile:
- `BUILD_TRANSLATIONS`: compile non-English translations into the image (default false, only `en` ships). It only takes effect when building from the repository's own Dockerfile, not in a downstream Dockerfile that extends a published tag.
- `DEV_MODE`: skip the frontend build; used by the docker-compose dev setup that mounts local code and runs webpack in watch mode.
- `INCLUDE_CHROMIUM`: include Chromium in the backend build for Alerts and Reports and thumbnails.
- `PY_VER`: base image for the Python backend; the page advises against changing it unless you work on Python compatibility.

Example (dev target with Chromium):

```bash
docker build --target dev --build-arg INCLUDE_CHROMIUM=true -t my-superset-dev .
```

Notes:
- To start from `-lean` and add only what you need, write a small Dockerfile with `FROM apache/superset:7.0.0-lean` and install your drivers and Playwright Chromium.
- The `-lean` and `-dev` published images carry no Chromium, so add it when workers must render reports.
- Pin image tags in deployments.

## Checked

2026-11-08. Confirmed against the Docker Builds page (read the presets, key ARGs and tag sections; Dockerfile example section skimmed): presets, driver contents, BUILD_TRANSLATIONS, DEV_MODE, INCLUDE_CHROMIUM, PY_VER, Chromium in default but not lean/dev images. Removed: the claim that drivers are absent from the base image (the default image bundles psycopg2-binary and mysqlclient), SERVER_THREADS_AMOUNT (the page ties it to ci and showtime targets only), the unverified `--target lean` example, "rebuild on a schedule".
Method: documentation only; no commands were run.
